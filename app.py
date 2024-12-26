import streamlit as st
import pandas as pd
import math
import re                # 檢查座標格式
from geopy import Point  # 轉換座標
import pydeck as pdk     # 畫地圖

def main():
    st.title("我的多分頁 Streamlit App")
    st.write("歡迎來到首頁，請從左側選單選取功能頁面。")

if __name__ == "__main__":
    main()
