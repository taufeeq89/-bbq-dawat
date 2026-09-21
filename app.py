import streamlit as st
import pandas as pd

st.set_page_config(page_title="BBQ Dawat - 13 Families", page_icon="🍖", layout="wide")

st.title("🍖 Sunday BBQ Dawat - 13 Families Expense Splitter")
st.caption("Track live expenses | Thank you Ismail Bhai & Mahbub Bhai!")

# Default families
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
    ]

with st.sidebar:
    st.header("⚙️ Families (13)")
    families_text = st.text_area("Edit families (one per line)", "\n".join(st.session_state.families), height=300)
    st.session_state.families = [f.strip() for f in families_text.split("\n") if f.strip()]
    st.metric("Total Families", len(st.session_state.families))

col1, col2 = st.columns([1,2])

with col1:
    st.subheader("➕ Add Expense")
    with st.form("add_expense"):
        person = st.selectbox("Who Paid?", st.session_state.families)
        item = st.text_input("Item", placeholder="e.g., 36 lb Goat")
        amount = st.number_input("Amount $", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Add Expense")
        if submitted and amount>0:
            st.session_state.expenses.append({"Person": person, "Item": item, "Amount": amount})
            st.success(f"Added {item}: ${amount}")

    if st.button("Clear All Expenses"):
        st.session_state.expenses = []
        st.rerun()

with col2:
    st.subheader("📋 Live Expenses")
    df = pd.DataFrame(st.session_state.expenses)
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        total = df["Amount"].sum()
        per_family = total / len(st.session_state.families) if st.session_state.families else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Spent", f"${total:.2f}")
        c2.metric("Per Family", f"${per_family:.2f}")
        c3.metric("Families", len(st.session_state.families))

        paid_df = df.groupby("Person")["Amount"].sum().reindex(st.session_state.families, fill_value=0)
        summary = pd.DataFrame({
            "Paid": paid_df,
            "Share": per_family,
            "Balance": paid_df - per_family
        })
        st.subheader("💰 Settlement - Who Owes Whom")
        st.dataframe(summary.style.format("${:.2f}"), use_container_width=True)

        st.subheader("📲 WhatsApp Message")
        msg_lines = [f"*BBQ Dawat Final Split - {len(st.session_state.families)} Families*",
                     f"Total: ${total:.2f} | Per Family: ${per_family:.2f}\n",
                     "*Expenses:*"]
        for _, row in df.iterrows():
            msg_lines.append(f"- {row['Person']}: {row['Item']} = ${row['Amount']:.2f}")
        msg_lines.append("\n*Settlement:*")
        for person in summary.index:
            bal = summary.loc[person, "Balance"]
            if bal < -0.01:
                msg_lines.append(f"- {person} owes ${abs(bal):.2f}")
            elif bal > 0.01:
                msg_lines.append(f"- {person} should get ${bal:.2f}")
            else:
                msg_lines.append(f"- {person} settled ✅")
        msg_lines.append("\nJazakAllah to Ismail Bhai & Mahbub Bhai! 🤲")
        st.text_area("Copy to WhatsApp", "\n".join(msg_lines), height=300)

    else:
        st.info("No expenses yet.")

st.markdown("---")
st.caption("Made for BBQ Dawat | Mount Lebanon, PA")