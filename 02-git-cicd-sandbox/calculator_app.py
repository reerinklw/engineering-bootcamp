"""Visual calculator built with Streamlit."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
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
