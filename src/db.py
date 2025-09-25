# db_manager.py
import os
from supabase import create_client
from dotenv import load_dotenv


#loading environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

#-------------------------------------
#-------------Users Table-------------
#-------------------------------------
#Create Users
def add_user(email, name):
    return supabase.table("users").insert({"email": email, "name": name}).execute()

#Get All Users
def get_all_users():
    return supabase.table("users").select("*").execute()

#Get User by ID
def get_user_by_id(user_id):    
    return supabase.table("users").select("*").eq("id", user_id).execute()

#Update User
def update_user(user_id, email=None, name=None):
    update_data = {}
    if email:
        update_data["email"] = email
    if name:
        update_data["name"] = name
    return supabase.table("users").update(update_data).eq("id", user_id).execute()

#Delete User
def delete_user(user_id):
    return supabase.table("users").delete().eq("id", user_id).execute()

#-------------------------------------
#-----------Categories Table----------
#-------------------------------------
#Create categories
def add_category(name):
    return supabase.table("categories").insert({"name": name}).execute()

#Get All categories
def get_all_categories():
    return supabase.table("categories").select("*").execute()

#Get category by ID
def get_category_by_id(category_id):
    return supabase.table("categories").select("*").eq("id", category_id).execute()

#Update category
def update_category(category_id, updated_name):
    return supabase.table("categories").update({"name": updated_name}).eq("id", category_id).execute()

#Delete Category
def delete_category(category_id):
    return supabase.table("categories").delete().eq("id", category_id).execute()

#-----------------------------------------
#-----------Transactions Table------------
#-----------------------------------------

#Create Transaction
def add_transaction(user_id, category_id, t_type, amount, description=None, date=None, receipt_url=None):
    transaction_data = {
        "user_id": user_id,
        "category_id": category_id,
        "type": t_type,
        "amount": amount
    }
    if description:
        transaction_data["description"] = description
    if date:
        transaction_data["date"] = date
    if receipt_url:
        transaction_data["receipt_url"] = receipt_url    
    return supabase.table("transactions").insert(transaction_data).execute()

#Get All Transactions
def get_all_transactions(limit=100, offset=0):
    return supabase.table("transactions") \
        .select("*") \
        .order("date", desc=True) \
        .range(offset, offset + limit - 1) \
        .execute()


#Get Monthly Transactions
def get_monthly_transactions(user_id, year, month):
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"
    return supabase.table("transactions").select("*").eq("user_id", user_id).gte("date", start_date).lt("date", end_date).execute()

#Get Transaction by ID
def get_transaction_by_id(transaction_id):
    return supabase.table("transactions").select("*").eq("id", transaction_id).execute()

#Update Transaction
def update_transaction(transaction_id, category_id=None, t_type=None, amount=None, description=None):
    update_data = {}
    if category_id:
        update_data["category_id"] = category_id
    if t_type:
        update_data["type"] = t_type
    if amount:
        update_data["amount"] = amount
    if description is not None:  # Allow empty string
        update_data["description"] = description
    return supabase.table("transactions").update(update_data).eq("id", transaction_id).execute()

#Delete Transaction
def delete_transaction(transaction_id):
    return supabase.table("transactions").delete().eq("id", transaction_id).execute()

#-------------------------------------
#-----------Budgets Table-------------
#-------------------------------------

#Create Budget
from datetime import date
def add_budget(user_id, category_id, amount, month=None):
    if month is None:
        month = date.today().replace(day=1)

    return supabase.table("budgets").insert({
        "user_id": user_id,
        "category_id": category_id,
        "amount": amount,
        "month": month
    }).execute()

#Get All Budgets
def get_all_budgets(user_id):
    return supabase.table("budgets").select("*").eq("user_id", user_id).execute()

#Get Budget by ID
def get_budget_by_id(budget_id):
    return supabase.table("budgets").select("*").eq("id", budget_id).execute()

#Update Budget
def update_budget(budget_id, category_id=None, amount=None, month=None):
    update_data = {}
    if category_id:
        update_data["category_id"] = category_id
    if amount:
        update_data["amount"] = amount
    if month:
        update_data["month"] = month
    return supabase.table("budgets").update(update_data).eq("id", budget_id).execute()

#Delete Budget
def delete_budget(budget_id):
    return supabase.table("budgets").delete().eq("id", budget_id).execute()

#-------------------------------------------
#-----------Saving Goals Table---------------
#-------------------------------------------

#Create Saving Goal
from datetime import date, timedelta

def add_saving_goal(user_id, name, target_amount, saved_amount=0.0, target_date=None, status="active"):
    if target_date is None:
        target_date = date.today() + timedelta(days=30)
    goal_data = {
        "user_id": user_id,
        "name": name,
        "target_amount": target_amount,
        "saved_amount": saved_amount,
        "target_date": target_date,
        "status": status
    }
    return supabase.table("savings_goals").insert(goal_data).execute()

#Get All Saving Goals
def get_all_saving_goals(user_id):
    return supabase.table("savings_goals").select("*").eq("user_id", user_id).execute()

#Get Saving Goal by ID
def get_saving_goal_by_id(goal_id):
    return supabase.table("savings_goals").select("*").eq("id", goal_id).execute()

#Update Saving Goal
def update_saving_goal(goal_id, name=None, target_amount=None, saved_amount=None, target_date=None, status=None):
    update_data = {}
    if name:
        update_data["name"] = name
    if target_amount:
        update_data["target_amount"] = target_amount
    if saved_amount is not None:  # Allow zero
        update_data["saved_amount"] = saved_amount
    if target_date:
        update_data["target_date"] = target_date
    if status:
        update_data["status"] = status
    return supabase.table("savings_goals").update(update_data).eq("id", goal_id).execute()

#Delete Saving Goal
def delete_saving_goal(goal_id):
    return supabase.table("savings_goals").delete().eq("id", goal_id).execute()




