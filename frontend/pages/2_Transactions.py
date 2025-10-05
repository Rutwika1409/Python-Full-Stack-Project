import streamlit as st
from datetime import date
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.logic import TransactionLogic, CategoryLogic

st.set_page_config(page_title="Transactions", page_icon="💳", layout="wide")
st.title("💳 Transaction Management")

transaction_logic = TransactionLogic()
category_logic = CategoryLogic()

if "logged_in_user" not in st.session_state:
    st.warning("⚠️ Please login first.")
else:
    user_id = st.session_state.logged_in_user["id"]

    categories = category_logic.fetch_all_categories()
    cat_data = categories["data"] if categories["Success"] else []
    cat_map = {c["name"]: c["id"] for c in cat_data}

    st.subheader("➕ Add Transaction")
    cat_name = st.selectbox("Category", list(cat_map.keys()) if cat_map else ["No categories"])
    t_type = st.selectbox("Type", ["income", "expense"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    desc = st.text_area("Description")
    t_date = st.date_input("Date", date.today())

    if st.button("Add Transaction"):
        res = transaction_logic.create_transaction(user_id, cat_map[cat_name], t_type, amount, desc, t_date.isoformat())
        if res["Success"]:
            st.success("✅ Transaction added successfully!")
        else:
            st.error(res["message"])

    st.divider()

    st.subheader("📋 View All Transactions")
    txns = transaction_logic.fetch_all_transactions()
    user_txns = [t for t in txns["data"] if t["user_id"] == user_id] if txns["Success"] else []
    if user_txns:
        for t in user_txns:
            st.write(f"**ID:** {t['id']} | **Type:** {t['type']} | ₹{t['amount']} | **Category:** {t['category_id']} | {t['description']}")
    else:
        st.info("No transactions found.")
