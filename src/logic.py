# src/logic.py
from src.db import DatabaseManager

class UserLogic:
    """
    Acts as a bridge between frontend (Streamlit/FastAPI) and the database.
    """
    def __init__(self):
        #Create a databse manager instance (this will handle all the db operations)
        self.db = DatabaseManager()

    #----------Create----------
    def create_user(self, email, name):
        """ Add a new user to the databse.
        Return success message if user is added successfully"""
        
        if not email or not name:
            return {"Success": False, "message": "Email and Name are required."}
        
        #Call DB method to add user
        result = self.db.add_user(email, name)
        if result.get("Success"):
            return {"Success": True, "message": "User added Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.get('error')}"}
        
    #---------Read----------
    def fetch_all_users(self):
        """ Fetch all users from the database."""
        return self.db.get_all_users()
    def fetch_user_by_id(self, user_id):
        """ Fetch a user by ID from the database."""
        return self.db.get_user_by_id(user_id)
    
    #---------Update----------
    def modify_user(self, user_id, email=None, name=None):
        """ Update user details in the database."""
        result = self.db.update_user(user_id, email, name)
        if result.get("Success"):
            return {"Success": True, "message": "User updated Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.get('error')}"}
        
    #---------Delete----------
    def remove_user(self, user_id):
        """ Delete a user from the database."""
        result = self.db.delete_user(user_id)
        if result.get("Success"):
            return {"Success": True, "message": "User deleted Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.get('error')}"}

class CategoryLogic:
    def __init__(self):
    #Create a databse manager instance (this will handle all the db operations)
        self.db = DatabaseManager()
        
    #----------Create----------
    def create_category(self, name):
        """ Add a new category to the database."""
        return self.db.add_category(name)
    
    #---------Read----------
    def fetch_all_categories(self):
        """ Fetch all categories from the database."""
        return self.db.get_all_categories()
    def fetch_category_by_id(self, category_id):
        """ Fetch a category by ID from the database."""
        return self.db.get_category_by_id(category_id)
    
    #---------Update----------
    def modify_category(self, category_id, updated_name):
        """ Update category details in the database."""
        result = self.db.update_category(category_id, updated_name)
        if result.get("Success"):
            return {"Success": True, "message": "Category updated Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.get('error')}"}
    
    #---------Delete----------
    def remove_category(self, category_id):
        """ Delete a category from the database."""
        result = self.db.delete_category(category_id)
        if result.get("Success"):
            return {"Success": True, "message": "Category deleted Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.get('error')}"}        

class Transaction:
    def __init__(self):
        # Create a database manager instance (handles all DB operations)
        self.db = DatabaseManager()

    #----------Create----------
    def create_transaction(self, user_id, category_id, t_type, amount, description=None, date=None, receipt_url=None):
        """ Add a new transaction to the database. """
        if not user_id or not category_id or not t_type or not amount:
            return {"Success": False, "message": "User ID, Category ID, Type, and Amount are required."}
        result = self.db.add_transaction(user_id, category_id, t_type, amount, description, date, receipt_url)
        if hasattr(result, 'error') and result.error:
            return {"Success": False, "message": str(result.error)}
        return {"Success": True, "data": result.data}

    #---------Read----------
    def fetch_all_transactions(self, limit=100, offset=0):
        """ Fetch all transactions from the database. """
        result = self.db.get_all_transactions(limit=limit, offset=offset)
        if hasattr(result, 'error') and result.error:
            return {"Success": False, "message": str(result.error)}
        return {"Success": True, "data": result.data}

    def fetch_transaction_by_id(self, transaction_id):
        """ Fetch a transaction by ID from the database. """
        result = self.db.get_transaction_by_id(transaction_id)
        if hasattr(result, 'error') and result.error:
            return {"Success": False, "message": str(result.error)}
        return {"Success": True, "data": result.data}

    #--------Update----------
    def modify_transaction(self, transaction_id, category_id=None, t_type=None, amount=None, description=None):
        """ Update transaction details in the database. """
        result = self.db.update_transaction(
            transaction_id,
            category_id=category_id,
            t_type=t_type,
            amount=amount,
            description=description
        )
        if hasattr(result, 'error') and result.error:
            return {"Success": False, "message": str(result.error)}
        return {"Success": True, "data": result.data}

    #--------Delete----------
    def remove_transaction(self, transaction_id):
        """ Delete a transaction from the database. """
        result = self.db.delete_transaction(transaction_id)
        if hasattr(result, 'error') and result.error:
            return {"Success": False, "message": str(result.error)}
        return {"Success": True, "message": "Transaction deleted successfully!"}


