import streamlit as st

def show_topology():
    st.code("""
A0 ─ A1 ─ A2
│    │    │
B0 ─ B1 ─ B2
│    │    │
C0 ─ C1 ─ C2
""")