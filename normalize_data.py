#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 data.js 中 sections 里连续的多个 `p: '...'` 合并为数组 `p: ['...', '...']`，
使数据结构统一为数组形式。
"""
import re, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'original', 'data.js')
src = open(P, encoding='utf-8').read()
lines = src.split('\n')

# 定位 sections 区域（仅处理 reading.sections）
# 策略：扫描所有形如 `p: '...'` 的行，若紧随其后（忽略空白）仍是 `p: '...'`，则合并
out = []
i = 0
merged = 0
n_merged_lines = 0

P_LINE = re.compile(r"^(\s*)p:\s*'((?:[^'\\]|\\.)*)'\s*,?\s*$")

while i < len(lines):
    m = P_LINE.match(lines[i])
    if not m:
        out.append(lines[i])
        i += 1
        continue

    indent, first = m.group(1), m.group(2)
    # 收集连续的所有 p: 行
    group = [first]
    j = i + 1
    while j < len(lines):
        m2 = P_LINE.match(lines[j])
        if m2 and m2.group(1) == indent:
            group.append(m2.group(2))
            j += 1
        else:
            break

    if len(group) == 1:
        out.append(lines[i])
    else:
        merged += 1
        n_merged_lines += len(group) - 1
        body = (',\n' + indent + ' ').join("'%s'" % g for g in group)
        out.append(f"{indent}p: [{body}],")
    i = j

open(P, 'w', encoding='utf-8').write('\n'.join(out))
print(f"合并了 {merged} 组，共减少 {n_merged_lines} 行")

# 复验
src2 = open(P, encoding='utf-8').read()
strs = len(re.findall(r"^\s*p:\s*'", src2, re.M))
arrs = len(re.findall(r"^\s*p:\s*\[", src2, re.M))
print("剩余字符串 p:", strs, "| 数组 p:", arrs)