from datetime import date, datetime        
class BudgetsLogic:
    def __init__(self):
        #Create a databse manager instance (this will handle all the db operations)
        self.db = DatabaseManager()
        
    #----------Create----------
    def create_budget(self, user_id, category_id, amount, month=None):
        """
        Create a new budget for a user and category.
        If month is None, defaults to the first day of the current month.
        Accepts 'YYYY-MM' format from API and converts to DATE.
        """
        if month is None:
            # default to first day of current month
            month = date.today().replace(day=1)
        else:
            # convert 'YYYY-MM' string to a proper date object
            try:
                month = datetime.strptime(month, "%Y-%m").date().replace(day=1)
            except ValueError:
                return {"Success": False, "message": "Invalid month format. Use 'YYYY-MM'."}

        return self.db.add_budget(user_id, category_id, amount, month)

    #---------Read----------
    def fetch_all_budgets(self, user_id=None): 
        """ Fetch all budgets from the database."""
        return self.db.get_all_budgets(user_id)
    def fetch_budget_by_id(self, budget_id):
        """ Fetch a budget by ID from the database."""
        return self.db.get_budget_by_id(budget_id)
    
    #--------Update----------
    def modify_budget(self, budget_id, category_id=None, amount=None, month=None):
        """ Update budget details in the database."""
        result = self.db.update_budget(budget_id, category_id, amount, month)
        if result.get("Success"):
            return {"Success": True, "message": "Budget updated Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.get('error')}"}
        
        
    #--------Delete----------
    def remove_budget(self, budget_id):
        """ Delete a budget from the database."""
        result = self.db.delete_budget(budget_id)
        if result.get("Success"):
            return {"Success": True, "message": "Budget deleted Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.get('error')}"}


class SavingGoals:

    #Create a databse manager instance (this will handle all the db operations)
    def __init__(self):       
        self.db = DatabaseManager()     
    #----------Create----------
    def create_saving_goal(self, user_id, name, target_amount, saved_amount=0.0, deadline=None, status="active"):
        return self.db.add_saving_goal(
            user_id=user_id,
            name=name,
            target_amount=target_amount,
            saved_amount=saved_amount,
            target_date=deadline,  # 👈 maps API "deadline" to DB "target_date"
            status=status
        )

    #--------Read----------
    def fetch_all_saving_goals(self, user_id=None):
        """ Fetch all saving goals from the database."""
        return self.db.get_all_saving_goals(user_id)
    def fetch_saving_goal_by_id(self, goal_id):
        """ Fetch a saving goal by ID from the database."""
        return self.db.get_saving_goal_by_id(goal_id)
    
    #--------Update----------
    def modify_saving_goal(self, goal_id, name=None, target_amount=None, saved_amount=None, target_date=None, status=None):
        """ Update saving goal details in the database."""
        result = self.db.update_saving_goal(goal_id, name, target_amount, saved_amount, target_date, status)
        if result.get("Success"):
            return {"Success": True, "message": "Saving Goal updated Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.get('error')}"}
        
    #--------Delete----------
    def remove_saving_goal(self, goal_id):
        """ Delete a saving goal from the database."""
        result = self.db.delete_saving_goal(goal_id)
        if result.get("Success"):
            return {"Success": True, "message": "Saving Goal deleted Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.get('error')}"}


