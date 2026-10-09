/* ══════════════════════════════════════════════════
   月轮观解读浮层 — 挂载到官方页面快照上
   不改动原站 DOM 结构，仅追加按钮与浮层
   ══════════════════════════════════════════════════ */
(function () {
  'use strict';

  var A = 'assets/';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  if (typeof DATA === 'undefined' || typeof PROLOGUE === 'undefined') {
    console.error('[月轮观] data.js 未加载');
    return;
  }

  /* ── 扁平索引 ── */
  var IDX = [];
  FLOOR_ORDER.forEach(function (fid) {
    var f = DATA.find(function (d) { return d.id === fid; });
    f.chars.forEach(function (c) { IDX.push({ floor: f, char: c }); });
  });

  /* ── 从原站 DOM 抓取真实的风味文本 ── */
  /* 原站简介容器特征：class 含 px-20 + font-sans + leading-relaxed，内部以 <br> 分行 */
  var DESC_SEL = '.px-20.py-10.font-sans';

  function scrapeOfficialText() {
    var map = {};
    $$('h3').forEach(function (h3) {
      var name = (h3.textContent || '').trim();
      if (!name) return;
      var li = h3.closest('li');
      if (!li) return;
      var box = li.querySelector(DESC_SEL);
      if (!box) return;
      var t = (box.textContent || '').replace(/\s+/g, ' ').trim();
      if (t) map[name] = t;
    });
    return map;
  }
  var OFFICIAL = scrapeOfficialText();

  /* ── 楼层容器（含统治者）───────────────────────── */
  function collectSections() {
    var out = [];
    var sv = $('#stratum-0');
    if (sv) out.push({ floorId: 'sovereign', el: sv });
    for (var i = 1; i <= 8; i++) {
      var el = document.getElementById('stratum-' + i);
      if (el) out.push({ floorId: 'stratum-' + i, el: el });
    }
    return out;
  }

  /* ── 在每个角色条目上挂「佛学解读」按钮 ── */
  var INJECT_BTN =
    '<button class="mn-inject" type="button">' +
    '<span>佛学解读</span>' +
    '<svg class="mn-ic" viewBox="0 0 36 64.82" aria-hidden="true"><path d="M1562,1941.85l8,12.15-8,12.15-8-12.15Zm-8,44.55,24-32.4-24-32.4,36,32.4Z" transform="translate(-1554 -1921.59)"/></svg>' +
    '</button>';

  function injectButtons() {
    var n = 0;
    IDX.forEach(function (entry) {
      var name = entry.char.name;
      // 在原站中找该角色的 h3
      var h3 = null;
      $$('h3').some(function (el) {
        if ((el.textContent || '').trim() === name) { h3 = el; return true; }
        return false;
      });
      if (!h3) return;

      var li = h3.closest('li') || h3.parentElement;
      if (!li) return;
      if (li.querySelector('.mn-inject')) return;

      /* 落点：官方简介容器（.px-20.py-10.font-sans）之后；
         若无简介，则退回角色名 h3 的所在块之后 */
      var anchor = li.querySelector(DESC_SEL);
      /* 注意：原站简介容器祖先为 pointer-events:none，且 `*:pointer-events-auto`
         仅对直接子元素生效。因此按钮必须直接挂到该容器内，不能再包一层 div。 */
      var host = anchor || h3.parentElement;
      if (!host) return;

      host.insertAdjacentHTML('beforeend', INJECT_BTN);
      var real = host.querySelector('.mn-inject');
      if (!real) return;

      real.setAttribute('data-mn-gid', entry.floor.id + '__' + name);
      real.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        open(entry.floor.id + '__' + name);
      });
      n++;
    });
    return n;
  }

  /* ── 浮层 ── */
  var ov = $('#moonOverlay');
  var panel = $('.mn-panel');
  var scrollBox = $('.mn-scroll');
  var lastFocus = null;

  function open(gid) {
    var i = IDX.findIndex(function (x) { return x.floor.id + '__' + x.char.name === gid; });
    if (i < 0) return;
    lastFocus = document.activeElement;
    render(i);
    ov.classList.add('mn-open');
    ov.setAttribute('aria-hidden', 'false');
    document.documentElement.style.overflow = 'hidden';
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { ov.classList.add('mn-visible'); });
    });
    var c = $('.mn-close'); if (c) c.focus();
  }

  function close() {
    ov.classList.remove('mn-visible');
    ov.setAttribute('aria-hidden', 'true');
    document.documentElement.style.overflow = '';
    setTimeout(function () { ov.classList.remove('mn-open'); }, 480);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function render(i) {
    var e = IDX[i];
    var f = e.floor, c = e.char, r = c.reading;
    var F = FACTIONS[c.faction];
    var fc = F.color;

    panel.style.setProperty('--mn-fc', fc);
    $('#mnHeroImg').src = A + c.img;
    $('#mnHeroImg').alt = c.name;

    var CN = ['零', '一', '二', '三', '四', '五', '六', '七', '八'];
    var floorTxt = f.id === 'sovereign'
      ? '监狱统治者'
      : '第' + CN[f.floor] + '层“' + f.floorName + '”';

    $('#mnBadges').innerHTML =
      '<span class="mn-badge mn-badge--solid" style="--mn-fc:' + fc + '">' + esc(F.label) + '</span>' +
      '<span class="mn-badge" style="--mn-fc:' + fc + '">' + esc(r.role) + '</span>' +
      '<span class="mn-badge" style="--mn-fc:' + fc + '">' + esc(floorTxt) + '</span>';

    $('#mnTitle').textContent = r.title;
    $('#mnProto').innerHTML = '佛学原型 · <b>' + esc(r.proto) + '</b>';

    var out = [];

    /* 位分条 */
    out.push(
      '<div class="mn-role-line">' +
      '<div class="mnrl"><span class="mnrl-k">阵营</span><span class="mnrl-v">' + esc(F.label) + '</span></div>' +
      '<div class="mnrl"><span class="mnrl-k">位分</span><span class="mnrl-v">' + esc(r.role) + '</span></div>' +
      (c.cv ? '<div class="mnrl"><span class="mnrl-k">声优</span><span class="mnrl-v">' + esc(c.cv) + '</span></div>' : '') +
      '</div>');

    /* 概述 */
    out.push('<div class="mn-summary">' + esc(r.summary) + '</div>');

    /* 对位（成对时） */
    if (f.id !== 'sovereign' && f.chars.length === 2) {
      var other = f.chars.find(function (x) { return x !== c; });
      if (other) {
        out.push(
          '<div class="mn-match">' +
          '<div class="mn-match-k">本层对位 · ' + esc(f.pairTitle) + '</div>' +
          '<div class="mn-pair">' +
          '<div class="mn-side mn-side--a">' +
          '<div class="mn-side-n">' + esc(c.name) + '</div>' +
          '<div class="mn-side-r">' + esc(r.role) + '</div>' +
          '<div class="mn-side-p">' + esc(r.proto.split('——')[0].trim()) + '</div>' +
          '</div>' +
          '<div class="mn-vs">⟷</div>' +
          '<div class="mn-side mn-side--b">' +
          '<div class="mn-side-n">' + esc(other.name) + '</div>' +
          '<div class="mn-side-r">' + esc(other.reading.role) + '</div>' +
          '<div class="mn-side-p">' + esc(other.reading.proto.split('——')[0].trim()) + '</div>' +
          '</div>' +
          '</div></div>');
      }
    }

    /* 分节 */
    r.sections.forEach(function (s) {
      /* p 兼容两种写法：字符串 或 字符串数组 */
      var paras = s.p == null ? [] : (Array.isArray(s.p) ? s.p : [s.p]);
      var ps = paras.map(function (p) {
        return '<p class="mn-sec-p">' + esc(p) + '</p>';
      }).join('');
      var q = s.quote ? '<blockquote class="mn-quote">' + esc(s.quote) + '</blockquote>' : '';
      out.push('<section class="mn-sec"><h4 class="mn-sec-h">' + esc(s.h) + '</h4>' + ps + q + '</section>');
    });

    /* 导航 */
    var p = IDX[i - 1], n = IDX[i + 1];
    out.push(
      '<nav class="mn-nav">' +
      '<button ' + (p ? 'data-go="' + p.floor.id + '__' + p.char.name + '"' : 'disabled') + '>' +
      '<span class="mn-nav-k">← 上一位</span><span class="mn-nav-v">' + (p ? esc(p.char.name) : '已是首位') + '</span></button>' +
      '<button ' + (n ? 'data-go="' + n.floor.id + '__' + n.char.name + '"' : 'disabled') + '>' +
      '<span class="mn-nav-k">下一位 →</span><span class="mn-nav-v">' + (n ? esc(n.char.name) : '已是末位') + '</span></button>' +
      '</nav>');

    var body = $('#mnBody');
    body.innerHTML = '<div class="mn-stag">' + out.join('') + '</div>';
    scrollBox.scrollTop = 0;

    $$('[data-go]', body).forEach(function (b) {
      b.addEventListener('click', function () {
        var gid = b.getAttribute('data-go');
        var j = IDX.findIndex(function (x) { return x.floor.id + '__' + x.char.name === gid; });
        if (j >= 0) render(j);
      });
    });
  }

  /* ── 关闭交互 ── */
  $$('[data-mn-close]').forEach(function (el) {
    el.addEventListener('click', close);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && ov.classList.contains('mn-open')) close();
  });

  /* ── FAB ── */
  var fab = $('#mnFab');
  if (fab) fab.addEventListener('click', function () { open(IDX[0].floor.id + '__' + IDX[0].char.name); });

  /* ── 楼层侧栏 ── */
  function buildRail() {
    var rail = $('#mnRail');
    if (!rail) return;
    rail.innerHTML = DATA.map(function (f) {
      var c = f.chars[0];
      return '<button type="button" data-go="' + f.id + '__' + c.name + '">' +
        '<span class="mn-rail-d"></span>' +
        '<span class="mn-rail-t">' + (f.id === 'sovereign' ? '统治者' : '第' + f.floor + '层 ' + f.floorName) + '</span>' +
        '</button>';
    }).join('');
    $$('button', rail).forEach(function (b) {
      b.addEventListener('click', function () {
        open(b.getAttribute('data-go'));
      });
    });
  }

  /* ── 滚动时显隐侧栏 ── */
  function initRailScroll() {
    var rail = $('#mnRail');
    if (!rail) return;
    var tick = false;
    window.addEventListener('scroll', function () {
      if (tick) return;
      tick = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        rail.classList.toggle('mn-show', y > window.innerHeight * 0.8);
        tick = false;
      });
    }, { passive: true });
  }

  /* ── 启动 ── */
  function boot() {
    var n = injectButtons();
    buildRail();
    initRailScroll();
    console.log('[月轮观] 已挂载解读入口：' + n + ' / ' + IDX.length);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();