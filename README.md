---
title: DwCleaner
emoji: 🐢
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: 1.40.2
app_file: app.py
pinned: false
license: cc-by-4.0
short_description: DwC data cleaner
---

# 生物數據清道夫

## Introduction

這是一個生物出現資料的清理工具，讓你可以上傳自己的資料後**檢查並修正為符合生物資料庫標準的格式**，可以使人工檢查的過程更加自動化以節省時間和人力。  

生物出現資料為「何種生物何時在何處出現」的資料，通常包含 🐢 物種、📅 時間和 📍 地點資訊。目前最大的生物多樣性資料庫為 [GBIF]((https://www.gbif.org/))（Global Biodiversity Information Facility），這個單位期待能藉由這個開放資料庫將生物資訊共享給大眾，也增加資料被利用性和科學價值。

許多學術單位或民間組織會進行生物調查並且產出生物出現資料，但因每個人記錄的格式不一，要上傳到資料庫之前必須先做清理和資料欄位的對應。GBIF 資料庫使用**國際通用資料標準 [Darwin Core](https://dwc.tdwg.org/terms/)** (DwC)，藉由定義相同的資料欄位名稱和格式，讓其他資料使用者也能讀懂每個欄位代表的含義。

## Usage & Features

跟著左側選單列的順序一步一步修改並且檢視你的資料，最後就能下載乾淨的檔案囉！

本工具包含以下 5 個清理步驟：  
1. 檔案上傳和重新命名欄位  
2. 日期格式檢查和視覺化  
3. 學名格式修正  
4. 經緯度格式修正和地理分佈視覺化  
5. 下載檔案

## Upcoming Features

1. 修正日期格式為 ISO 8601
2. 清理文字欄位前後的空格（如欄位 locality）
3. 合併相似值（如「台灣」和「臺灣」）
4. 學名校正和根據學名自動新增物種高階分類群（串接 NomenMatch 和 GBIF Backbone API）
5. 根據經緯度自動新增國家、國家代碼、縣市等地區資訊（Google maps API or Geocoding API）

## Limitations

需注意的是，此工具能接受的資料格式有以下限制：  
1. 只能處理度分秒和十進位的經緯度格式  
2. 目前只能處理出現紀錄（occurrence）的資料類型，不接受調查活動（sampling event）和物種名錄（checklist）  
3. 無法將 core 和 extension 分成兩個資料表  

## Reference

各欄位的填寫標準和要求請參考以下資源：  
- [Darwin Core Quick Reference Guide - Darwin Core](https://dwc.tdwg.org/terms/)  
- [Darwin Core 達爾文核心標準資料格式說明 中文版](https://hackmd.io/TmsAwdC6TaGr-lciIwxh3g?view)