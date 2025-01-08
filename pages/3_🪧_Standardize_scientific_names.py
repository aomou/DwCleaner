import streamlit as st
import pandas as pd 

def main():
    st.title("學名格式化")
    # 確認第一頁有上傳並處理過資料
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("尚未上傳或處理資料，請先回到『1_📁_Upload』頁面。")
        return
    
    df = st.session_state.df

    st.write("### 目前的資料：")
    st.dataframe(df)

    # 格式化學名的函數
    def format_scientific_name(scientificName):
        if pd.notna(scientificName):
            return scientificName.strip().title()
        return scientificName
        
    # 建立新的資料表，並套用格式化函數
    new_df = df.copy()  
    new_df['scientificName'] = new_df['scientificName'].apply(format_scientific_name)
    
    if 'scientificName' not in new_df.columns:
        st.error("資料表中缺少 'scientificName' 欄位，無法進行格式化處理。")
        return
        
    new_df['scientificName'] = new_df['scientificName'].apply(format_scientific_name)
    
    st.write("### 學名格式化後的資料：")
    st.dataframe(new_df)
    
    # 如果有資料，可以顯示「下一頁」按鈕
    if st.session_state.df is not None:
        st.info("請點選左側的『4_📍_Map_Visualization』進行地圖檢查或修正。")
    
    st.session_state.df = new_df
    
if __name__ == "__main__":
    main()