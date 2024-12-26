import io

st.title('title')

uploaded_file = st.file_uploader("請上傳您的 Excel 檔案", type=["xlsx", "xls", "csv"])

if uploaded_file:
    try:

        # 讀取檔案
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("檔案成功上傳！以下是資料內容：")
        st.write(df)

        # 檢查欄位是否符合要求
        incorrect_columns = [col for col in df.columns if col not in valid_columns]

        if incorrect_columns:
            st.warning("以下欄位名稱有錯誤：")
            for col in incorrect_columns:
                st.write(f"錯誤欄位：{col}")

                # 提供下拉式選單讓用戶選擇正確的名稱
                new_column_name = st.selectbox(
                    f"請選擇 {col} 的正確欄位名稱：",
                    options=valid_columns,
                    key=col
                )

                # 如果用戶選擇了新的名稱，進行更新
                if new_column_name:
                    df.rename(columns={col: new_column_name}, inplace=True)
                    st.success(f"{col} 已更改為 {new_column_name}")

            # 更新後的資料預覽
            st.write("修正後的資料預覽：")
            st.dataframe(df)

            # 嘗試解決 PyArrow 相關問題
            try:
                st.write("檢查欄位資料類型：")
                st.write(df.dtypes)

                # 將所有非支持類型轉為字串
                for col in df.columns:
                    if df[col].dtype == "object":
                        df[col] = df[col].astype(str)

                # 填補空值
                df.fillna("", inplace=True)

                # 更新後的資料再次預覽
                st.write("資料清理後的預覽：")
                st.dataframe(df)

            except Exception as clean_error:
                st.error(f"資料清理失敗：{clean_error}")

            # 提供下載選項
            try:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                processed_data = output.getvalue()

                st.download_button(
                    label="下載修正後的 Excel 檔案",
                    data=processed_data,
                    file_name="updated_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as download_error:
                st.error(f"下載檔案失敗：{download_error}")

        else:
            st.success("所有欄位名稱都正確！")

    except Exception as e:
        st.error(f"上傳或處理檔案時發生錯誤：{e}")