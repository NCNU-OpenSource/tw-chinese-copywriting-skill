#!/usr/bin/env python3
"""第二道閘：OpenCC 逐行候選偵測（tw-chinese-copywriting v2.5.0 起）。

usage: opencc_gate.py <檔案> [--vocab]
  預設用 -c s2t（STPhrases+STCharacters）：命中＝簡體字形/簡體詞候選。
  --vocab 用 -c s2twp：另外命中「繁體正確但大陸用語」的詞彙建議（僅供參考）。
exit: 0=無候選, 1=有候選, 2=執行錯誤。

鐵則：只列候選，绝不自動改全文。已知誤報型（依語境判斷）：
  台→臺（舞台/台階合法）、核→覈（查核合法）、裡/里（里程合法）。
"""
import subprocess, sys

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    path = sys.argv[1]
    cfg = 's2twp' if '--vocab' in sys.argv else 's2t'
    lines = open(path, encoding='utf-8').read().splitlines()
    r = subprocess.run(['opencc', '-c', cfg], input='\n'.join(lines),
                       capture_output=True, text=True)
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
