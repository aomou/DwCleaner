import streamlit as st
import pandas as pd 

def main():
    st.write(處理學名格式)
    # 確認第一頁有上傳並處理過資料
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("尚未上傳或處理資料，請先回到『1_📁_Upload』頁面。")
        return

    df = st.session_state.df

    st.write("### 目前的資料：")
    st.dataframe(df)

    # 格式化學名的函數
    def standardize_species(scientific_name):
        if pd.notna(scientific_name):
            return scientific_name.strip().title()
        return scientific_name
        
    # 建立新的資料表，並套用格式化函數
    new_df = df.copy()  # 假設 `df` 是 pandas DataFrame
    if 'scientific_name' not in new_df.columns:
        st.error("資料表中缺少 'scientific_name' 欄位，無法進行格式化處理。")
        return
        
    new_df['scientific_name'] = new_df['scientific_name'].apply(standardize_species)
    
    st.write("### 格式化後的資料：")
    st.dataframe(new_df)
    
    # 如果有資料，可以顯示「下一頁」按鈕
    if st.session_state.df is not None:
        st.info("請點選左側的『4_📍_Map_Visualization』進行地圖檢查或修正。")
    
    st.session_state.df = new_df
if __name__ == "__main__":
    main()