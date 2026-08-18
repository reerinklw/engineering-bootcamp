"""Visual calculator built with Streamlit."""

import streamlit as st

from application import OPERATIONS

st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("Calculator")
st.markdown("🧮", unsafe_allow_html=True)

operation = st.selectbox(
    "Operation",
    options=list(OPERATIONS.keys()),
    format_func=lambda x: f"{x.capitalize()} 🚀",
)

col1, col2 = st.columns([1, 1])
with col1:
    a = st.number_input("First number", value=0.0)
with col2:
    b = st.number_input("Second number", value=0.0)

if st.button("Calculate", type="primary"):
    try:
        result = OPERATIONS[operation](a, b)
        st.success(f"Result: {result:.2f}")
    except ValueError as exc:
        st.error(str(exc))

st.markdown(
    """
    <style>
        .stApp {
            background-color: #191919;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #191919;
            color: #FFFFFF;
        }
        .stButton>button:hover {
            background-color: #19C919;
        }
        .sinput input {
            background-color: #191919;
            color: #FFFFFF;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
