import streamlit as st
import pandas as pd

def main():
    st.title("上傳並修改資料")

    # 設定合法欄位列表（依照實際需求自行調整或擴充）
    valid_columns = ["latitude", "longitude", "name", "address", "type"]

    # 在 Session State 中準備一個 df 變數，如果沒有就預設 None
    if "df" not in st.session_state:
        st.session_state.df = None

    uploaded_file = st.file_uploader("請上傳您的 Excel 或 CSV 檔案", type=["xlsx", "xls", "csv"])
    if uploaded_file:
        try:
            # 自動判斷 CSV 或 Excel 進行讀取
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("檔案成功上傳！以下是資料內容：")
            st.write(df)

            # 檢查欄位是否符合要求
            incorrect_columns = [col for col in df.columns if col not in valid_columns]

            if incorrect_columns:
                st.warning("以下欄位名稱有錯誤，請選擇正確的名稱進行修正：")
                for col in incorrect_columns:
                    st.write(f"- 錯誤欄位：**{col}**")

                    # 提供下拉式選單讓用戶選擇正確名稱
                    new_column_name = st.selectbox(
                        f"請選擇『{col}』的正確欄位名稱：",
                        options=valid_columns,
                        key=col  # 確保多個 selectbox 不互相衝突
                    )

                    # 若選擇了新的名稱就改名
                    if new_column_name:
                        df.rename(columns={col: new_column_name}, inplace=True)
                        st.success(f"{col} 已更改為 {new_column_name}")

                # 預覽修正後的資料
                st.write("### 修正後的資料預覽：")
                st.dataframe(df)

            else:
                st.success("所有欄位名稱都正確，無需修正。")

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
        if st.button("下一頁 →"):
            st.info("請點選左側的『2_📍_Map_Visualization』進行地圖檢查或修正。")

if __name__ == "__main__":
    main()
