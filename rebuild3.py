#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按《无标题.txt》原文出场顺序重建八对 → 官方楼层的映射。

原文顺序（脚本已核实）：
  第一对：罗刹与明王        → 伽罗塔德/泽特        → 八层「蛇殿」
  第二对：求道者与至善者    → 赛菲/菲绫            → 五层「破式」
  第三对：行恶者与行善者    → 巴巴洛丝/贝尔铁佐    → 七层「武皇」
  第四对：理想者与不理想者  → 卡特斯罗特/艾兹伊甸  → 一层「弹哭」
  第五对：他人者与断桥者    → 安缇马丽亚/诺玛格达拉→ 二层「禁牙」
  第七对：自卑者与无条件相信者→ 艾尔拉德/奥梅里欧  → 六层「翼天」
  第七对：延长寿命者与求死者  → 玛尔奇盖特/伊斯坦戴德→ 三层「灭尸」
  第八对：继承者与求死者      → 曲千代/飞燕         → 四层「香风」
  最后：监狱统治者            → 泽勒尔              → 监狱统治者
"""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = r'C:\Users\Administrator\Desktop\无标题.txt'
OUT = os.path.join(BASE, 'original', 'data.js')

L = io.open(SRC, encoding='utf-8').read().split('\n')
src_norm = re.sub(r'\s+', '', io.open(SRC, encoding='utf-8').read())

def G(a, b):
    return [L[i].strip() for i in range(a - 1, min(b, len(L))) if L[i].strip()]

def S(t, ps):
    return {'h': t, 'p': ps}

RM, TM = '修满月者', '天魔'

# ═════════ 原文素材（按原文行号）═════════

# 第一对（L48-113）：伽罗塔德 / 泽特
P1_GARO = [
    S('央掘魔罗是谁？', G(86, 90)),
    S('入场语音（“月輪”）：', [G(66, 66)[0]]),
    S('进化语音（“光明”）：', [G(68, 68)[0]]),
    S('“破蛇（はじゃ）”与“破邪”的音义双关', G(72, 74)),
]
P1_ZET = [
    S('释迦牟尼佛做了什么？', G(98, 106) + [G(110, 110)[0]]),
]

# 第二对（L115-188）：赛菲 / 菲绫
P2_SEFI = [
    S('大黑天是谁？', G(150, 154)),
    S('大黑天是修满月者。', G(173, 173) + G(185, 185)),
    S('“烏ノ涅”与“鵠ノ白煉”', G(124, 135)),
    S('这代表什么', G(136, 138)),
]
P2_FEILIN = [
    S('白玛哈嘎拉是谁？', G(162, 169)),
    S('白玛哈嘎拉是至善者（天魔）。', G(177, 181)),
]

# 第三对（L190-243）：巴巴洛丝 / 贝尔铁佐
P3_BAR = [
    S('文殊菩萨是谁？', G(208, 212)),
    S('对应关系：', G(232, 240)),
]
P3_BEL = [
    S('普贤菩萨是谁？', G(220, 224)),
    S('对应关系：', G(232, 240)),
]

# 第四对（L245-297）：卡特斯罗特 / 艾兹伊甸
P4_KATO = [
    S('维摩诘是谁？', G(275, 283)),
    S('对应关系：', G(291, 295)),
]
P4_EDEN = [
    S('舍利弗是谁？', G(263, 267)),
    S('对应关系：', G(291, 295)),
]

# 第五对（L303-373）：安缇马丽亚 / 诺玛格达拉
P5_ANTI = [
    S('阿难是谁？', G(343, 351)),
    S('对应关系', [G(371, 371)[0]]),
]
P5_NOMA = [
    S('经典里有一个比喻，叫无明壳', G(313, 321)),
    S('但《大般涅槃经》还说了一句话：', G(329, 333)),
    S('摩诃迦叶是谁？', G(359, 367)),
    S('对应关系', [G(371, 371)[0]]),
]

# 第七对（L377-459）：艾尔拉德 / 奥梅里欧
P6_ERU = [
    S('提婆达多是谁？', G(393, 401)),
    S('他做了什么？', G(437, 437)),
    S('对应关系：', G(445, 449)),
]
P6_OME = [
    S('释迦牟尼佛是谁？', G(409, 413)),
    S('对应关系：', G(449, 457)),
]

# 第七对（L462-502）：玛尔奇盖特 / 伊斯坦戴德
P7_MARG = [
    S('善星比丘是谁？', G(490, 490)),
    S('对应关系：', G(498, 502)),
]
P7_IST = [
    S('地藏菩萨是谁？', G(478, 482)),
    S('对应关系：', G(498, 498)),
]

# 第八对（L504-546）：曲千代 / 飞燕
P8_TOYO = [
    S('频婆娑罗王是谁？', G(532, 540)),
    S('对应关系：', [G(544, 544)[0]]),
]
P8_TOBI = [
    S('地藏菩萨是谁？', G(520, 524)),
    S('对应关系：', [G(544, 544)[0]]),
]

# 监狱统治者（L548-573）
P9_ZER = [
    S('监狱崩溃，诅咒消散', [G(553, 553)[0]]),
    S('帝释天', G(557, 559)),
    S('变貌', G(562, 567)),
    S('关于他的死', G(569, 573)),
]

# ═════════ 楼层顺序 = 官方原站顺序 ═════════
# (id, 层号, 层名, 对序标题, [(角色, 阵营, 声优, 编号, 图, 位分, 原型, 剧情区间, 小节)])
FLOORS = [
    ('sovereign', 0, '监狱统治者', '最后：监狱统治者', [
        ('泽勒尔', 'neutral', '井上和彦', '—', 'chara0_img1.Dyi3hmXN.webp',
         RM, '帝释天', (550, 553), P9_ZER),
    ]),
    # 一层 弹哭 = 第四对
    ('stratum-1', 1, '弹哭', '第四对：理想者与不理想者', [
        ('卡特斯罗特', 'nemesis', '花江夏树', '囚犯编号：B-4234-44HE42',
         'chara1_img1.DspFYMts.webp', RM, '维摩诘', (249, 251), P4_KATO),
        ('艾兹伊甸', 'nemesis', '冈本信彦', '识别编号：42E-23-4434RB',
         'chara1_img2.BOJJdEyq.webp', TM, '舍利弗', (253, 253), P4_EDEN),
    ]),
    # 二层 禁牙 = 第五对
    ('stratum-2', 2, '禁牙', '第五对：他人者与断桥者', [
        ('安缇马丽亚', 'dragon', '佐仓绫音', '囚犯编号：F-42-IE3314',
         'chara2_img1.DieXgygq.webp', RM, '阿难', (305, 309), P5_ANTI),
        ('诺玛格达拉', 'dragon', 'Lynn', '识别编号：14N-15-2442F',
         'chara2_img2.D05tXWoe.webp', TM, '摩诃迦叶', None, P5_NOMA),
    ]),
    # 三层 灭尸 = 第七对（延长寿命者与求死者）
    ('stratum-3', 3, '灭尸', '第七对：延长寿命者与求死者', [
        ('玛尔奇盖特', 'nightmare', '咲川雏乃', '识别编号：22N-24-3112IS',
         'chara3_img1.Cm_CaooI.webp', TM, '善星比丘', None, P7_MARG),
        ('伊斯坦戴德', 'nightmare', '三木真一郎', '囚犯编号：S-2412-LI3322',
         'chara3_img1.Cm_CaooI.webp', RM, '地藏菩萨', (464, 468), P7_IST),
    ]),
    # 四层 香风 = 第八对
    ('stratum-4', 4, '香风', '第八对：继承者与求死者', [
        ('曲千代', 'elf', '川澄绫子', '囚犯编号：M-34-T231542',
         'chara4_img1.D4aLn6xF.webp', TM, '频婆娑罗王', (506, 508), P8_TOYO),
        ('飞燕', 'elf', '铃木达央', '识别编号：33O-24-13S',
         'chara4_img2.CwDQ7q6N.webp', RM, '地藏菩萨', (510, 510), P8_TOBI),
    ]),
    # 五层 破式 = 第二对
    ('stratum-5', 5, '破式', '第二对：求道者与至善者', [
        ('赛菲', 'witch', '水濑祈', '囚犯编号：S-24-ST1542',
         'chara5_img1.6W2FK87L.webp', RM, '大黑天', (118, 122), P2_SEFI),
        ('菲绫', 'witch', '大西沙织', '识别编号：42E-44-4324S',
         'chara5_img2.BdAHZjMc.webp', TM, '白玛哈嘎拉', None, P2_FEILIN),
    ]),
    # 六层 翼天 = 第七对（自卑者与无条件相信者）
    ('stratum-6', 6, '翼天', '第七对：自卑者与无条件相信者', [
        ('艾尔拉德', 'bishop', '石田彰', '囚犯编号：P-1142-TN1542',
         'chara6_img1.CfHEq4Ot.webp', RM, '提婆达多', (379, 383), P6_ERU),
        ('奥梅里欧', 'bishop', '关智一', '识别编号：42E-33-4442AP',
         'chara6_img2.BPAW21ba.webp', TM, '释迦牟尼佛', None, P6_OME),
    ]),
    # 七层 武皇 = 第三对
    ('stratum-7', 7, '武皇', '第三对：行恶者与行善者', [
        ('巴巴洛丝', 'royal', '悠木碧', '囚犯编号：D-114522-HT1542',
         'chara7_img1.HroMp0Vm.webp', RM, '文殊菩萨', (192, 194), P3_BAR),
        ('贝尔铁佐', 'royal', '佐藤拓也', '识别编号：42E-23-4411F',
         'chara7_img2.D6xbROoZ.webp', TM, '普贤菩萨', (196, 196), P3_BEL),
    ]),
    # 八层 蛇殿 = 第一对
    ('stratum-8', 8, '蛇殿', '第一对：罗刹与明王', [
        ('伽罗塔德', 'nightmare', '木村良平', '囚犯编号：D-244313-IP3115',
         'chara8_img1.BYgBZQS0.webp', RM, '央掘魔罗', (53, 64), P1_GARO),
        ('泽特', 'nightmare', '安元洋贵', '识别编号：42E-44-4311M',
         'chara8_img1.BYgBZQS0.webp', TM, '释迦牟尼佛', None, P1_ZET),
    ]),
]

def q(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"

o = []
o.append('// 八狱角色 · 解读数据')
o.append('// 文字全部摘自《无标题.txt》原文，未作增删改写')
o.append('// 位分仅两种：修满月者 / 天魔（依原文「对应关系」判断）')
o.append('// 楼层顺序 = 官方原站顺序；对序标题 = 原文对应段落')
o.append('')
o.append('const PROLOGUE = {')
o.append("  title: '月轮观',")
o.append("  subtitle: '缺月与满月',")
o.append('  blocks: [')
o.append(f"    {{ type: 'lead', text: {q(G(1,1)[0])} }},")
o.append(f"    {{ type: 'moon', left: '缺月', right: '满月', note: {q(G(5,5)[0])} }},")
o.append(f"    {{ type: 'p', text: {q(G(7,7)[0])} }},")
o.append(f"    {{ type: 'q', text: {q(G(10,10)[0])} }},")
o.append("    { type: 'h', text: '四魔' },")
o.append(f"    {{ type: 'p', text: {q(G(14,14)[0])} }},")
o.append("    { type: 'h', text: '他化自在天' },")
o.append(f"    {{ type: 'p', text: {q(G(18,18)[0])} }},")
o.append(f"    {{ type: 'p', text: {q(G(22,22)[0])} }},")
o.append(f"    {{ type: 'quote', src: '大般涅槃经', text: {q(G(26,26)[0])} }},")
o.append(f"    {{ type: 'p', text: {q(G(30,30)[0])} }},")
o.append(f"    {{ type: 'h', text: {q(G(32,32)[0])} }},")
o.append(f"    {{ type: 'p', text: {q(G(36,36)[0])} }},")
o.append(f"    {{ type: 'q', text: {q(G(40,40)[0])} }},")
o.append(f"    {{ type: 'p', text: {q(G(43,43)[0])} }},")
o.append('  ],')
o.append("  pairs_intro: '接下来的八对，是这座监狱里全部的相遇。每一对都是一次照见。',")
o.append('};')
o.append('')
o.append('const DATA = [')
for i, (pid, fl, fn, pt, chars) in enumerate(FLOORS):
    o.append('  {')
    o.append(f"    id: {q(pid)},")
    o.append(f"    floor: {fl},")
    o.append(f"    floorName: {q(fn)},")
    o.append(f"    pairTitle: {q(pt)},")
    o.append('    chars: [')
    for name, fac, cv, no, img, role, proto, rng, secs in chars:
        o.append('      {')
        o.append(f"        name: {q(name)},")
        o.append(f"        faction: {q(fac)},")
        o.append(f"        cv: {q(cv)},")
        o.append(f"        no: {q(no)},")
        o.append(f"        img: {q(img)},")
        o.append(f"        role: {q(role)},")
        o.append(f"        proto: {q(proto)},")
        o.append('        reading: {')
        o.append(f"          title: {q(name + ' · ' + proto)},")
        o.append(f"          role: {q(role)},")
        o.append(f"          proto: {q(proto)},")
        o.append('          sections: [')
        for s in secs:
            o.append('            {')
            o.append(f"              h: {q(s['h'])},")
            o.append(f"              p: [{', '.join(q(x) for x in s['p'])}],")
            o.append('            },')
        o.append('          ],')
        o.append('        },')
        o.append('      },')
    o.append('    ],')
    o.append('  },')
    if i < len(FLOORS) - 1:
        o.append('')
o.append('];')
o.append('')
o.append("const FLOOR_ORDER = ['sovereign', 'stratum-1', 'stratum-2', 'stratum-3', 'stratum-4', 'stratum-5', 'stratum-6', 'stratum-7', 'stratum-8'];")
o.append('')
o.append('const FLOOR_IMG = {')
o.append("  0: 'floor0.IjgHsuQq.webp', 1: 'floor1.DAaEa2Tq.webp', 2: 'floor2.1_8-Wg1x.webp',")
o.append("  3: 'floor3.nqMhQzY0.webp', 4: 'floor4.B_EfjANZ.webp', 5: 'floor5.DKFfAQlE.webp',")
o.append("  6: 'floor6.CQHsZiaO.webp', 7: 'floor7.Dcr-ZNJN.webp', 8: 'floor8.BO67vXJ_.webp',")
o.append('};')
o.append('')
o.append('const FACTIONS = {')
o.append("  neutral:   { label: '中立',     color: '#aebdc0' },")
o.append("  nemesis:   { label: '超越者',   color: '#90ddde' },")
o.append("  dragon:    { label: '龙族',     color: '#c6966b' },")
o.append("  nightmare: { label: '梦魇',     color: '#ff90b4' },")
o.append("  elf:       { label: '精灵',     color: '#aada75' },")
o.append("  witch:     { label: '巫师',     color: '#a3aeff' },")
o.append("  bishop:    { label: '主教',     color: '#d2ceae' },")
o.append("  royal:     { label: '皇家护卫', color: '#c3c261' },")
o.append('};')
o.append('')
o.append('const PROFILE_IMG = {')
o.append("  neutral: 'chara_profile_neutral.BHc-nmGW.webp', nemesis: 'chara_profile_nemesis.BNmsEHLA.webp',")
o.append("  dragon: 'chara_profile_dragon.CQdfXIiS.webp', nightmare: 'chara_profile_nightmare.DrO1RG1U.webp',")
o.append("  elf: 'chara_profile_elf.BUqA3AU-.webp', witch: 'chara_profile_witch.ae9VqKtv.webp',")
o.append("  bishop: 'chara_profile_bishop.By0RUAY0.webp', royal: 'chara_profile_royal.C3T9fuYc.webp',")
o.append('};')

io.open(OUT, 'w', encoding='utf-8').write('\n'.join(o) + '\n')
print('已按原文顺序重建 data.js')

newtxt = io.open(OUT, encoding='utf-8').read()
miss = []
for m in re.finditer(r"'((?:[^'\\]|\\.){6,})'", newtxt):
    s = m.group(1).replace("\\'", "'").replace('\\\\', '\\')
    sn = re.sub(r'\s+', '', s)
    fr = re.findall(r'[\u4e00-\u9fff]{8,}', sn)
    if not fr:
        continue
    fr.sort(key=len, reverse=True)
    if fr[0] not in src_norm:
        miss.append(s[:60])
print(f'无法在原文定位：{len(miss)} 处')
for x in miss:
    print('   ', x)
# 追加阵营纹章映射
with open(OUT, 'a', encoding='utf-8') as f:
    f.write("""

// 阵营纹章（用于楼层导航）
const CHARA_BTN = {
  neutral:   'chara_btn_neutral.B_CFxn4T.webp',
  nemesis:   'chara_btn_nemesis.5hprusFm.webp',
  dragon:    'chara_btn_dragon.DXdfiMUI.webp',
  nightmare: 'chara_btn_nightmare.BQqtiSNj.webp',
  elf:       'chara_btn_elf.jiOl42mu.webp',
  witch:     'chara_btn_witch.B5U1vHYu.webp',
  bishop:    'chara_btn_bishop.DdCHUEHR.webp',
  royal:     'chara_btn_royal.cxh8PZrR.webp',
};
""")
print('已追加 CHARA_BTN')
