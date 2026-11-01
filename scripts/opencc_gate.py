#!/usr/bin/env python3
"""第二道閘：OpenCC 逐行候選偵測（tw-chinese-copywriting v2.5.0 起）。
參考來源：BYVoid/OpenCC（https://github.com/BYVoid/OpenCC ，Apache-2.0）。

usage: opencc_gate.py <檔案> [--vocab]
  預設用 -c s2t（STPhrases+STCharacters）：命中＝簡體字形/簡體詞候選。
  --vocab 用 -c s2twp：另外命中「繁體正確但大陸用語」的詞彙建議（僅供參考）。
exit: 0=無候選, 1=有候選, 2=執行錯誤。

鐵則：只列候選，絕不自動改全文。已知誤報型（依語境判斷）：
  台→臺（舞台/台階合法）、核→覈（查核合法）、才→纔（副詞「才」合法）、裡/里（里程合法）。
"""
import os, subprocess, sys

AMBIG = set('台才了里后只别并着装东面干发愿效借沈范复')
# 兩用字：兩邊都合法，只能依語境判斷。清單來自本 skill 實際誤發紀錄，可擴充。

def load_charmap():
    p = os.path.join(os.path.dirname(__file__), '..', 'references', 's2t-chars.tsv')
    m = {}
    with open(p, encoding='utf-8') as f:
        for line in f:
            a, _, b = line.partition('\t')
            if a and b:
                m[a] = b.strip()
    return m

def fallback_scan(lines, cmap):
    hits = 0
    for i, ln in enumerate(lines, 1):
        found = [ch for ch in ln if ch in cmap]
        if not found:
            continue
        hits += 1
        pure = ''.join(dict.fromkeys(c for c in found if c not in AMBIG))
        amb = ''.join(dict.fromkeys(c for c in found if c in AMBIG))
        tags = []
        if pure:
            tags.append(f'純簡體字[{pure}]')
        if amb:
            tags.append(f'兩用字[{amb}](依語境判斷)')
        print(f'L{i} ' + ' '.join(tags))
        print(f'  原文: {ln[:90]}')
    return hits

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    path = sys.argv[1]
    cfg = 's2twp' if '--vocab' in sys.argv else 's2t'
    lines = open(path, encoding='utf-8').read().splitlines()
    try:
        r = subprocess.run(['opencc', '-c', cfg], input='\n'.join(lines),
                           capture_output=True, text=True)
    except FileNotFoundError:
        # 沒有 opencc 二進位（未安裝的機器）：降級為純 Python 字形表掃描
        print(f'-- mode: fallback（{load_charmap().__len__()} 字表，無詞保護，'
              f'候測一律人工判斷）')
        hits = fallback_scan(lines, load_charmap())
        print(f'-- fallback: {hits} 行候選')
        return 1 if hits else 0
    if r.returncode != 0:
        print('opencc 失敗:', r.stderr.strip()); return 2
    conv = r.stdout.splitlines()
    hits = 0
    for i, (a, b) in enumerate(zip(lines, conv), 1):
        if a != b:
            hits += 1
            diff = ''.join(sorted(set(b) - set(a)))
            print(f'L{i} 新增字形[{diff}]')
            print(f'  原文: {a[:90]}')
    print(f'-- {cfg}: {hits} 行候選')
    return 1 if hits else 0

if __name__ == '__main__':
    sys.exit(main())
