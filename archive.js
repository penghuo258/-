/* ══════════════════════════════════════════════
   月轮观 · 八狱考据 — 渲染与视图切换
   角色排版对齐官方页：立绘大图 → 阵营行 → 大字号渐变名 → sans 简介 → 考据区
   ══════════════════════════════════════════════ */
(function () {
  'use strict';

  var A = 'archive/assets/';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  };

  if (typeof DATA === 'undefined') { console.error('[考据卷] data.js 未加载'); return; }
  var OFF = (typeof OFFICIAL !== 'undefined') ? OFFICIAL : {};
  var CN = ['零', '一', '二', '三', '四', '五', '六', '七', '八'];

  /* 官方箭头：11×20，fill #eb422e */
  var ARROW = '<svg class="mn-arrow" viewBox="0 0 36 64.82" aria-hidden="true">' +
    '<path d="M1562,1941.85l8,12.15-8,12.15-8-12.15Zm-8,44.55,24-32.4-24-32.4,36,32.4Z" ' +
    'transform="translate(-1554 -1921.59)"/></svg>';

  /* ═══ 视图切换 ═══ */
  function initSwitch() {
    var btns = $$('.vs-btn');
    var archive = $('#viewArchive');
    var source = $('#viewSource');

    function show(v) {
      var isArchive = v === 'archive';
      archive.hidden = !isArchive;
      source.hidden = isArchive;
      btns.forEach(function (b) {
        var on = b.dataset.view === v;
        b.classList.toggle('is-on', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      if (isArchive) window.scrollTo(0, 0);
    }

    btns.forEach(function (b) {
      b.addEventListener('click', function () { show(b.dataset.view); });
    });
    $$('[data-view]').forEach(function (el) {
      if (el.classList.contains('vs-btn')) return;
      el.addEventListener('click', function (e) { e.preventDefault(); show(el.dataset.view); });
    });
  }

  /* ═══ 楼层导航（两种形态：纹章 / 横排） ═══ */
  function navLabel(f) {
    if (f.id === 'sovereign') return '统治者';
    return '第' + CN[f.floor] + '层 “' + f.floorName + '”';
  }

  function buildNav() {
    var nav = $('#pairsNav');

    function render(mode) {
      nav.className = 'mn-nav mn-nav--' + mode;
      var btns = FLOOR_ORDER.map(function (fid) {
        var f = DATA.find(function (d) { return d.id === fid; });
        var fc = FACTIONS[f.chars[0].faction].color;
        var label = navLabel(f);
        var crest = '<img class="nav-crest" src="' + A + CHARA_BTN[f.chars[0].faction] +
                    '" alt="" aria-hidden="true">';
        var txt = '<span class="nav-txt">' + esc(label) + '</span>';
        var sov = f.id === 'sovereign' ? ' nav-btn--sovereign' : '';
        return '<button class="nav-btn' + sov + '" data-target="' + f.id +
               '" style="--fc:' + fc + '" type="button">' + crest + txt + '</button>';
      }).join('');

      nav.innerHTML = '<div class="mn-nav-bar">' + btns + '</div>';

      $$('.nav-btn', nav).forEach(function (b) {
        b.addEventListener('click', function () {
          var el = document.getElementById('pair-' + b.dataset.target);
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      });
      markActive(currentFloor);
    }

    render('crest');
    initNavObserver();
  }

  var currentFloor = FLOOR_ORDER[0];

  function markActive(fid) {
    currentFloor = fid;
    $$('#pairsNav .nav-btn').forEach(function (b) {
      b.classList.toggle('is-on', b.dataset.target === fid);
    });
  }

  function initNavObserver() {
    if (!('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        markActive(en.target.id.replace('pair-', ''));
      });
    }, { threshold: 0.12, rootMargin: '-15% 0px -72% 0px' });
    FLOOR_ORDER.forEach(function (f) {
      var el = document.getElementById('pair-' + f);
      if (el) io.observe(el);
    });
  }

  /* ═══ 单个角色（立绘 | 插图 | 考据 三栏对应） ═══ */
  function renderChar(c, fc, floorId) {
    var o = OFF[c.name] || {};
    var r = c.reading;

    /* 官方编号：竖排旋转于右上 */
    var noLine = (o.no || c.no || '');
    var noHtml = noLine
      ? '<span class="chara-no">绝密记录 · ' + esc(noLine.replace(/^[^：]+：/, '')) + '</span>'
      : '';

    /* 阵营行 */
    var metaHtml =
      '<div class="chara-meta">' +
        '<img src="' + A + PROFILE_IMG[c.faction] + '" alt="" aria-hidden="true">' +
        '<span>' + esc(FACTIONS[c.faction].label) + '</span>' +
      '</div>';

    /* 官方风味文本（sans，与官方一致） */
    var descHtml = (o.desc || c.desc)
      ? '<p class="chara-desc">' + esc(o.desc || c.desc) + '</p>'
      : '';

    var cvTxt = o.cv || (c.cv ? '声优：' + c.cv : '');
    var cvHtml = cvTxt ? '<p class="chara-cv">' + esc(cvTxt) + '</p>' : '';

    /* 位分条 */
    var roleLine =
      '<div class="rd-role">' +
        '<div class="rdr"><span class="rdr-k">位分</span><span class="rdr-v">' + esc(r.role) + '</span></div>' +
        '<div class="rdr"><span class="rdr-k">原型</span><span class="rdr-v">' + esc(r.proto.split('——')[0].trim()) + '</span></div>' +
        (c.cv ? '<div class="rdr"><span class="rdr-k">声优</span><span class="rdr-v">' + esc(c.cv) + '</span></div>' : '') +
      '</div>';

    /* 考据正文（在角色卡内） */
    var reading = (r.sections || []).map(function (s) {
      var paras = s.p == null ? [] : (Array.isArray(s.p) ? s.p : [s.p]);
      return '<div class="rd-s"><h4 class="rd-h">' + esc(s.h) + '</h4>' +
        paras.map(function (p) { return '<p class="rd-p">' + esc(p) + '</p>'; }).join('') +
      '</div>';
    }).join('');

    return '' +
      '<article class="chara" style="--fc:' + fc + '">' +
        noHtml +
        '<div class="chara-fig">' +
          picHtml(c) +
          '<button class="mn-btn mn-btn--round chara-zoom" type="button" aria-label="放大立绘">' +
            ARROW +
          '</button>' +
        '</div>' +
        '<div class="chara-body">' +
          metaHtml +
          '<h3 class="chara-name">' + esc(c.name) + '</h3>' +
          cvHtml +
          roleLine +
          descHtml +
          '<div class="chara-ops">' +
            '<div class="chara-voice">' +
              '<button class="mn-btn mn-btn--voice" type="button">' +
                '<img src="' + A + 'chara_voice.CRMOMoGV.svg" alt="" aria-hidden="true">通常' +
              '</button>' +
              '<button class="mn-btn mn-btn--voice" type="button">' +
                '<img src="' + A + 'chara_voice.CRMOMoGV.svg" alt="" aria-hidden="true">特殊' +
              '</button>' +
            '</div>' +
            /* 考据按钮：默认收起，点开 */
            '<button class="mn-btn mn-btn--read" type="button" data-read="' + esc(c.name) + '">' +
              '<span>查看佛学解读</span>' + ARROW +
            '</button>' +
          '</div>' +
          '<div class="chara-reading" id="rd-' + esc(c.name) + '">' + reading + '</div>' +
        '</div>' +
      '</article>';
  }

  /* 立绘：桌面用 PC 高清版，移动用 SP 版（与官方 srcset 逻辑一致） */
  function picHtml(c) {
    var sp = c.img;
    var key = sp.replace(/\.[A-Za-z0-9_\-]+\.webp$/, '');
    var pc = (typeof CHARA_IMG_PC !== 'undefined') ? CHARA_IMG_PC[key] : null;

    if (pc) {
      return '<picture>' +
        '<source srcset="' + A + pc + '" media="(min-width: 835px)">' +
        '<img src="' + A + sp + '" alt="' + esc(c.name) + '" loading="lazy">' +
      '</picture>';
    }
    return '<img src="' + A + sp + '" alt="' + esc(c.name) + '" loading="lazy">';
  }

    /* ═══ 楼层插图区：小图 + 该层全部考据 ═══ */
  function renderIllus(f) {
    if (typeof ILLUSTRATIONS === 'undefined') return '';
    var list = ILLUSTRATIONS[f.id];
    if (!list || !list.length) return '';

    var items = list.map(function (im) {
      return '<figure class="illus-item" data-src="' + A + 'illus/' + im.src + '">' +
        '<img src="' + A + 'illus/' + im.src + '" alt="' + esc(f.floorName) + ' 插图" ' +
        'decoding="async">' +
      '</figure>';
    }).join('');

    var floorTxt = f.id === 'sovereign' ? '监狱统治者' : '第' + CN[f.floor] + '层“' + f.floorName + '”';
    var names = f.chars.map(function (c) { return c.name; }).join(' · ');

    return '<div class="illus">' +
      '<div class="illus-row">' + items +
        '<div class="illus-meta">' +
          '<div class="illus-cap">' + esc(floorTxt) + '</div>' +
          '<div class="illus-pair">' + esc(f.pairTitle) + '</div>' +
          '<div class="illus-note">' + esc(names) + '</div>' +
        '</div>' +
      '</div>' +
    '</div>';
  }

  /* ═══ 整层 ═══ */
  function renderPair(f) {
    var fc = FACTIONS[f.chars[0].faction].color;
    var floorTxt = f.id === 'sovereign' ? '监狱统治者' : '第' + CN[f.floor] + '层“' + f.floorName + '”';
    var names = f.chars.map(function (c) { return c.name; }).join(' ⟷ ');

    var chars = f.chars.map(function (c) { return renderChar(c, fc, f.id); }).join('');

    var match = '';
    if (f.chars.length === 2) {
      var a = f.chars[0], b = f.chars[1];
      match =
        '<div class="match">' +
          '<div class="match-k">本层对位 · ' + esc(f.pairTitle) + '</div>' +
          '<div class="match-pair">' +
            '<div class="ms ms--a">' +
              '<div class="ms-name">' + esc(a.name) + '</div>' +
              '<span class="ms-role">' + esc(a.reading.role) + '</span>' +
              '<div class="ms-proto">' + esc(a.reading.proto.split('——')[0].trim()) + '</div>' +
            '</div>' +
            '<div class="ms-vs">⟷</div>' +
            '<div class="ms ms--b">' +
              '<div class="ms-name">' + esc(b.name) + '</div>' +
              '<span class="ms-role">' + esc(b.reading.role) + '</span>' +
              '<div class="ms-proto">' + esc(b.reading.proto.split('——')[0].trim()) + '</div>' +
            '</div>' +
          '</div>' +
        '</div>';
    }

    return '' +
      '<section class="pair" id="pair-' + f.id + '" style="--fc:' + fc + '">' +
        '<div class="pair-hd">' +
          '<img class="pair-floor" src="' + A + FLOOR_IMG[f.floor] + '" alt="" loading="lazy">' +
          '<div class="pair-ttl">' +
            '<div class="pair-fl">' + esc(floorTxt) + '</div>' +
            '<h2 class="pair-name">' + esc(floorTxt) + '</h2>' +
            '<p class="pair-proto">' + esc(f.pairTitle) + '</p>' +
          '</div>' +
          '<div class="pair-no">' + esc(names) + '</div>' +
        '</div>' +
        renderIllus(f) +
        chars +
        match +
      '</section>';
  }

  function renderPairs() {
    $('#pairsBody').innerHTML = FLOOR_ORDER.map(function (fid) {
      return renderPair(DATA.find(function (d) { return d.id === fid; }));
    }).join('');
  }

  /* ═══ 附录 ═══ */
  function renderAppendix() {
    var sov = DATA.find(function (d) { return d.id === 'sovereign'; });
    if (!sov) return;
    var r = sov.chars[0].reading;

    var sections = (r.sections || []).map(function (s) {
      var paras = s.p == null ? [] : (Array.isArray(s.p) ? s.p : [s.p]);
      var ps = paras.map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('');
      var q = s.quote ? '<blockquote class="src"><p>' + esc(s.quote) + '</p></blockquote>' : '';
      return '<h3 class="h3">' + esc(s.h) + '</h3>' + ps + q;
    }).join('');

    $('#appendixBody').innerHTML = '<p class="lead">' + esc(r.summary) + '</p>' + sections;
  }

  /* ═══ 立绘放大（官方圆钮行为） ═══ */
  function initZoom() {
    $$('.chara-zoom').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var img = btn.parentElement.querySelector('img');
        if (!img) return;
        img.classList.toggle('is-zoomed');
      });
    });
  }

  /* ═══ 考据折叠 ═══ */
  function initReadToggle() {
    $$('[data-read]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var box = document.getElementById('rd-' + btn.dataset.read);
        if (!box) return;
        var open = box.classList.toggle('is-open');
        btn.classList.toggle('is-on', open);
        var label = btn.querySelector('span');
        if (label) label.textContent = open ? '收起解读' : '查看佛学解读';
      });
    });
  }

  

  /* ═══ 插图灯箱 ═══ */
  function initLightbox() {
    var lb = $('#lightbox');
    if (!lb) return;
    var lbImg = $('#lbImg');
    var lbCap = $('#lbCap');

    function open(src, cap) {
      lbImg.src = src;
      lbCap.textContent = cap || '';
      lb.classList.add('is-open');
      lb.setAttribute('aria-hidden', 'false');
      document.documentElement.style.overflow = 'hidden';
    }
    function close() {
      lb.classList.remove('is-open');
      lb.setAttribute('aria-hidden', 'true');
      document.documentElement.style.overflow = '';
    }

    $$('.illus-item').forEach(function (it) {
      it.addEventListener('click', function () {
        var img = it.querySelector('img');
        open(it.dataset.src, img ? img.alt : '');
      });
    });

    $('#lbClose').addEventListener('click', close);
    lb.addEventListener('click', function (e) {
      if (e.target === lb || e.target.parentElement === lb) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && lb.classList.contains('is-open')) close();
    });
  }

  /* ═══ 启动 ═══ */
  initSwitch();
  buildNav();
  renderPairs();
  renderAppendix();
  initZoom();
  initReadToggle();
  initLightbox();
})();