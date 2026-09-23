import streamlit as st
import pandas as pd

st.set_page_config(page_title="BBQ Dawat - FINAL", page_icon="🍖", layout="wide")

# --- EDIT THIS: Ismail Bhai Zelle Info ---
ZELLE_PHONE = "412-294-7303"  # Replace with real number
ZELLE_EMAIL = "XXX-XXXX@com"
ZELLE_NAME = "Mohamed Hameed"
# -----------------------------------------

st.title("🍖 BBQ Dawat - FINAL SETTLEMENT")
st.success("✅ Final Total: $823.14 | Per Family: $63.32 | 13 Families")
st.caption("Thank you Ismail Bhai & Mahbub Bhai! | Mount Lebanon, PA")

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

with st.sidebar:
    st.header("⚙️ Families (13)")
    families_text = st.text_area("Edit families", "\n".join(st.session_state.families), height=250)
    st.session_state.families = [f.strip() for f in families_text.split("\n") if f.strip()]
    st.divider()
    st.header("💳 Payment Info")
    st.info(f"**Pay to:** {ZELLE_NAME}\n\n**Zelle:** {ZELLE_PHONE}\n\n**Email:** {ZELLE_EMAIL}")
    st.metric("Total Families", len(st.session_state.families))
    st.metric("Grand Total", "$823.14")

col1, col2 = st.columns([1,2])

with col1:
    st.subheader("➕ Add Expense")
    with st.form("add_expense"):
        person = st.selectbox("Who Paid?", st.session_state.families)
        item = st.text_input("Item", placeholder="e.g., Extra plates")
        amount = st.number_input("Amount $", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Add Expense")
        if submitted and amount>0:
            st.session_state.expenses.append({"Person": person, "Item": item, "Amount": amount})
            st.success(f"Added {item}: ${amount}")
            st.rerun()

    if st.button("Reset to Final $823.14"):
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
        st.rerun()

with col2:
    st.subheader("📋 All Expenses")
    df = pd.DataFrame(st.session_state.expenses)
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
    
    st.subheader("💰 FINAL Settlement - Pay to Ismail Bhai")
    summary_display = summary.copy()
    summary_display["Status"] = summary_display["Balance"].apply(
        lambda x: f"Owes ${abs(x):.2f}" if x < -0.01 else f"Gets ${x:.2f}" if x > 0.01 else "Settled ✅"
    )
    st.dataframe(summary_display.style.format({"Paid":"${:.2f}","Share":"${:.2f}","Balance":"${:.2f}"}), use_container_width=True)

    st.subheader("💳 Payment Instructions")
    st.markdown(f"""
    <div style="background-color:#eff6ff; padding:15px; border-radius:10px; border:2px solid #2563eb">
    <b>Please Zelle to {ZELLE_NAME}:</b><br>
    📱 Phone: <code>{ZELLE_PHONE}</code><br>
    📧 Email: <code>{ZELLE_EMAIL}</code><br><br>
    <b>Memo:</b> "BBQ Dawat - Your Name"<br>
    <b>Deadline:</b> This weekend<br><br>
    <b>Ismail Bhai gets back: ${summary.loc['Ismail Bhai Mintt','Balance']:.2f}</b>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📲 WhatsApp Message - COPY THIS")
    msg_lines = [f"*🍖 BBQ Dawat Final - 13 Families - Mt. Lebanon*",
                 f"Total: ${total:.2f} | Per Family: ${per_family:.2f}\n",
                 "*Breakdown:*"]
    for _, row in df.iterrows():
        msg_lines.append(f"- {row['Person']}: {row['Item']} = ${row['Amount']:.2f}")
    msg_lines.append("\n*Settlement (Pay to Ismail Bhai):*")
    for person in summary.index:
        bal = summary.loc[person, "Balance"]
        if bal < -0.01:
            msg_lines.append(f"- {person}: ${abs(bal):.2f}")
    msg_lines.append(f"\n*Zelle to {ZELLE_NAME}: {ZELLE_PHONE} / {ZELLE_EMAIL}*")
    msg_lines.append(f"Ismail Bhai gets back: ${summary.loc['Ismail Bhai Mintt','Balance']:.2f}")
    msg_lines.append("\nJazakAllah Khair to All! 🤲")
    
    full_msg = "\n".join(msg_lines)
    st.text_area("Copy", full_msg, height=350)
    
    # Download PDF bill
    st.download_button(
        label="📄 Download Bill Text",
        data=full_msg,
        file_name="BBQ_Final_Settlement.txt",
        mime="text/plain"
    )

st.markdown("---")
st.caption("Final as of Ismail Bhai message 10:20 PM | Built for 13 families")