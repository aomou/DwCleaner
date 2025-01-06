import streamlit as st

def main():
 # 檢查是否有上傳的資料
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("尚未上傳或處理資料，請先回到『上傳與編輯資料』頁面。")
        return

    # 取得已處理的資料
    df = st.session_state.df
    

    # 顯示資料表
    st.write("以下是更新後的資料表：")
    st.dataframe(df)
    
    # 將 DataFrame 轉換為 CSV 格式
    csv = df.to_csv(index=False).encode("utf-8")
    
    # 提供下載按鈕
    st.download_button(
        label="下載更新後的資料",
        data=csv,
        file_name="updated_data.csv",
        mime="text/csv"
    )
if __name__ == "__main__":
    main()