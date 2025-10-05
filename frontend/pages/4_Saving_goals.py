import streamlit as st
from datetime import date
import sys, os
import plotly.graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.logic import SavingGoalsLogic

st.set_page_config(page_title="Saving Goals", page_icon="🎯", layout="wide")
st.title("🎯 Saving Goals Management")

saving_goals_logic = SavingGoalsLogic()

# Check if user is logged in
if "logged_in_user" not in st.session_state:
    st.warning("⚠️ Please login first.")
else:
    user_id = st.session_state.logged_in_user["id"]

    # ---------- Add New Goal ----------
    st.subheader("➕ Add New Goal")
    name = st.text_input("Goal Name")
    target = st.number_input("Target Amount", min_value=0.0, format="%.2f")
    deadline = st.date_input("Deadline", date.today())

    if st.button("Add Goal"):
        deadline_str = deadline.isoformat() if isinstance(deadline, date) else str(deadline)
        res = saving_goals_logic.create_saving_goal(user_id, name, target, deadline=deadline_str)
        if res["Success"]:
            st.success("✅ Goal added successfully!")
        else:
            st.error(res.get("message", "Failed to add goal."))

    st.divider()

    # ---------- View & Update Goals ----------
    st.subheader("📋 View & Update Goals")
    goals_res = saving_goals_logic.fetch_all_saving_goals(user_id)

    if goals_res["Success"] and goals_res["data"]:
        for g in goals_res["data"]:
            goal_id = g['id']
            saved_amount = g['saved_amount']
            target_amount = g['target_amount']

            # Initialize previous saved amount in session_state
            if f'prev_saved_{goal_id}' not in st.session_state:
                st.session_state[f'prev_saved_{goal_id}'] = saved_amount

            st.write(f"**ID:** {goal_id} | {g['name']} | ₹{saved_amount} / ₹{target_amount}")
            progress = min(saved_amount / target_amount, 1.0)
            st.progress(progress)

            # Input to add/subtract saved amount
            delta_saved = st.number_input(
                f"Add/Subtract Money for {g['name']}",
                value=0.0,
                step=100.0,
                key=f"delta_saved_{goal_id}"
            )

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Update Saved {goal_id}"):
                    new_saved_amount = max(saved_amount + delta_saved, 0.0)  # prevent negative total
                    res = saving_goals_logic.modify_saving_goal(goal_id, saved_amount=new_saved_amount)
                    if res["Success"]:
                        st.success(f"✅ Saved amount updated to ₹{new_saved_amount}!")
                        # Check for balloons
                        prev_saved = st.session_state[f'prev_saved_{goal_id}']
                        if prev_saved < target_amount <= new_saved_amount:
                            st.balloons()
                        st.session_state[f'prev_saved_{goal_id}'] = new_saved_amount
                        # Update local variable to reflect change immediately
                        saved_amount = new_saved_amount
                    else:
                        st.error(res.get("message", "Failed to update saved amount"))
            with col2:
                if st.button(f"Delete Goal {goal_id}"):
                    saving_goals_logic.remove_saving_goal(goal_id)
                    st.success("✅ Goal deleted!")
                    st.session_state.pop(f'prev_saved_{goal_id}', None)

    else:
        st.info("No saving goals yet.")

    st.divider()

    # ---------- Goals Overview Chart ----------
    st.subheader("📊 Goals Overview")
    if goals_res["Success"] and goals_res["data"]:
        goal_names = [g["name"] for g in goals_res["data"]]
        saved = [g["saved_amount"] for g in goals_res["data"]]
        target_amounts = [g["target_amount"] for g in goals_res["data"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=goal_names, y=saved, name="Saved", marker_color="green"))
        fig.add_trace(go.Bar(
            x=goal_names, y=[t - s for t, s in zip(target_amounts, saved)],
            name="Remaining", marker_color="lightgrey"))
        fig.update_layout(
            barmode="stack",
            title="Savings Progress",
            yaxis_title="Amount",
            xaxis_title="Goals"
        )
        st.plotly_chart(fig, use_container_width=True)
