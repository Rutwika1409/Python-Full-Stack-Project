# db.py
import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import date, datetime, timedelta  # ADD datetime here

# Loading environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

class DatabaseManager:
    def __init__(self):
        self.supabase = supabase

            # ---------- HELPER METHOD ----------
    def _convert_dates_to_strings(self, result):
        """Convert any date objects in the response to ISO format strings"""
        if hasattr(result, 'data') and result.data:
            for item in result.data:
                # Convert budget month field
                if 'month' in item and isinstance(item['month'], (date, datetime)):
                    item['month'] = item['month'].isoformat()
                # Convert transaction date field if needed
                if 'date' in item and isinstance(item['date'], (date, datetime)):
                    item['date'] = item['date'].isoformat()
                # Convert saving goal target_date field if needed
                if 'target_date' in item and isinstance(item['target_date'], (date, datetime)):
                    item['target_date'] = item['target_date'].isoformat()
        return result


    #-------------------------------------
    #-------------Users Table-------------
    #-------------------------------------
    # Create Users
    def add_user(self, email, name):
        try:
            res = self.supabase.table("users").insert({"email": email, "name": name}).execute()
            return res
        except Exception as e:
            err_msg = str(e)
            if "duplicate key value" in err_msg or "already exists" in err_msg:
                return {"Success": False, "message": "User already exists"}
            return {"Success": False, "message": err_msg}


    # Get All Users
    def get_all_users(self):
        return self.supabase.table("users").select("*").execute()

    # Get User by ID
    def get_user_by_id(self, user_id):    
        return self.supabase.table("users").select("*").eq("id", user_id).execute()

    # Update User
    def update_user(self, user_id, email=None, name=None):
        update_data = {}
        if email:
            update_data["email"] = email
        if name:
            update_data["name"] = name
        return self.supabase.table("users").update(update_data).eq("id", user_id).execute()

    # Delete User
    def delete_user(self, user_id):
        return self.supabase.table("users").delete().eq("id", user_id).execute()

    #-------------------------------------
    #-----------Categories Table----------
    #-------------------------------------
    # Create categories
    def add_category(self, name):
        return self.supabase.table("categories").insert({"name": name}).execute()

    # Get All categories
    def get_all_categories(self):
        return self.supabase.table("categories").select("*").execute()

    # Get category by ID
    def get_category_by_id(self, category_id):
        return self.supabase.table("categories").select("*").eq("id", category_id).execute()

    # Update category
    def update_category(self, category_id, updated_name):
        return self.supabase.table("categories").update({"name": updated_name}).eq("id", category_id).execute()

    # Delete Category
    def delete_category(self, category_id):
        return self.supabase.table("categories").delete().eq("id", category_id).execute()

    #-----------------------------------------
    #-----------Transactions Table------------
    #-----------------------------------------

    # Create Transaction
    def add_transaction(self, user_id, category_id, t_type, amount, description=None, date=None, receipt_url=None):
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
        return self.supabase.table("transactions").insert(transaction_data).execute()

    # In get_all_transactions method:
    def get_all_transactions(self, limit=100, offset=0):
        result = self.supabase.table("transactions") \
            .select("*") \
            .order("date", desc=True) \
            .range(offset, offset + limit - 1) \
            .execute()
        
        return self._convert_dates_to_strings(result)  # CALL HELPER HERE

    # Get Monthly Transactions
    def get_monthly_transactions(self, user_id, year, month):
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        return self.supabase.table("transactions").select("*").eq("user_id", user_id).gte("date", start_date).lt("date", end_date).execute()

    # Get Transaction by ID
    def get_transaction_by_id(self, transaction_id):
        return self.supabase.table("transactions").select("*").eq("id", transaction_id).execute()

    # Update Transaction
    def update_transaction(self, transaction_id, category_id=None, t_type=None, amount=None, description=None):
        update_data = {}
        if category_id:
            update_data["category_id"] = category_id
        if t_type:
            update_data["type"] = t_type
        if amount:
            update_data["amount"] = amount
        if description is not None:  # Allow empty string
            update_data["description"] = description
        return self.supabase.table("transactions").update(update_data).eq("id", transaction_id).execute()

    # Delete Transaction
    def delete_transaction(self, transaction_id):
        return self.supabase.table("transactions").delete().eq("id", transaction_id).execute()

    #-------------------------------------
    #-----------Budgets Table-------------
    #-------------------------------------
    # Create Budget
    def add_budget(self, user_id, category_id, amount, month=None):
        if month is None:
            today = date.today()
            month = date(today.year, today.month, 1)

        # Prepare the data with proper date conversion
        budget_data = {
            "user_id": user_id,
            "category_id": category_id,
            "amount": amount,
            "month": month.isoformat() if isinstance(month, (date, datetime)) else month
        }
        
        result = self.supabase.table("budgets").insert(budget_data).execute()
        
        return self._convert_dates_to_strings(result)

    # Get All Budgets
    def get_all_budgets(self, user_id=None):
        query = self.supabase.table("budgets").select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.execute()
        
        return self._convert_dates_to_strings(result)  # CALL HELPER HERE

    # Get Budget by ID
    def get_budget_by_id(self, budget_id):
        result = self.supabase.table("budgets").select("*").eq("id", budget_id).execute()
        
        return self._convert_dates_to_strings(result)  # CALL HELPER HERE

    # Update Budget
    def update_budget(self, budget_id, category_id=None, amount=None, month=None):
        update_data = {}
        if category_id:
            update_data["category_id"] = category_id
        if amount:
            update_data["amount"] = amount
        if month:
            update_data["month"] = month
        
        result = self.supabase.table("budgets").update(update_data).eq("id", budget_id).execute()
        
        return self._convert_dates_to_strings(result)  # CALL HELPER HERE

    # Delete Budget
    def delete_budget(self, budget_id):
        result = self.supabase.table("budgets").delete().eq("id", budget_id).execute()
        
        return self._convert_dates_to_strings(result)  # CALL HELPER HERE

    #-------------------------------------------
    #-----------Saving Goals Table---------------
    #-------------------------------------------

    # Create Saving Goal
    def add_saving_goal(self, user_id, name, target_amount, saved_amount=0.0, target_date=None, status="active"):
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
        return self.supabase.table("savings_goals").insert(goal_data).execute()

    # In get_all_saving_goals method:
    def get_all_saving_goals(self, user_id=None):
        query = self.supabase.table("savings_goals").select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.execute()
        
        return self._convert_dates_to_strings(result)  # CALL HELPER HERE

    # Get Saving Goal by ID
    def get_saving_goal_by_id(self, goal_id):
        return self.supabase.table("savings_goals").select("*").eq("id", goal_id).execute()

    # Update Saving Goal
    def update_saving_goal(self, goal_id, name=None, target_amount=None, saved_amount=None, target_date=None, status=None):
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
        return self.supabase.table("savings_goals").update(update_data).eq("id", goal_id).execute()

    # Delete Saving Goal
    def delete_saving_goal(self, goal_id):
        return self.supabase.table("savings_goals").delete().eq("id", goal_id).execute()