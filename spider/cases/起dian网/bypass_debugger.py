#!/usr/bin/env python3
"""通过 CDP Network.setBlockedURLs + Fetch 双重拦截 probev3.js - 稳定版"""

import json
import websocket
import time
import threading
import urllib.request
import queue

CHROME_HOST = "localhost"
CHROME_PORT = 9223

event_queue = queue.Queue()
response_map = {}
response_lock = threading.Lock()

def on_message(ws, raw):
    try:
        resp = json.loads(raw)
        msg_id = resp.get("id")
        if msg_id is not None:
            with response_lock:
                response_map[msg_id] = resp
            return
        event_queue.put(resp)
    except:
        pass

def send_cdp(ws, method, params=None, timeout=30):
    msg_id = int(time.time() * 1_000_000) % 2**31
    payload = {"id": msg_id, "method": method}
    if params:
        payload["params"] = params
    ws.send(json.dumps(payload))

    deadline = time.time() + timeout
    while time.time() < deadline:
        with response_lock:
            if msg_id in response_map:
                resp = response_map.pop(msg_id)
                if "error" in resp:
                    print(f"  [{method}] Error: {resp['error']}")
                    return None
                return resp.get("result")
        time.sleep(0.02)
    print(f"  [{method}] Timeout")
    return None

def send_to_session(ws, session_id, method, params=None, timeout=30):
    msg_id = int(time.time() * 1_000_000) % 2**31
    payload = {"id": msg_id, "method": method, "sessionId": session_id}
    if params:
        payload["params"] = params
    ws.send(json.dumps(payload))

    deadline = time.time() + timeout
    while time.time() < deadline:
        with response_lock:
            if msg_id in response_map:
                resp = response_map.pop(msg_id)
                if "error" in resp:
                    print(f"  [{method}] Error: {resp['error']}")
                    return None
                return resp.get("result")
        time.sleep(0.02)
    print(f"  [{method}] Timeout")
    return None

def main():
    version_url = f"http://{CHROME_HOST}:{CHROME_PORT}/json/version"
    version_data = json.loads(urllib.request.urlopen(version_url).read())
    browser_ws_url = version_data["webSocketDebuggerUrl"]
    print(f"WebSocket: {browser_ws_url}")

    ws = websocket.WebSocketApp(browser_ws_url, on_message=on_message)
    t = threading.Thread(target=ws.run_forever, daemon=True)
    t.start()
    time.sleep(0.5)

    # Fetch.enable 在浏览器级别启用
    print("浏览器级别: Fetch.enable")
    send_cdp(ws, "Fetch.enable", {
        "patterns": [
            {"urlPattern": "*://*.qidian.com/*/probev3.js", "requestStage": "Request"},
            {"urlPattern": "*://*.qidian.com/*probev3*", "requestStage": "Request"},
        ]
    })

    # 创建页面
    create_result = send_cdp(ws, "Target.createTarget", {"url": "about:blank"})
    target_id = create_result["targetId"]
    print(f"Target: {target_id}")

    attach_result = send_cdp(ws, "Target.attachToTarget", {
        "targetId": target_id, "flatten": True
    })
    session_id = attach_result["sessionId"]
    print(f"Session: {session_id}")

    # Session 级别 Fetch 拦截
    send_to_session(ws, session_id, "Fetch.enable", {
        "patterns": [
            {"urlPattern": "*probev3*", "requestStage": "Request"},
        ]
    })

    # Debugger 防护
    send_to_session(ws, session_id, "Debugger.enable")
    send_to_session(ws, session_id, "Debugger.setSkipAllPauses", {"skip": True})

    # Runtime + Page
    send_to_session(ws, session_id, "Runtime.enable")
    send_to_session(ws, session_id, "Page.enable")

    # 关键: 等待确保所有拦截都已就绪
    print("等待所有拦截器就绪...")
    time.sleep(2)

    # 导航
    print("导航到起点章节页...")
    send_to_session(ws, session_id, "Page.navigate", {
        "url": "https://www.qidian.com/chapter/1209977/23724364/"
    })

    # 事件处理循环
    print("处理事件...")
    deadline = time.time() + 60
    load_fired = False
    blocked_count = 0

    while time.time() < deadline and not load_fired:
        try:
            event = event_queue.get(timeout=2)
        except queue.Empty:
            continue

        method = event.get("method", "")
        event_session = event.get("sessionId", "")
        params = event.get("params", {})

        # 处理 Fetch.requestPaused（作为双重保险）
        if method == "Fetch.requestPaused":
            request_id = params.get("requestId", "")
            url = params.get("request", {}).get("url", "")

            if "probev3" in url:
                blocked_count += 1
                print(f"  [封锁 #{blocked_count}] probev3.js (Fetch)")
                send_to_session(ws, event_session, "Fetch.fulfillRequest", {
                    "requestId": request_id,
                    "responseCode": 200,
                    "responseHeaders": [
                        {"name": "Content-Type", "value": "application/javascript"},
                    ],
                    "body": "LyogQkxPQ0tFRCAqLw=="
                })
            else:
                send_to_session(ws, event_session, "Fetch.continueRequest", {
                    "requestId": request_id
                })

        elif method == "Page.loadEventFired":
            print(f"  Page.loadEventFired! session={event_session[:20]}")
            if event_session == session_id:
                load_fired = True

        elif method == "Target.attachedToTarget":
            new_session = event_session
            if new_session and new_session != session_id:
                send_to_session(ws, new_session, "Fetch.enable", {
                    "patterns": [{"urlPattern": "*probev3*", "requestStage": "Request"}]
                })
                send_to_session(ws, new_session, "Debugger.enable")
                send_to_session(ws, new_session, "Debugger.setSkipAllPauses", {"skip": True})

    print(f"\n共拦截 probev3.js {blocked_count} 次")
    time.sleep(2)

    # 获取结果
    print("\n" + "="*60)
    print("页面结果")
    print("="*60)

    def evaluate(expr):
        resp = send_to_session(ws, session_id, "Runtime.evaluate", {
            "expression": expr, "returnByValue": True
        }, timeout=10)
        return resp.get("result", {}).get("value", "N/A") if resp else "N/A"

    print(f"URL: {evaluate('location.href')}")
    print(f"标题: {evaluate('document.title')}")
    print(f"状态: {evaluate('JSON.stringify({readyState: document.readyState, hasBody: !!document.body, bodyChildCount: document.body ? document.body.children.length : 0, htmlLen: document.documentElement.outerHTML.length})')}")

    text = evaluate("document.body ? document.body.innerText.substring(0, 5000) : 'no body'")
    if text and text != "no body":
        print(f"\n--- Body Text (前5000) ---")
        print(text)
        print(f"--- 总长度: {len(text)} ---")
    else:
        print("Body: 无内容或为空")

    # 不关闭页面，保留给用户查看
    # send_cdp(ws, "Target.closeTarget", {"targetId": target_id})
    # 清理拦截（如果页面有后续请求会用到 probev3）
    # send_cdp(ws, "Network.setBlockedURLs", {"urls": []})
    print("\n页面已加载，请在 Chrome 窗口中查看。页面将保持打开。")
    print("按 Ctrl+C 退出...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    send_cdp(ws, "Target.closeTarget", {"targetId": target_id})
    ws.close()
    print("\n完成!")

if __name__ == "__main__":
    main()
