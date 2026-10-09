#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把「月轮观」解读浮层注入官方页面快照。

策略：不重排原站 DOM，只做三处最小侵入
  1) </body> 前插入浮层容器 + 脚本
  2) 每个角色条目内追加「佛学解读」按钮（运行时由 JS 定位并插入，零侵入）
  3) 追加 appendix.css 覆盖样式
"""
import re, os, json

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'original')
html = open(os.path.join(OUT, '_base.html'), encoding='utf-8').read()

# ── 注入浮层容器 ────────────────────────────────────
OVERLAY = '''
<!-- ═══════ 月轮观解读浮层（注入） ═══════ -->
<div id="moonOverlay" class="mn-overlay" aria-hidden="true">
  <div class="mn-backdrop" data-mn-close></div>
  <aside class="mn-panel" role="dialog" aria-modal="true" aria-labelledby="mnTitle">
    <button class="mn-close" data-mn-close aria-label="关闭解读">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4l16 16M20 4L4 20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    </button>
    <div class="mn-scroll">
      <div class="mn-hero">
        <img class="mn-hero-img" id="mnHeroImg" src="" alt="">
        <div class="mn-hero-veil"></div>
        <div class="mn-hero-text">
          <div class="mn-badges" id="mnBadges"></div>
          <h2 class="mn-title" id="mnTitle"></h2>
          <p class="mn-proto" id="mnProto"></p>
        </div>
      </div>
      <div class="mn-body" id="mnBody"></div>
    </div>
  </aside>
</div>

<!-- 悬浮入口 -->
<button id="mnFab" class="mn-fab" aria-label="打开月轮观解读">
  <span class="mn-fab-orb" aria-hidden="true"></span>
  <span class="mn-fab-label">月轮观</span>
</button>

<!-- 阅读进度侧栏 -->
<nav id="mnRail" class="mn-rail" aria-label="楼层导航"></nav>
'''

SCRIPTS = '''
<script src="data.js?v=3"></script>
<script src="moon-overlay.js?v=3"></script>
</body>'''

if 'id="moonOverlay"' not in html:
    html = html.replace('</body>', OVERLAY + SCRIPTS, 1)

open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)
print('index.html written:', len(html.encode('utf-8')))