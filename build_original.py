#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
以官方页面真实快照为底座，注入「月轮观」解读浮层。
产出：site/original/index.html  +  assets/（原站资源本地化）
"""
import re, os, shutil, html as H

BASE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(BASE, '_extract')
OUT = os.path.join(BASE, 'original')
ASSETS = os.path.join(OUT, 'assets')

os.makedirs(ASSETS, exist_ok=True)

raw = open(os.path.join(EXT, '00.html'), encoding='utf-8', errors='replace').read()

# ── 1. 复制原站 CSS ────────────────────────────────
for css in ['02.css', '08.css']:
    src = os.path.join(EXT, css)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(ASSETS, f'orig_{css}'))

# ── 2. 资源本地化：远端 URL → assets/ ───────────────
REMOTE = re.compile(r'https://revenants-of-azvaldt\.shadowverse-wb\.com/_app/immutable/assets/([A-Za-z0-9_.\-]+\.(?:webp|png|jpg|svg|mp4))')

def localize(m):
    fn = m.group(1)
    src_m = re.match(r'(.+?)\.[A-Za-z0-9_]{8}\.(webp|png|jpg|svg|mp4)$', fn)
    return f'assets/{fn}'

html_out = REMOTE.sub(localize, raw)

# 根相对路径（srcset="/_app/immutable/assets/xxx.webp"）→ assets/xxx.webp
html_out = re.sub(r'(/_app/immutable/assets/)([A-Za-z0-9_.\-]+\.(?:webp|png|jpg|svg|mp4))', r'assets/\2', html_out)

# movies 目录下的视频/海报 → assets/（文件名已下载到 assets）
html_out = re.sub(
    r'https://revenants-of-azvaldt\.shadowverse-wb\.com/movies/([A-Za-z0-9_.\-]+\.(?:png|mp4|webm))',
    r'assets/\1', html_out)
# cid: 样式表引用替换
html_out = html_out.replace('href="cid:css-ab44c383-4c70-4744-94af-a6f53da64ec1@mhtml.blink"', 'href="assets/orig_02.css"')
html_out = html_out.replace('href="cid:css-99f8cbcc-8f25-4644-9f99-6d1acfaf90e6@mhtml.blink"', 'href="assets/orig_08.css"')
html_out = html_out.replace('href="cid:css-170a37ae-0e09-4d04-8954-2e779dc02fd4@mhtml.blink"', 'href="assets/appendix.css"')
html_out = html_out.replace('href="cid:css-p45w96', 'href="assets/orig_08.css"')
# 外部字体（parts.cygames / shadowverse-wb / onetrust）本地化或移除
html_out = re.sub(r'<link[^>]*parts\.cygames\.co\.jp[^>]*>', '', html_out)
html_out = re.sub(r'<link[^>]*shadowverse-wb\.com/assets/css[^>]*>', '', html_out)
html_out = re.sub(r'<link[^>]*fonts\.googleapis\.com[^>]*>', '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">', html_out)
html_out = re.sub(r'<link[^>]*fonts\.gstatic\.com[^>]*>', '', html_out)

# ── 3. 移除 OneTrust Cookie 弹层（占位资源已失效）──
html_out = re.sub(r'<div[^>]*id="onetrust-consent-sdk"[\s\S]*?</div>\s*</div>', '', html_out)
html_out = re.sub(r'<div id="ot-sdk-container"[\s\S]*?</div>\s*</div>', '', html_out)

# ── 4. 移除指向线上/已失效的外链资源 ───────────────
html_out = re.sub(r'<img[^>]*cdn-au\.onetrust\.com[^>]*>', '', html_out)

# ── 4b. 清除 SvelteKit 运行时（快照中已失效，且会与注入脚本冲突）──
# modulepreload / importmap / data-sveltekit
html_out = re.sub(r'<link[^>]*rel="modulepreload"[^>]*>', '', html_out)
html_out = re.sub(r'<link[^>]*rel="importmap"[^>]*>', '', html_out)
# VideoOptimization / 0. / preload 三份站点 CSS：用原站快照内的 CSS 替代
# （这些 link 标签在快照中属性可能不带引号，统一用正则按 URL 定位）
def _swap_css(match):
    url = match.group(0)
    if 'VideoOptimization' in url:
        return 'assets/orig_video.css'
    if 'preload.' in url:
        return 'assets/empty.css'
    if re.search(r'/0\.[A-Za-z0-9_]{8}\.css', url):
        return 'assets/empty.css'
    return url

html_out = re.sub(r'https://revenants-of-azvaldt\.shadowverse-wb\.com/_app/immutable/assets/[A-Za-z0-9_.\-]+\.css', _swap_css, html_out)
# 站点内其它语言链接与 favicon 保留（无害），但 /chs/ 自引用改为 #
html_out = html_out.replace('https://revenants-of-azvaldt.shadowverse-wb.com/chs/', '#')

# ── 5. 写入原站 HTML（浮层容器随后注入）───────────
open(os.path.join(OUT, '_base.html'), 'w', encoding='utf-8').write(html_out)

print('base html bytes:', len(html_out.encode('utf-8')))
print('assets dir:', ASSETS)