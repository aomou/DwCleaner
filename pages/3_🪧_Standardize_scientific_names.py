def main():
    # 確認第一頁有上傳並處理過資料
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("尚未上傳或處理資料，請先回到『1_📁_Upload_and_Edit』頁面。")
        return

    df = st.session_state.df

    st.write("### 目前的資料：")
    st.dataframe(df)

    # 格式化學名的函數
    def standardize_species(scientific_name):
        if pd.notna(scientific_name):
            return scientific_name.strip().title()
        return scientific_name
    st.write(df)
    
    # 如果有資料，可以顯示「下一頁」按鈕
    if st.session_state.df is not None:
        st.info("請點選左側的『4_📍_Map_Visualization』進行地圖檢查或修正。")

if __name__ == "__main__":
    main()