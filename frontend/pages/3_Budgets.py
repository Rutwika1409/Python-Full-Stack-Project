import streamlit as st
from datetime import date, datetime
import sys
import os

# Fix import path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, project_root)

from src.logic import BudgetsLogic, CategoryLogic, TransactionLogic

st.set_page_config(page_title="Budgets", page_icon="💰", layout="wide")
st.title("💰 Budgets Management")

budgets_logic = BudgetsLogic()
category_logic = CategoryLogic()
transaction_logic = TransactionLogic()

if "logged_in_user" not in st.session_state:
    st.warning("⚠️ Please login first.")
else:
    user_id = st.session_state.logged_in_user["id"]
    
    # Get current month for default selection
    current_date = datetime.today()
    current_year = current_date.year
    current_month = current_date.month

    # ---------- Fetch all categories ----------
    categories_res = category_logic.fetch_all_categories()
    if categories_res["Success"] and categories_res["data"]:
        category_options = {c["name"]: c["id"] for c in categories_res["data"]}
        category_id_to_name = {c["id"]: c["name"] for c in categories_res["data"]}
    else:
        category_options = {}
        category_id_to_name = {}
        st.error("No categories found. Please add categories first.")

    # ---------- Add New Budget ----------
    st.subheader("➕ Add New Budget")
    
    if category_options:
        with st.form("add_budget_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                category_name = st.selectbox("Select Category", list(category_options.keys()))
                category_id = category_options[category_name]
            
            with col2:
                amount = st.number_input("Monthly Budget Amount", min_value=0.0, format="%.2f", step=100.0, value=1000.0)
            
            with col3:
                # Year & Month dropdowns
                years = [str(y) for y in range(current_year-1, current_year + 2)]
                months = [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ]
                
                selected_year = st.selectbox("Year", years, index=1)  # Default to current year
                selected_month = st.selectbox("Month", months, index=current_month - 1)

            submitted = st.form_submit_button("Add Budget")
            
            if submitted:
                if amount <= 0:
                    st.error("❌ Budget amount must be greater than 0.")
                else:
                    # Convert selected month & year to proper date object
                    month_number = months.index(selected_month) + 1
                    budget_date = date(int(selected_year), month_number, 1)

                    # Check if budget already exists for this category and month
                    existing_budgets = budgets_logic.fetch_all_budgets(user_id)
                    budget_exists = False
                    
                    if existing_budgets["Success"] and existing_budgets["data"]:
                        for budget in existing_budgets["data"]:
                            # Extract year-month from the stored date
                            if isinstance(budget['month'], str):
                                budget_month = budget['month'][:7]  # Get YYYY-MM part
                            else:
                                # If it's already a date object
                                budget_month = budget['month'].strftime('%Y-%m')
                            
                            target_month = f"{selected_year}-{month_number:02d}"
                            
                            if (budget['category_id'] == category_id and 
                                budget_month == target_month):
                                budget_exists = True
                                st.error(f"❌ Budget already exists for {selected_month} {selected_year}")
                                break

                    if not budget_exists:
                        # Pass the date object directly (not as string)
                        res = budgets_logic.create_budget(
                            user_id=user_id,
                            category_id=category_id,
                            amount=amount,
                            month=budget_date  # Pass date object, not string
                        )

                        if res["Success"]:
                            st.success("✅ Budget added successfully!")
                            st.balloons()
                            st.rerun()  # Refresh to show the new budget
                        else:
                            st.error(res.get("message", "Failed to add budget."))

    st.divider()

    # ---------- View Budgets & Check Limits ----------
    st.subheader("📋 Your Budgets & Spending Analysis")
    
    # Month selection for analysis
    col1, col2 = st.columns(2)
    with col1:
        analysis_year = st.selectbox("Analysis Year", 
                                   [str(y) for y in range(current_year-1, current_year + 2)], 
                                   index=1, key="analysis_year")
    with col2:
        analysis_month = st.selectbox("Analysis Month", 
                                    ["January", "February", "March", "April", "May", "June",
                                     "July", "August", "September", "October", "November", "December"],
                                    index=current_month - 1, key="analysis_month")
    
    analysis_month_num = ["January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November", "December"].index(analysis_month) + 1
    analysis_date = date(int(analysis_year), analysis_month_num, 1)
    
    if st.button("🔍 Check Budget Progress"):
        # Get budget analysis
        budget_analysis = budgets_logic.check_budget_limits(user_id, analysis_date)
        
        if budget_analysis["Success"] and budget_analysis["data"]:
            st.subheader(f"📊 Budget Analysis for {analysis_month} {analysis_year}")
            
            for analysis in budget_analysis["data"]:
                category_name = category_id_to_name.get(analysis['category_id'], "Unknown Category")
                spent = analysis['spent_amount']
                budget = analysis['budget_amount']
                remaining = analysis['remaining_amount']
                percentage = analysis['percentage_used']
                
                # Create columns for better layout
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**{category_name}**")
                
                with col2:
                    st.metric("Budget", f"₹{budget:,.2f}")
                
                with col3:
                    st.metric("Spent", f"₹{spent:,.2f}", delta=f"-₹{spent:,.2f}")
                
                with col4:
                    st.metric("Remaining", f"₹{remaining:,.2f}")
                
                # Progress bar with color coding
                progress_color = "red" if analysis['exceeded'] else "green" if percentage < 80 else "orange"
                st.progress(min(percentage / 100, 1.0), text=f"{percentage:.1f}% used")
                
                # Show alerts
                if analysis['exceeded']:
                    st.error(f"🚨 **Budget exceeded!** You've spent ₹{spent - budget:,.2f} over your ₹{budget:,.2f} budget for {category_name}.")
                elif percentage >= 90:
                    st.warning(f"⚠️ **Close to limit!** You've used {percentage:.1f}% of your {category_name} budget.")
                elif percentage <= 20:
                    st.success(f"🎉 **Great job!** You've only used {percentage:.1f}% of your {category_name} budget.")
                
                st.write("---")
        else:
            st.info(f"No budgets found for {analysis_month} {analysis_year}.")

    st.divider()

    # ---------- View All Budgets with Delete Option ----------
    st.subheader("🗂️ Your Budgets")
    budgets_res = budgets_logic.fetch_all_budgets(user_id)
    
    if budgets_res["Success"] and budgets_res["data"]:
        # Group budgets by month
        budgets_by_month = {}
        for budget in budgets_res["data"]:
            # Handle both string and date formats
            if isinstance(budget['month'], str):
                month_key = budget['month'][:7]  # YYYY-MM
            else:
                month_key = budget['month'].strftime('%Y-%m')
                
            if month_key not in budgets_by_month:
                budgets_by_month[month_key] = []
            budgets_by_month[month_key].append(budget)
        
        # Display budgets by month
        for month_key, month_budgets in sorted(budgets_by_month.items(), reverse=True):
            year, month_num = month_key.split('-')
            month_name = ["January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November", "December"][int(month_num)-1]
            
            st.write(f"### {month_name} {year}")
            
            for budget in month_budgets:
                category_name = category_id_to_name.get(budget['category_id'], "Unknown")
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{category_name}**")
                with col2:
                    st.write(f"₹{budget['amount']:,.2f}")
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{budget['id']}"):
                        result = budgets_logic.remove_budget(budget['id'])
                        if result["Success"]:
                            st.success(f"✅ Budget for {category_name} deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete budget.")
            
            st.write("---")
    else:
        st.info("No budgets set yet. Create your first budget above!")