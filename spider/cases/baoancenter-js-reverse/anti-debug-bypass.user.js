// ==UserScript==
// @name         宝安文体通 反调试绕过 (bawtt.ydmap.cn anti-debug bypass)
// @namespace    baoan-ydmap
// @version      1.0.0
// @description  解除 bawtt.ydmap.cn 的无限 debugger 反调试,恢复可正常调试
// @match        https://bawtt.ydmap.cn/*
// @run-at       document-start
// @grant        none
// ==/UserScript==

/**
 * 反调试原理:
 *   该站 signature.min.js / 随机路径脚本(<host>/<x>/<y>/<z>) 会把签名逻辑
 *   拆成大量 `new Function(...)` / `eval(...)` 生成的微型函数,并在函数体里
 *   注入 `debugger` 语句(用 String.fromCharCode 动态拼出,源码里搜不到字面量)。
 *   当 DevTools 挂上调试器时,这些函数每执行一次就命中一次 debugger -> 无限暂停。
 *
 * 绕过思路:
 *   在页面脚本运行前(document-start)劫持所有能到达 Function 构造器 / eval 的
 *   入口,把生成代码里的 `debugger` 语句剥掉。函数语义不变,签名照常计算。
 *
 * 用法:
 *   1) Tampermonkey 安装本脚本,刷新页面即可正常调试;
 *   2) 或把下面 IIFE 直接粘到 DevTools Console 执行(仅对后续生成的函数生效)。
 */

(function () {
  'use strict';

  // 去掉字符串里的 debugger 语句(保留其余逻辑)
  var strip = function (s) {
    return typeof s === 'string' ? s.replace(/\bdebugger\s*;?/g, '') : s;
  };

  // 包装一个"函数构造器":把最后一个字符串参数(body)里的 debugger 剥掉
  var wrap = function (orig) {
    return function () {
      var a = Array.prototype.slice.call(arguments);
      var n = a.length;
      if (n && typeof a[n - 1] === 'string') a[n - 1] = strip(a[n - 1]);
      return orig.apply(this, a);
    };
  };

  var Native = Function; // 原生的 %Function%

  // 1) 覆盖全局 Function 绑定 -> 拦 `new Function(...)` / `Function(...)`
  try { window.Function = wrap(Native); } catch (e) {}

  // 2) 覆盖 Function.prototype.constructor -> 拦 `xxx.constructor(...)`
  try { Function.prototype.constructor = window.Function; } catch (e) {}

  // 3) 覆盖各内建构造器的 .constructor -> 拦 `[].constructor.constructor(...)` 等
  [Array, Object, String, Number, Boolean, RegExp, Date].forEach(function (C) {
    try { C.constructor = window.Function; } catch (e) {}
  });

  // 4) 覆盖 eval -> 拦 `eval('...debugger...')`
  try {
    var _eval = window.eval;
    window.eval = function (s) { return _eval(strip(s)); };
  } catch (e) {}

  // 5) 覆盖定时器字符串形式 -> 拦 `setTimeout('debugger...')`
  ['setTimeout', 'setInterval'].forEach(function (name) {
    try {
      var orig = window[name];
      window[name] = function (fn, delay) {
        var a = Array.prototype.slice.call(arguments);
        if (typeof a[0] === 'string') a[0] = strip(a[0]);
        return orig.apply(this, a);
      };
    } catch (e) {}
  });

  window.__antiDebugBypass = true;
})();
