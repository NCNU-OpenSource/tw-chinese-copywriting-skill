#!/usr/bin/env python3
"""第三道閘：排版與詞層候測（借 zhtw-mcp 的規則分類架構，純 stdlib，零依賴）。
參考來源：sysprog21/zhtw-mcp（https://github.com/sysprog21/zhtw-mcp ，MIT，
規則分類借鑑，未引入該工具）；邊界空格規則源頭 sparanoid/typesetting-guidelines。

usage: style_gate.py <檔案>
exit: 0=無候選, 1=有候選, 2=執行錯誤。

檢查類別（皆為候測，由人判斷，絕不自動改）：
  1. 半形標點緊貼中文（，。：；？！應用全形）
  2. 標點在地化（“ ” ‘ ’ 直排引號→建議「」『』）
  3. CJK 與拉丁/數字邊界缺空格（排版指北）
  4. 專名 casing（github→GitHub 這類）
  5. 政治色彩詞（依語境）
  6. 高信心 AI 腔填充語
遮蔽區（不檢查）：fenced code、行內程式、URL、檔案路徑、HTML tag。
"""
import re, sys

CASE_RULES = [
    (re.compile(r'(?<![A-Za-z])(?i:github)(?![A-Za-z])'), 'GitHub'),
    (re.compile(r'(?<![A-Za-z])(?i:gitlab)(?![A-Za-z])'), 'GitLab'),
    (re.compile(r'(?<![A-Za-z])(?i:javascript)(?![A-Za-z])'), 'JavaScript'),
    (re.compile(r'(?<![A-Za-z])(?i:typescript)(?![A-Za-z])'), 'TypeScript'),
    (re.compile(r'(?<![A-Za-z])(?i:kubernetes)(?![A-Za-z])'), 'Kubernetes'),
    (re.compile(r'(?<![A-Za-z])(?i:macos|mac\s?os)(?![A-Za-z])'), 'macOS'),
    (re.compile(r'(?<![A-Za-z])(?i:openai)(?![A-Za-z])'), 'OpenAI'),
    (re.compile(r'(?<![A-Za-z])(?i:chatgpt)(?![A-Za-z])'), 'ChatGPT'),
    (re.compile(r'(?<![A-Za-z])(?i:youtube)(?![A-Za-z])'), 'YouTube'),
]
POLITICAL = ['祖國', '內地']
AI_FILLER = ['值得一提', '綜上所述', '總體而言', '不難發現', '不難看出',
             '毫無疑問', '深入探討', '眾所周知']

CJK = r'\u4e00-\u9fff'

def mask(line):
    """遮蔽不該檢查的區段，用全形占位字撑住邊界計算。"""
    s = re.sub(r'https?://\S+', lambda m: '█' * len(m.group()), line)
    s = re.sub(r'`[^`]+`', lambda m: '█' * len(m.group()), s)
    s = re.sub(r'</?[A-Za-z][^>]*>', lambda m: '█' * len(m.group()), s)
    s = re.sub(r'(?<![\w])[\w./-]*[/][\w/.-]+', lambda m: '█' * len(m.group()), s)
    return s

def check_line(line):
    out = []
    s = mask(line)
    for m in re.finditer(rf'[{CJK}][,.;:?!]|[,.;:?!][{CJK}]', s):
        out.append(f'半形標點: …{s[max(0,m.start()-6):m.end()+6]}…')
    for m in re.finditer(r'[“”‘’]', s):
        out.append(f'引號在地化: {m.group()} → 建議「」')
        break
    if re.search(rf'"[^"\n]*[{CJK}][^"\n]*"', s):
        out.append('引號在地化: "…" 含中文 → 建議「」')
    for m in re.finditer(rf'[{CJK}][A-Za-z0-9]|[A-Za-z0-9][{CJK}]', s):
        # 排除全形占位與中文數字詞（24小時這類仍需空格，保留為候測）
        out.append(f'邊界空格: …{s[max(0,m.start()-4):m.end()+4]}…')
    for pat, want in CASE_RULES:
        for m in pat.finditer(s):
            if m.group() != want:
                out.append(f'casing: {m.group()} → {want}')
    for w in POLITICAL:
        if w in s:
            out.append(f'政治色彩詞: {w}（依語境判斷）')
    for w in AI_FILLER:
        if w in s:
            out.append(f'AI 腔: {w}')
    return out

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    lines = open(sys.argv[1], encoding='utf-8').read().splitlines()
    in_fence = False
    hits = 0
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence or not line.strip():
            continue
        found = check_line(line)
        if found:
            hits += len(found)
            print(f'L{i}:')
            for f in found:
                print(f'  {f}')
    print(f'-- style_gate: {hits} 個候測')
    return 1 if hits else 0

if __name__ == '__main__':
    sys.exit(main())
