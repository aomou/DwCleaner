import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

def main():
    error = False
    st.title("圖表可視化")
    
    # 確認第一頁有上傳並處理過資料
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("尚未上傳或處理資料，請先回到『1_📁_Upload』頁面。")
        return

    df = st.session_state.df

    st.write(" 目前的資料：")
    st.dataframe(df)
    
  # 提取年份及月份
    def extract_year(eventDate):
      for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%Y.%m.%d'):
          try:
              date_obj = datetime.strptime(str(eventDate), fmt)
              # 返回標準化的日期格式 (%Y-%m-%d)
              standardized_date = date_obj.strftime('%Y-%m-%d')
              return date_obj.year
          except ValueError:
              continue
      return None


    # 確保 DataFrame 包含 eventDate 欄位
    if 'eventDate' in df.columns:
        df['year']= df['eventDate'].apply(extract_year)
        st.success("處理完成！")    
    else:
        # 確保 year欄位存在後再進行操作(非空值均轉為字串)
        if 'year' in df.columns:
            df['year']= df['eventDate'].apply(lambda x: str(x) if pd.notna(x) else x)
            st.write(df)
            st.success("處理完成！")
        else:
            st.error("無法取得年份資料，請回到『1_Upload』增加年欄位!")
            error = True     
                
    
        

    if not error:
        # 確保日期欄位為字串並取出年份
        df['eventDate'] = pd.to_datetime(df['eventDate'], errors='coerce')
        df['year'] = df['eventDate'].dt.year

        # 計算每個年份的出現次數
        yearly_counts = df['year'].value_counts().sort_index()

        # 建立長條圖
        st.title("Event Yearly Data Visualization")
        st.write("每年數據累計圖:") # Yearly Count

        # 使用Plotly繪製長條圖
        # 使用 Plotly 繪製長條圖
        fig = px.bar(
            x=yearly_counts.index,
            y=yearly_counts.values,
            labels={'x': 'Year', 'y': 'Number of Records'},
            title='Yearly Data Counts',
            text=yearly_counts.values  # 在每個柱上顯示數值
        )
        
        # 移除鼠標的文字顯示
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

        # 顯示數據表
        st.write("數據表:")
        st.dataframe(yearly_counts)

      
  # 最終資料存進 Session State
    st.session_state.df = df
  
if __name__ == "__main__":
    main()