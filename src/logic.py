# src/logic.py
from src.db import DatabaseManager
from datetime import date, datetime

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
        # Handle Supabase insert response
        if isinstance(result, dict):  # duplicate or error caught
            return result
        elif result.data:
            return {"Success": True, "message": "User added successfully!", "data": result.data}
        else:
            return {"Success": False, "message": "Failed to add user"}
        
    #---------Read----------
    def fetch_all_users(self):
        """ Fetch all users from the database."""
        result = self.db.get_all_users()
        if result.data is not None:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    def fetch_user_by_id(self, user_id):
        """ Fetch a user by ID from the database."""
        result = self.db.get_user_by_id(user_id)
        if result.data:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    #---------Update----------
    def modify_user(self, user_id, email=None, name=None):
        """ Update user details in the database."""
        result = self.db.update_user(user_id, email, name)
        if result.data:
            return {"Success": True, "message": "User updated Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
        
    #---------Delete----------
    def remove_user(self, user_id):
        """ Delete a user from the database."""
        result = self.db.delete_user(user_id)
        if result.data:
            return {"Success": True, "message": "User deleted Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

class CategoryLogic:
    def __init__(self):
        #Create a databse manager instance (this will handle all the db operations)
        self.db = DatabaseManager()
        
    #----------Create----------
    def create_category(self, name):
        """ Add a new category to the database."""
        result = self.db.add_category(name)
        if result.data:
            return {"Success": True, "message": "Category added successfully!", "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    #---------Read----------
    def fetch_all_categories(self):
        """ Fetch all categories from the database."""
        result = self.db.get_all_categories()
        if result.data is not None:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    def fetch_category_by_id(self, category_id):
        """ Fetch a category by ID from the database."""
        result = self.db.get_category_by_id(category_id)
        if result.data:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    #---------Update----------
    def modify_category(self, category_id, updated_name):
        """ Update category details in the database."""
        result = self.db.update_category(category_id, updated_name)
        if result.data:
            return {"Success": True, "message": "Category updated Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    #---------Delete----------
    def remove_category(self, category_id):
        """ Delete a category from the database."""
        result = self.db.delete_category(category_id)
        if result.data:
            return {"Success": True, "message": "Category deleted Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}        

class TransactionLogic:
    def __init__(self):
        # Create a database manager instance (handles all DB operations)
        self.db = DatabaseManager()

    #----------Create----------
    def create_transaction(self, user_id, category_id, t_type, amount, description=None, date=None, receipt_url=None):
        """ Add a new transaction to the database. """
        if not user_id or not category_id or not t_type or not amount:
            return {"Success": False, "message": "User ID, Category ID, Type, and Amount are required."}
        
        result = self.db.add_transaction(user_id, category_id, t_type, amount, description, date, receipt_url)
        if result.data:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

    #---------Read----------
    def fetch_all_transactions(self, limit=100, offset=0):
        """ Fetch all transactions from the database. """
        result = self.db.get_all_transactions(limit=limit, offset=offset)
        if result.data is not None:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

    def fetch_transaction_by_id(self, transaction_id):
        """ Fetch a transaction by ID from the database. """
        result = self.db.get_transaction_by_id(transaction_id)
        if result.data:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

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
        if result.data:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

    #--------Delete----------
    def remove_transaction(self, transaction_id):
        """ Delete a transaction from the database. """
        result = self.db.delete_transaction(transaction_id)
        if result.data:
            return {"Success": True, "message": "Transaction deleted successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}


class BudgetsLogic:
    def __init__(self):
        self.db = DatabaseManager()
        
    #----------Create----------
    def create_budget(self, user_id, category_id, amount, month=None):
        """
        Create a new budget for a user and category.
        """
        # Handle default month
        if month is None:
            today = date.today()
            month = date(today.year, today.month, 1)
        
        # Handle string month input (from Streamlit)
        if isinstance(month, str):
            try:
                # Try parsing as YYYY-MM-DD format
                if len(month) == 10:  # YYYY-MM-DD
                    month = datetime.strptime(month, '%Y-%m-%d').date()
                elif len(month) == 7:  # YYYY-MM
                    month = datetime.strptime(month + '-01', '%Y-%m-%d').date()
                else:
                    return {"Success": False, "message": "Invalid month format. Use YYYY-MM-DD or YYYY-MM"}
            except ValueError as e:
                return {"Success": False, "message": f"Invalid month format: {str(e)}"}
        
        # Ensure month is first day of month
        if not isinstance(month, date):
            return {"Success": False, "message": "Month must be a date object."}

        # Ensure month is first day of the month
        month = date(month.year, month.month, 1)

        # Call database
        result = self.db.add_budget(user_id, category_id, amount, month)
        if result.data:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

    # Also update the modify_budget method
    def modify_budget(self, budget_id, category_id=None, amount=None, month=None):
        """ Update budget details in the database."""
        # Handle string month input if provided
        if month and isinstance(month, str):
            try:
                if len(month) == 10:  # YYYY-MM-DD
                    month = datetime.strptime(month, '%Y-%m-%d').date()
                elif len(month) == 7:  # YYYY-MM
                    month = datetime.strptime(month + '-01', '%Y-%m-%d').date()
                # Ensure it's first day of month
                month = date(month.year, month.month, 1)
            except ValueError:
                return {"Success": False, "message": "Invalid month format"}
        
        result = self.db.update_budget(budget_id, category_id, amount, month)
        if result.data:
            return {"Success": True, "message": "Budget updated Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

    #---------Read----------
    def fetch_all_budgets(self, user_id=None): 
        """ Fetch all budgets from the database."""
        result = self.db.get_all_budgets(user_id)
        if result.data is not None:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    def fetch_budget_by_id(self, budget_id):
        """ Fetch a budget by ID from the database."""
        result = self.db.get_budget_by_id(budget_id)
        if result.data:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
        
    #--------Delete----------
    def remove_budget(self, budget_id):
        """ Delete a budget from the database."""
        result = self.db.delete_budget(budget_id)
        if result.data:
            return {"Success": True, "message": "Budget deleted Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
        
     # check budget limits
    def check_budget_limits(self, user_id, month=None):
        """Check if spending exceeds budget limits for each category"""
        if month is None:
            today = date.today()
            month = date(today.year, today.month, 1)
        
        month_str = month.isoformat() if isinstance(month, date) else month
        
        # Get all budgets for the user and month
        budgets = self.db.get_all_budgets(user_id)
        if not budgets.data:
            return {"Success": True, "data": []}
        
        # Get transactions for the month
        transactions = self.db.get_monthly_transactions(user_id, month.year, month.month)
        
        results = []
        for budget in budgets.data:
            if budget['month'].startswith(month_str[:7]):  # Compare YYYY-MM
                category_id = budget['category_id']
                budget_amount = budget['amount']
                
                # Calculate total expenses for this category in the month
                category_expenses = sum(
                    t['amount'] for t in transactions.data 
                    if t['category_id'] == category_id and t['type'] == 'expense'
                )
                
                results.append({
                    'category_id': category_id,
                    'budget_amount': budget_amount,
                    'spent_amount': category_expenses,
                    'remaining_amount': budget_amount - category_expenses,
                    'exceeded': category_expenses > budget_amount,
                    'percentage_used': (category_expenses / budget_amount * 100) if budget_amount > 0 else 0
                })
        
        return {"Success": True, "data": results}


class SavingGoalsLogic:
    def __init__(self):       
        self.db = DatabaseManager()     
    
    #----------Create----------
    def create_saving_goal(self, user_id, name, target_amount, saved_amount=0.0, deadline=None, status="active"):
        result = self.db.add_saving_goal(
            user_id=user_id,
            name=name,
            target_amount=target_amount,
            saved_amount=saved_amount,
            target_date=deadline,  # 👈 maps API "deadline" to DB "target_date"
            status=status
        )
        if result.data:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

    #--------Read----------
    def fetch_all_saving_goals(self, user_id=None):
        """ Fetch all saving goals from the database."""
        result = self.db.get_all_saving_goals(user_id)
        if result.data is not None:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    def fetch_saving_goal_by_id(self, goal_id):
        """ Fetch a saving goal by ID from the database."""
        result = self.db.get_saving_goal_by_id(goal_id)
        if result.data:
            return {"Success": True, "data": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    #--------Update----------
    def modify_saving_goal(self, goal_id, name=None, target_amount=None, saved_amount=None, target_date=None, status=None):
        """ Update saving goal details in the database."""
        result = self.db.update_saving_goal(goal_id, name, target_amount, saved_amount, target_date, status)
        if result.data:
            return {"Success": True, "message": "Saving Goal updated Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
        
    #--------Delete----------
    def remove_saving_goal(self, goal_id):
        """ Delete a saving goal from the database."""
        result = self.db.delete_saving_goal(goal_id)
        if result.data:
            return {"Success": True, "message": "Saving Goal deleted Successfully!"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}