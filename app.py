import streamlit as st
import pandas as pd

st.set_page_config(page_title="BBQ Dawat - FINAL", page_icon="🍖", layout="wide")

ZELLE_PHONE = "412-294-7303"
ZELLE_EMAIL = "xxxxxxxx"
ZELLE_NAME = "Mohamed Hameed"

st.title("🍖 BBQ Dawat - FINAL SETTLEMENT")
st.success("✅ Grand Total: $823.14 | Per Family: $63.32 | 13 Families")

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
        {"Person": "Ismail Bhai Mintt", "Item": "Sauces", "Amount": 60.00},
        {"Person": "Ismail Bhai Mintt", "Item": "Rice & Dessert", "Amount": 160.00},
    ]

df = pd.DataFrame(st.session_state.expenses)
total = df["Amount"].sum()
per_family = total / len(st.session_state.families)
paid_df = df.groupby("Person")["Amount"].sum().reindex(st.session_state.families, fill_value=0)

# Calculate Who Pays Whom
settlement_rows = []
for person in st.session_state.families:
    paid = paid_df[person]
    balance = paid - per_family
    if balance < -0.01:
        settlement_rows.append({
            "From (Payer)": person,
            "To (Receiver)": "Ismail Bhai Mintt",
            "Amount": abs(balance),
            "Note": f"Paid ${paid:.2f}, Owes ${abs(balance):.2f}"
        })

settlement_df = pd.DataFrame(settlement_rows)

# --- UI ---
col1, col2 = st.columns([1,2])

with col1:
    st.metric("Grand Total", f"${total:.2f}")
    st.metric("Per Family", f"${per_family:.2f}")
    st.metric("Ismail Gets Back", f"${paid_df['Ismail Bhai Mintt'] - per_family:.2f}")
    with st.expander("⚙️ Edit Families & Zelle"):
        st.text(f"Zelle: {ZELLE_PHONE}")

with col2:
    st.subheader("📋 Expenses")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("💰 WHO PAYS WHOM - FINAL")
    st.dataframe(
        settlement_df.style.format({"Amount": "${:.2f}"}),
        use_container_width=True, hide_index=True
    )

    # Detailed summary
    st.subheader("📊 Full Summary")
    summary = pd.DataFrame({
        "Paid": paid_df,
        "Share": per_family,
        "Balance": paid_df - per_family
    })
    st.dataframe(summary.style.format("${:.2f}"), use_container_width=True)

    st.subheader("📲 WhatsApp Final Message")
    msg = [f"*🍖 BBQ FINAL - $ {total:.2f} / 13 = ${per_family:.2f} each*","", "*WHO PAYS WHOM (to Ismail Bhai):*"]
    for _, r in settlement_df.iterrows():
        msg.append(f"- {r['From (Payer)']} -> Ismail Bhai: ${r['Amount']:.2f}")
    msg.append("")
    msg.append(f"*Zelle:* {ZELLE_PHONE} / {ZELLE_EMAIL}")
    msg.append(f"Ismail gets back: ${paid_df['Ismail Bhai Mintt'] - per_family:.2f}")
    msg.append("JazakAllah! 🤲")
    st.text_area("Copy", "\n".join(msg), height=400)