# 宝安文体通 (bawtt.ydmap.cn) 反调试逆向报告

## 目标
https://bawtt.ydmap.cn/ -> 302 重定向 -> https://bawtt.ydmap.cn/srv100244/api/pub/page/page.shtml?id=101456

## 结论摘要
- **无限 debugger 来源**: `signature.min.js`(以及每次会话随机的 `<host>/<x>/<y>/<z>` 引导脚本)把签名逻辑拆成
  大量 `new Function(...)` / `eval(...)` 生成的微型函数,体内注入 `debugger` 语句。
  `debugger` 用 `String.fromCharCode` 动态拼出,源码里搜不到字面量(搜 `debugger` 只命中运行时 eval 产物)。
- **反调试第二层**: `signature.min.js` 用 Proxy 包装某个 `window` 函数,临时把 `Function.prototype.toString`
  换成抛异常函数做自检,检测到篡改则 `for(;;)` 死循环冻死标签页(反「反调试」)。
- **绕过方案(已验证)**: document-start 劫持全局 `Function` 绑定 + `Function.prototype.constructor`
  + 各内建 `.constructor` + `eval`,剥掉生成代码里的 `debugger`。实测 `new Function('debugger')`、
  `(function(){}).constructor('debugger')`、`[].constructor.constructor('debugger')`、`eval('debugger')`
  生成的代码均不再含 debugger,且返回值正确。

## 关键网络证据 (js-reverse reqid)
- reqid=1  `GET /` -> reqid=31 `GET /srv100244/.../page.shtml?id=101456` (重定向)
- reqid=34 页面带 `type__1386=<密文>` 重新请求 (签名回注)
- reqid=9/38 `signature.min.js` + reqid=13/55 `portal.wasm?commitId=06b10670` (签名引擎)
- reqid=33 随机路径脚本 `/u21pn7x6/r8lw5pzu/psk8uqfi` (172KB, 反调试引导, 运行后自删)
- reqid=26 `fingerprintjs` (浏览器指纹)
- reqid=30/80 API 带 `type__1386=<密文>` (如 srv200/api/pub/tool/sysDate)

## 待办 / 后续
- `type__1386` 签名算法逆向 (signature.min.js + portal.wasm, 疑为瑞数类自定义编码, 密文大量 `W` 字符)
- 999998「频次过快」: 服务端风控, 疑为 IP 级限流或签名缺失, 需进一步定位
