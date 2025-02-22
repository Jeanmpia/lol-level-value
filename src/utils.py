import re
import streamlit as st

def camel_to_spaces(s):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s).title()

def gold_helper():
    st.sidebar.markdown("## Gold Calculation Helper")
    st.sidebar.markdown("""
    **Gold = Starting Gold + (Level - 1) * Gold per Level**

    - **Starting Gold:** Sum of selected stat flat values (e.g. health, mana, etc.)
    - **Gold per Level:** Sum of selected stat per level values
    - **Final Gold:** Starting Gold + 17 * Gold per Level
    - **Gold Increase:** Final Gold - Starting Gold
    """)

