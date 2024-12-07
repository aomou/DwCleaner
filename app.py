import streamlit as st

st.header("Calculate diameter and radius of given area")

import math

a = round(st.number_input('Input an area (m2)'), 2)
r = round(math.sqrt(a / math.pi), 2)
d = round(2 * r, 2)
l = round(math.sqrt(a), 2)

st.write('r = ', r)
st.write('d = ', d)
st.write('l = ', l)

st.write('A circle with an area of', a, 'has a radius of', r, 'meters and a diameter of', d, 'meters.', '\n', 'A square with an area of', a, 'has a side length of', l, 'meters.')

import pyperclip

st.header("Mass edit text")

# 初始化 state
if "new_txt" not in st.session_state:
    st.session_state.new_txt = ""
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# UI 設計
col1, col2 = st.columns(2)

newline = col1.checkbox("Remove all line breaks")
num_space = col2.checkbox("Trim spaces around numbers")
comma = col1.checkbox("Replace halfwidth comma `,` with fullwidth comma `，`")

txt = st.text_area(label = 'Paste your text:', placeholder = 'here', height = 34*8) # height > 68 (2 lines)

if st.button('Submit'):
    if txt:
        if comma:
            txt = txt.replace(',', '，')

        if newline:
            txt = txt.replace('\n', '')

        if num_space:
            for i in range(10):  # 0-9
                txt = txt.replace(f" {i} ", str(i))
                txt = txt.replace(f"{i} ", str(i))
                txt = txt.replace(f" {i}", str(i))

        st.session_state.new_txt = txt  # 讓點按 copy 後不會重跑而讓 new_txt 消失
        st.session_state.submitted = True
    else:
        st.write('Please paste your text!')

# 顯示處理好的文字 (submit後才出現)
if st.session_state.submitted:
    st.text_area(
        label = 'New text:', value = st.session_state.new_txt, height = max(68, int(len(txt)/41*30)))

    if st.button('Copy', key="copy_button"):
        pyperclip.copy(st.session_state.new_txt)
        st.success('Text copied successfully!')

    st.code(f'''{st.session_state.new_txt}''', language = "text", wrap_lines = True)
