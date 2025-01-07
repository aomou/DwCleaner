import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

def main():
    
    st.title("圖表視覺化")
    
    # 確認第一頁有上傳並處理過資料
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("尚未上傳或處理資料，請先回到『1_📁_Upload』頁面。")
        return
    

    df = st.session_state.df
    st.write(" 目前的資料：")
    st.dataframe(df)
    
    # 顯示目前的欄位名稱，方便除錯
    st.write("資料框中的欄位名稱：", df.columns.tolist())

    
    # 確保 DataFrame 包含 eventDate 欄位
    if 'eventDate' in df.columns:
        # 轉換為字串並移除逗號
        df['eventDate'] = pd.to_datetime(df['eventDate'], errors='coerce')
        # 提取年份
        df['eventDate'] = df['eventDate'].dt.year

        # 移除無效年份資料（NaN）
        df = df.dropna(subset=['eventDate'])
        df['eventDate'] = df['eventDate'].astype(int)  # 確保為整數

        # 計算每年的出現次數
        yearly_counts = df['eventDate'].value_counts().sort_index()

        # 更新 session state 中的資料
        st.session_state.df = df
        st.write(st.session_state.df)
        st.success("『eventDate』欄位處理完成！")

        st.write("計算年份出現次數!!!")
        st.write(yearly_counts)
    
    
        # 如果 yearly_counts 有資料
        if not yearly_counts.empty:
           
            st.title("Event Yearly Data Visualization")
            st.write("歷年生物出現長條圖:") 

            st.write(yearly_counts.index)
            st.write(yearly_counts.values)
            
            # 繪製長條圖
            fig = px.bar(
                x=yearly_counts.index,
                y=yearly_counts.values,
                labels={'x': 'Year', 'y': 'Number of Records'},
                title='Yearly Data Counts',
                text=yearly_counts.values  # 在每個柱上顯示數值
            )
            
            # 移除滑鼠文字顯示
            fig.update_traces(
                hovertemplate = 'Year=%{x}<br>Number of Records=%{y}<extra></extra>'
            )
    
            # 設定 X 軸和 Y 軸刻度為正整數
            fig.update_xaxes(type='category')  # X 軸：顯示年份
            fig.update_yaxes(
                dtick=int(max(yearly_counts.values)/10) if max(yearly_counts.values)>10 else 1,  # Y 軸：正整數刻度，從零開始
                rangemode = 'tozero'  # Y 軸：從零開始
            )# Y 軸：根據數據範圍計算合理的刻度間隔
            
            # 設定長條圖寬度一致
            fig.update_layout(
                bargap=0.2, # 長條間隙，值越小，長條越寬（0.2 為適中間隔）
                bargroupgap=0 # 長條組間無間隙
            )
    
            # 顯示圖表
            st.plotly_chart(fig)
    
            # # 顯示數據表
            # st.write("數據表:")
            # st.dataframe(yearly_counts)

            # 最終資料存進 Session State
            st.session_state.df = df
      
  
if __name__ == "__main__":
    main()