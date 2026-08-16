"""Visual calculator built with Streamlit."""

import streamlit as st

from application import OPERATIONS

st.title("Calculator")

operation = st.selectbox(
    "Operation",
    options=list(OPERATIONS.keys()),
    format_func=str.capitalize,
)

col1, col2 = st.columns(2)
with col1:
    a = st.number_input("First number", value=0.0)
with col2:
    b = st.number_input("Second number", value=0.0)

if st.button("Calculate"):
    try:
        result = OPERATIONS[operation](a, b)
        st.success(f"Result: {result}")
    except ValueError as exc:
        st.error(str(exc))
