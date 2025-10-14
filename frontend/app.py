import streamlit as st
import plotly.express as px
from datetime import date, datetime
import sys, os
from src.auth import AuthLogic

# Ensure backend logic is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.logic import UserLogic, CategoryLogic, TransactionLogic, BudgetsLogic, SavingGoalsLogic

# ------------------ App Configuration ------------------
st.set_page_config(page_title="FinTrack", page_icon="💰", layout="wide")

# ------------------ Initialize Session State ------------------
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# ------------------ Backend Instances ------------------
user_logic = UserLogic()
category_logic = CategoryLogic()
transaction_logic = TransactionLogic()
budgets_logic = BudgetsLogic()
saving_goals_logic = SavingGoalsLogic()

# ------------------ LOGIN / REGISTER ------------------
if not st.session_state.logged_in_user:
    st.markdown("<h1 style='text-align:center;'>💰 Welcome to FinTrack</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            auth_logic = AuthLogic()
            result = auth_logic.sign_in(email, password)
            if result["Success"]:
                users = user_logic.fetch_all_users()
                user_found = next((u for u in users["data"] if u["email"] == email), None)
                if user_found:
                    st.session_state.logged_in_user = user_found
                    st.success("Logged in successfully ✅")
                    st.rerun()
                else:
                    st.error("User not found in database.")
            else:
                st.error(result["message"])
    
    with tab2:
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Create Account"):
            auth_logic = AuthLogic()
            result = auth_logic.sign_up(email, password, name)
            if result["Success"]:
                st.success("Account created successfully! Please login.")
            else:
                st.error(result["message"])

# ------------------ DASHBOARD ------------------
if st.session_state.logged_in_user:
    user = st.session_state.logged_in_user
    user_id = user["id"]

    st.markdown(f"<h2>🏠 Welcome back, {user['name']}!</h2>", unsafe_allow_html=True)
    st.markdown("### Your Financial Overview for This Month")

    # -------- Fetch Data --------
    txns = transaction_logic.fetch_all_transactions()
    budgets = budgets_logic.fetch_all_budgets(user_id)
    goals = saving_goals_logic.fetch_all_saving_goals(user_id)
    
    # ADDED: Fetch categories for budget alerts and spending chart
    categories_res = category_logic.fetch_all_categories()

    user_txns = [t for t in txns["data"] if t["user_id"] == user_id] if txns["Success"] else []
    income = sum(t["amount"] for t in user_txns if t["type"] == "income")
    expense = sum(t["amount"] for t in user_txns if t["type"] == "expense")
    remaining_balance = income - expense

    # -------- Stats Section --------
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Income", f"₹{income:.2f}")
    c2.metric("Total Expense", f"₹{expense:.2f}")
    c3.metric("Available Balance", f"₹{remaining_balance:.2f}")
    c4.metric("Budgets Set", f"{len(budgets['data']) if budgets['Success'] else 0}")
    c5.metric("Active Goals", f"{len(goals['data']) if goals['Success'] else 0}")

    st.divider()

    # -------- Budget Alerts --------
    st.subheader("🔔 Budget Alerts")
    
    # Check if categories were fetched successfully
    if categories_res["Success"] and categories_res["data"]:
        # Create a mapping from category ID to category name
        category_id_to_name = {c["id"]: c["name"] for c in categories_res["data"]}
        
        budget_analysis = budgets_logic.check_budget_limits(user_id)
        if budget_analysis["Success"] and budget_analysis["data"]:
            exceeded_budgets = [b for b in budget_analysis["data"] if b['exceeded']]
            warning_budgets = [b for b in budget_analysis["data"] if b['percentage_used'] >= 90 and not b['exceeded']]
            
            if exceeded_budgets:
                for budget in exceeded_budgets:
                    category_name = category_id_to_name.get(budget['category_id'], "Unknown Category")
                    st.error(f"🚨 **{category_name}** budget exceeded by ₹{budget['spent_amount'] - budget['budget_amount']:,.2f}")
            
            if warning_budgets:
                for budget in warning_budgets:
                    category_name = category_id_to_name.get(budget['category_id'], "Unknown Category")
                    st.warning(f"⚠️ **{category_name}** budget at {budget['percentage_used']:.1f}%")
            
            if not exceeded_budgets and not warning_budgets:
                st.success("✅ All budgets are within limits!")
        else:
            st.info("No budget alerts for this month.")
    else:
        st.info("No categories found. Please add categories first to set up budgets.")

    st.divider()

    # -------- Active Saving Goals --------
    st.subheader("🎯 Active Saving Goals")
    if goals["Success"] and goals["data"]:
        for g in goals["data"]:
            progress = min(g["saved_amount"] / g["target_amount"], 1.0) if g["target_amount"] else 0
            st.write(f"**{g['name']}** (₹{g['saved_amount']} / ₹{g['target_amount']})")
            st.progress(progress)
    else:
        st.info("No active saving goals yet.")

    st.divider()

    # -------- Spending by Category --------
    st.subheader("📊 Monthly Spending by Category")
    if user_txns:
        cat_totals = {}
        for t in user_txns:
            if t["type"] == "expense":
                cat_totals[t["category_id"]] = cat_totals.get(t["category_id"], 0) + t["amount"]

        if cat_totals:
            # Use category names instead of IDs if available
            if categories_res["Success"] and categories_res["data"]:
                category_id_to_name = {c["id"]: c["name"] for c in categories_res["data"]}
                df = [{"Category": category_id_to_name.get(k, "Unknown"), "Amount": v} for k, v in cat_totals.items()]
            else:
                df = [{"Category": k, "Amount": v} for k, v in cat_totals.items()]
                
            fig = px.pie(df, names="Category", values="Amount", title="Expenses by Category")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expenses recorded this month.")
    else:
        st.info("No transactions available.")

    st.divider()

    # -------- Navigation Section --------
    st.markdown("### 🧭 Navigate to Other Sections")
    n1, n2, n3, n4, n5 = st.columns(5)

    if n1.button("📂 Categories"):
        st.switch_page("pages/1_Categories.py")

    if n2.button("💳 Transactions"):
        st.switch_page("pages/2_Transactions.py")

    if n3.button("📈 Budgets"):
        st.switch_page("pages/3_Budgets.py")

    if n4.button("🎯 Saving Goals"):
        st.switch_page("pages/4_Saving_Goals.py")

    if n5.button("🚪 Logout"):
        st.session_state.logged_in_user = None
        st.success("Logged out successfully!")
        st.rerun()

    # -------- Account Management Section --------
    st.divider()
    st.subheader("⚙️ Account Management")
    u1, u2 = st.columns(2)

    # UPDATE ACCOUNT
    if u1.button("✏️ Update Account"):
        with st.form("update_form"):
            new_name = st.text_input("New Name", value=user["name"])
            new_email = st.text_input("New Email", value=user["email"])
            submitted = st.form_submit_button("Save Changes")
            if submitted:
                res = user_logic.modify_user(user["id"], new_email, new_name)
                if res["Success"]:
                    user["name"] = new_name
                    user["email"] = new_email
                    st.session_state.logged_in_user = user
                    st.success("✅ User details updated successfully!")
                else:
                    st.error(res["message"])

    # DELETE ACCOUNT
    if u2.button("🗑️ Delete Account"):
        st.warning("⚠️ This will permanently delete your account and all data.")
        if st.button("Confirm Delete"):
            res = user_logic.remove_user(user["id"])
            if res["Success"]:
                st.success("✅ Account deleted successfully!")
                st.session_state.logged_in_user = None
                st.rerun()
            else:
                st.error(res["message"])