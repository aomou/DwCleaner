import streamlit as st
import pandas as pd

def main():
    st.title("上傳並修改資料")

    # 設定合法欄位列表（依照實際需求自行調整或擴充）
    valid_columns = ["occurrenceID", "eventDate", "scientificName", "verbatimLatitude", "verbatimLongitude", "individualCount", "locality"]

    # 在 Session State 中準備一個 df 變數，如果沒有就預設 None
    if "df" not in st.session_state:
        st.session_state.df = None

    # 使用者可以上傳檔案
    user_file = st.file_uploader("請上傳您的 Excel 或 CSV 檔案", type=["xlsx", "xls", "csv"])

    # 提供範例檔案選項（checkbox 或者 radio / selectbox 皆可）
    use_sample = st.checkbox("使用範例檔案 (data/1_jellyfish_originalData.csv)")

    # 用一個變數來代表真正要處理的 uploaded_file
    uploaded_file = None

    # 決定最終的 uploaded_file
    if use_sample:
        uploaded_file = "../data/1_jellyfish_originalData.csv"
    elif user_file is not None:
        uploaded_file = user_file
    
    if uploaded_file:
        try:
            # 如果是字串代表是範例檔案路徑，用 pandas.read_csv() 讀取
            if isinstance(uploaded_file, str):
                df = pd.read_csv(uploaded_file)
            else:
                # user_file 的情況 -> 要判斷副檔名
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

            st.write("檔案成功上傳！以下是資料內容：")
            st.write(df)

            # 在這裡可以做進一步的資料清理 (例如填補空值、轉型態...)
            # ------ 以下示範 ------
            df.fillna("", inplace=True)
            # ------ 結束示範 ------

            # 最終資料存進 Session State
            st.session_state.df = df

        except Exception as e:
            st.error(f"上傳或處理檔案時發生錯誤：{e}")

    # 如果有資料，可以顯示「下一頁」按鈕
    if st.session_state.df is not None:
        st.info("請點選左側的『2_📍_Map_Visualization』進行地圖檢查或修正。")

if __name__ == "__main__":
    main()
