import streamlit as st
import io
import pandas as pd

def main():
    st.title("下載資料")
    # 檢查是否有上傳的資料
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("尚未上傳或處理資料，請先回到『📁 Upload』頁面。")
        return

    # 取得已處理的資料
    df = st.session_state.df
    

    # 顯示資料表
    st.write("### 以下是處理後的資料表：")
    st.dataframe(df)
    
    # 將 DataFrame 轉換為 CSV 格式
    csv = df.to_csv(index=False).encode("utf-8")
    
    # 提供下載按鈕
    st.download_button(
        label="下載csv",
        data=csv,
        file_name="updated_data.csv",
        mime="text/csv"
    )

    st.write("以Excel打開csv檔，編碼指定\"utf-8\"可解決欄位亂碼問題")
    
    # 將DataFrame 轉換為 Excel 格式
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine-'xlsxwriter') as writer:
        df.to_excel(write, index=False, sheet_name="Sheet1")
        writer.save()
        xlsx_data = output.getvalue()
    
    # 提供下載按鈕
    st.download_button(
        label="下載 Excel",
        data=xlsx_data,
        file_name="updated_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
if __name__ == "__main__":
    main()