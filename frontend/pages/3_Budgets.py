import streamlit as st
from datetime import date, datetime
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.logic import BudgetsLogic, CategoryLogic

st.set_page_config(page_title="Budgets", page_icon="💰", layout="wide")
st.title("💰 Budgets Management")

budgets_logic = BudgetsLogic()
category_logic = CategoryLogic()

if "logged_in_user" not in st.session_state:
    st.warning("⚠️ Please login first.")
else:
    user_id = st.session_state.logged_in_user["id"]

    # ---------- Fetch all categories ----------
    categories_res = category_logic.fetch_all_categories()
    if categories_res["Success"] and categories_res["data"]:
        category_options = {c["name"]: c["id"] for c in categories_res["data"]}
    else:
        category_options = {}

    # ---------- Add New Budget ----------
    st.subheader("➕ Add New Budget")
    if category_options:
        category_name = st.selectbox("Select Category", list(category_options.keys()))
        category_id = category_options[category_name]

        amount = st.number_input("Amount", min_value=0.0, format="%.2f")

        # Year & Month dropdowns
        current_year = datetime.today().year
        current_month = datetime.today().month
        years = [str(y) for y in range(current_year, current_year + 5)]
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        selected_year = st.selectbox("Year", years, index=0)
        selected_month = st.selectbox("Month", months, index=current_month - 1)

        if st.button("Add Budget"):
            # Convert selected month & year to proper date object
            month_number = months.index(selected_month) + 1
            budget_date = date(int(selected_year), month_number, 1)

            # Convert date to string to avoid JSON serialization issue
            res = budgets_logic.create_budget(
                user_id=user_id,
                category_id=category_id,
                amount=amount,
                month=budget_date.isoformat()
            )

            if res["Success"]:
                st.success("✅ Budget added successfully!")
            else:
                st.error(res.get("message", "Failed to add budget."))

    else:
        st.info("No categories found. Please add categories first.")

    st.divider()

    # ---------- View Budgets ----------
    st.subheader("📋 View Budgets")
    budgets_res = budgets_logic.fetch_all_budgets(user_id)
    if budgets_res["Success"] and budgets_res["data"]:
        for b in budgets_res["data"]:
            cat_name = next((c["name"] for c in categories_res["data"] if c["id"] == b["category_id"]), "Unknown")
            st.write(f"**Category:** {cat_name} | ₹{b['amount']} | Month: {b['month']}")
    else:
        st.info("No budgets yet.")
