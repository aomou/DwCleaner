def main():
  st.write("測試")
  # 確認第一頁有上傳並處理過資料
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("尚未上傳或處理資料，請先回到『1_📁_Upload_and_Edit』頁面。")
        return

    df = st.session_state.df

    st.write("### 目前的資料：")
    st.dataframe(df)

