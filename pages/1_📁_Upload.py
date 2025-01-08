import streamlit as st
import pandas as pd

def main():
    st.title("上傳並修改資料")

    required_cols = [
        "occurrenceID",
        "eventDate",
        "scientificName",
        "verbatimLatitude",
        "verbatimLongitude",
        "individualCount",
        "locality"
    ]

    # 初始化 session_state
    if "df" not in st.session_state:
        st.session_state.df = None
    if "updated_df" not in st.session_state:
        st.session_state.updated_df = None
    if "required_mapping" not in st.session_state:
        st.session_state.required_mapping = {col: "---尚未選擇---" for col in required_cols}
    if "new_col_settings" not in st.session_state:
        st.session_state.new_col_settings = {}
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "ready_for_step2" not in st.session_state:
        st.session_state.ready_for_step2 = False

    # 提供範例檔案選項
    use_sample = st.checkbox("使用範例檔案 (data/test_occurrenceData.xlsx)")

    # 上傳檔案
    user_file = st.file_uploader("請上傳您的 Excel 或 CSV 檔案", type=["xlsx", "xls", "csv"])

    # 決定最終使用的檔案
    uploaded_file = "data/test_occurrenceData.xlsx" if use_sample else user_file

    try:
        if uploaded_file:
            if isinstance(uploaded_file, str) and uploaded_file.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif isinstance(uploaded_file, str):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("檔案成功上傳！以下是資料內容：")
            st.dataframe(df)
            st.session_state.df = df
            if st.session_state.updated_df is None:
                st.session_state.updated_df = df.copy()
        else:
            st.warning("尚未上傳檔案，或未啟用範例檔案")
    except Exception as e:
        st.error(f"上傳或處理檔案時發生錯誤：{e}")

    if st.session_state.df is not None:
        df = st.session_state.updated_df  # 使用已更新的表單
        original_cols = list(df.columns)

        if st.session_state.step == 1:
            st.subheader("第一步：指定必填欄位對應")
            st.markdown(
                "請選擇上傳文件中的欄位名稱，對應到系統所需的必填欄位。\n\n"
                "若文件中沒有相應欄位，可以選擇 '新增此欄位'，並在下一步填寫相關資料。"
            )
            used_columns = set()

            for req_col in required_cols:
                available_options = ["---尚未選擇---", "(新增此欄位)"] + [
                    col for col in original_cols if col not in used_columns
                ]

                current_value = st.session_state.required_mapping[req_col]
                if current_value not in available_options:
                    available_options.append(current_value)

                def update_mapping(req_col=req_col):
                    selected_value = st.session_state[f"required_map_{req_col}"]
                    if selected_value not in ["---尚未選擇---", "(新增此欄位)"]:
                        used_columns.add(selected_value)
                    st.session_state.required_mapping[req_col] = selected_value

                st.selectbox(
                    f"必填欄位『{req_col}』對應：",
                    options=available_options,
                    index=available_options.index(current_value)
                    if current_value in available_options
                    else 0,
                    key=f"required_map_{req_col}",
                    on_change=update_mapping
                )

            if st.button("設定完成第一步"):
                if any(value == "---尚未選擇---" for value in st.session_state.required_mapping.values()):
                    st.warning("請確保所有必填欄位都有對應的欄位或選擇新增此欄位。")
                else:
                    for req_col, selected in st.session_state.required_mapping.items():
                        if selected not in ["---尚未選擇---", "(新增此欄位)"]:
                            if selected in df.columns:
                                df.rename(columns={selected: req_col}, inplace=True)
                        elif selected == "(新增此欄位)":
                            st.session_state.new_col_settings[req_col] = {"method": "manual_input", "cols": [], "delimiter": "-", "text": ""}
                    
                    st.session_state.updated_df = df
                    st.session_state.ready_for_step2 = True
                    st.success("第一步設定完成！以下是更正後的表單：")
                    st.dataframe(df)

        if st.session_state.ready_for_step2:
            if st.button("進入第二步驟"):
                st.session_state.step = 2

        if st.session_state.step == 2:
            st.subheader("第二步：設定新增欄位")
            
            # 檢查是否有需要新增的欄位
            new_field_needed = any(
                selected == "(新增此欄位)" for selected in st.session_state.required_mapping.values()
            )
            if not new_field_needed:
                st.info("若沒有需要新增的欄位，請直接點選「完成第二步」。")
                
            for req_col, selected in st.session_state.required_mapping.items():
                if selected == "(新增此欄位)":
                    setting = st.session_state.new_col_settings.get(req_col, {})
                    method = st.radio(
                        f"請選擇如何產生『{req_col}』的資料：",
                        ["combine_cols", "manual_input"],
                        index=0 if setting.get("method", "manual_input") == "combine_cols" else 1,
                        key=f"method_{req_col}"
                    )
                    st.session_state.new_col_settings[req_col]["method"] = method

                    if method == "combine_cols":
                        with st.form(key=f"form_{req_col}"):
                            selected_cols = st.multiselect(
                                f"請選擇要合併的欄位 (可多選)：",
                                options=list(df.columns),
                                default=setting.get("cols", []),
                                key=f"selected_cols_{req_col}"
                            )
                            delimiter = st.text_input(
                                f"請輸入要用來連接的符號：",
                                value=setting.get("delimiter", "-"),
                                key=f"delim_{req_col}"
                            )
                            submit_button = st.form_submit_button(label="確定選擇")
                            if submit_button:
                                st.session_state.new_col_settings[req_col]["cols"] = selected_cols
                                st.session_state.new_col_settings[req_col]["delimiter"] = delimiter
                    elif method == "manual_input":
                        manual_text = st.text_area(
                            f"請輸入此欄位的文字內容 (所有列都會套用同一份文字)：",
                            value=setting.get("text", ""),
                            key=f"manual_text_{req_col}"
                        )
                        st.session_state.new_col_settings[req_col]["text"] = manual_text

            if st.button("完成第二步"):
                for req_col, setting in st.session_state.new_col_settings.items():
                    if setting["method"] == "combine_cols":
                        cols_to_combine = setting["cols"]
                        delim = setting["delimiter"]
                        df[req_col] = df[cols_to_combine].fillna("").apply(
                            lambda row: delim.join(str(x) for x in row), axis=1
                        )
                    elif setting["method"] == "manual_input":
                        df[req_col] = setting["text"]
                
                if "occurrenceID" in df.columns:
                    if df["occurrenceID"].duplicated().any():
                        st.warning("檢測到 occurrenceID 欄位中有重複值，系統將自動修正。")
                        df["occurrenceID"] = [f"ID{i+1}" for i in range(len(df))]
                        st.success("occurrenceID 欄位已修正為唯一值。")
                
                st.session_state.df = df
                st.success("新增欄位完成！以下為更新後的資料：")
                st.dataframe(df)

                st.info("請點選左側的「📊Chart Visualization」進行下一步資料可視化。")

if __name__ == "__main__":
    main()
