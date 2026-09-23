import streamlit as st
import pandas as pd

st.set_page_config(page_title="BBQ Dawat - FINAL", page_icon="🍖", layout="wide")

st.title("🍖 BBQ Dawat - FINAL SETTLEMENT")
st.success("✅ Final Total: $823.14 | Per Family: $63.32 | 13 Families")
st.caption("Thank you Ismail Bhai & Mahbub Bhai!")

default_families = [
    "Mahsooque CTS", "Faraz Ahmed", "Firdous Pittsburgh", "Qadir Bhai",
    "Hasan Bhai", "Mydeen Kasim", "Ismail Bhai Mintt", "Aijaz Bhai Pitts",
    "Mahbub Pitts", "Rafic Bhai", "Sheik", "Jafar Inamdar Usa Pitts", "You (Host)"
]

if 'families' not in st.session_state:
    st.session_state.families = default_families.copy()
if 'expenses' not in st.session_state:
    st.session_state.expenses = [
        {"Person": "Rafic Bhai", "Item": "Dollar Tree", "Amount": 25.68},
        {"Person": "Rafic Bhai", "Item": "Walmart", "Amount": 15.49},
        {"Person": "Mahsooque CTS", "Item": "Snacks & kids juice", "Amount": 33.32},
        {"Person": "Mahsooque CTS", "Item": "Soda", "Amount": 10.70},
        {"Person": "Jafar Inamdar Usa Pitts", "Item": "Pita bread", "Amount": 5.98},
        {"Person": "Hasan Bhai", "Item": "Watermelon", "Amount": 11.97},
        {"Person": "Ismail Bhai Mintt", "Item": "Goat & Rotisserie Chicken", "Amount": 500.00},
        {"Person": "Ismail Bhai Mintt", "Item": "Sauces - Garlic, Hummus, Green", "Amount": 60.00},
        {"Person": "Ismail Bhai Mintt", "Item": "Rice & Dessert", "Amount": 160.00},
    ]

# ... rest same as before (sidebar + settlement logic) ...