import streamlit as st
import math

a = st.number_input('Input an area (m)')
r = math.sqrt(a / math.pi)
d = 2 * r
l = math.sqrt(a)

st.write('A circle with an area of', a, 'has a radius of', r, 'and a diameter of', d)
st.write('A square with an area of', a, 'has a side length of', l)