import streamlit as st
import math

a = st.number_input('Input an area (m2)')
r = round(math.sqrt(a / math.pi), 2)
d = round(2 * r, 2)
l = round(math.sqrt(a), 2)

st.write('A circle with an area of', a, 'has a radius of', r, 'meters and a diameter of', d, 'meters.')
st.write('A square with an area of', a, 'has a side length of', l, 'meters.')