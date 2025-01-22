import streamlit as st
import pandas as pd
import numpy as np 
import math
import re                # 檢查座標格式
from geopy import Point  # 轉換座標
import pydeck as pdk     # 畫地圖
import plotly.express as px # 畫長條圖
from datetime import datetime # 檢查日期


def main():
    st.title("生物數據清道夫 :duck:")
    st.markdown("> 歡迎來到首頁，請閱讀以下說明後，從左側選單選取功能頁面。")

    st.subheader(":information_source: 這是什麼？")

    introduction = '''
    一個 :blue-background[生物出現資料的清理工具] ，讓你可以上傳自己的資料後**檢查並修正為符合生物資料庫標準的格式**，可以使人工檢查的過程更加自動化以節省時間和人力。  
    跟著左側選單列的順序一步一步修改並且檢視你的資料，最後就能下載乾淨的檔案囉！
    '''
    st.markdown(introduction)
    
    st.divider() 
    
    st.subheader(":broom: 為何要清理資料？")
    why = '''
    生物出現資料為「何種生物何時在何處出現」的資料，通常包含 :fish: 物種、:calendar: 時間和 :pushpin: 地點資訊。目前最大的生物多樣性資料庫為 [GBIF]((https://www.gbif.org/))（Global Biodiversity Information Facility），這個單位期待能藉由這個開放資料庫將生物資訊共享給大眾，也增加資料被利用性和科學價值。
    \n\n
    許多學術單位或民間組織會進行生物調查並且產出生物出現資料，但因每個人記錄的格式不一，要上傳到資料庫之前必須先做清理和資料欄位的對應。GBIF 資料庫使用**國際通用資料標準 [Darwin Core](https://dwc.tdwg.org/terms/)** (DwC)，藉由定義相同的資料欄位名稱和格式，讓其他資料使用者也能讀懂每個欄位代表的含義。
    '''
    st.markdown(why)

    st.divider() 
    
    st.subheader(":mag: 如何使用？")
    how = '''
    本工具包含以下 5 個清理步驟：  
        1. 檔案上傳和欄位清理  
        2. 日期格式檢查和視覺化  
        3. 學名格式修正  
        4. 經緯度格式修正和地理分佈視覺化  
        5. 下載檔案
    \n\n
    需注意的是，此工具能接受的資料格式有以下限制：  
        1. 只能處理度分秒和十進位的經緯度格式  
        2. 目前只能處理出現紀錄（occurrence）的資料類型，不接受調查活動（sampling event）和物種名錄（checklist）
        3. 無法將 core 和 extension 分成兩個資料表  
    \n\n
    各欄位的填寫標準和要求請參考以下資源：  
    - [Darwin Core Quick Reference Guide - Darwin Core](https://dwc.tdwg.org/terms/)  
    - [Darwin Core 達爾文核心標準資料格式說明 中文版](https://hackmd.io/TmsAwdC6TaGr-lciIwxh3g?view)
    '''
    st.markdown(how)

if __name__ == "__main__":
    main()