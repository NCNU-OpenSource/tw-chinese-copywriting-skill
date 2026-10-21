---
name: tw-chinese-copywriting
version: 1.0.0
author: Hermes Agent
license: MIT
description: Use for zh-TW text. Taiwan terms only, sparanoid layout.
metadata:
  hermes:
    tags: [writing, zh-tw, formatting]
    related_skills: [humanizer]
---

# 繁體中文文案（臺灣用語＋排版指北）

## When to Use
任何要產出或修改繁體中文文字的場合：回覆、文件、專案 README、訊息稿、UI 文案。對純英文輸出與程式碼本身不適用，但其中的中文註解適用。

基準：https://github.com/sparanoid/chinese-copywriting-guidelines
兩條硬規則：(1) 輸出的繁體中文**不得出現大陸用語**；(2) 排版完全依指北。

## 詞彙（硬規則）

寫繁體中文前先想：這個詞是不是大陸用語？是就換臺灣用語。完整對照表見 `references/terminology.md`（含禁用詞清單，可擴充）。

高頻核心：軟體／硬體／伺服器／資料庫／程式碼／網路／搜尋／使用者／預設／載入／記憶體／硬碟／執行緒／處理程序／叢集／容器映像／網域名稱／介面／選單／設定／專案／檔案／資料夾／說明文件／回饋／教學／列印／儲存／視窗／外掛程式／快取／頻寬／連接埠／字元／應用程式／影片／音訊／資訊／雲端／私訊／按讚。

例外（不轉換）：專有名詞與產品名（微信、支付寶、抖音、Bilibili 照原名）、程式碼與指令、欄位名與 API 名稱、引文原文、檔名／路徑、大陸機構與地名（照原名）、英文技術詞照英文（使用者自己也是此慣例）。

## 排版（指北摘要，逐條遵守）

1. **中西空格**：中文與英文、中文與數字、數字與單位之間加半形空格：`在 GitHub 上，資料存在 `config.yaml` 裡`、`買了 5000 元`、`寬頻 10 Gbps`。
   - 例外：度數／百分比緊貼數字（`15%`、`90°`），但與中文之間仍留空格（`有 15% 的效能提升`）；產品官方格式照官方（如「豆瓣FM」）。
2. **全形標點周圍不加空格**：`買了 iPhone，好開心！`（不是 `iPhone ，`）。
3. **中文語境用全形標點**：，。！？；：、「」『』（）。括號內是英文也用全形括號：`成像（NMRI）`。
4. **不重複標點**：不用 `！！`、`？？！`，各用一次。
5. **數字一律半形**：`1000 元`，不用１０００（設計稿對齊除外）。
6. **完整英文句子保留半形標點**，用「」包裹：`「Stay hungry, stay foolish.」`；英文書名用斜體不用《》，不借用中文標點改造英文。
7. **專有名詞正確大小寫**：GitHub、macOS、JavaScript，不寫 github／Github。
8. 簡繁正確：輸出為正體字，用字正確。

## 工作流

1. 起草。
2. 對照 `references/terminology.md` 禁用詞列逐詞檢視；檔案交付前用 `search_files` 照該檔末段的禁用詞 regex 掃一遍。
3. 排版自查：中西空格、全形標點、數字半形、標點不重複、專有名詞大小寫。
4. 兩關都過才輸出。

## 維護

新遇到的大陸詞隨時 patch 進 `references/terminology.md`（只在本次工作出現過的也收）。