# Frontend ---> API ---> Logic ---> Database ---> Response

# API handles requests and responses,
# Logic processes data and interacts with Database.

#api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# Import Taskmanager from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import UserLogic, CategoryLogic, TransactionLogic, BudgetsLogic, SavingGoals



#----------App Setup----------
app = FastAPI(title="FinTrack API", version="1.0")

#----------Allow frontend (Streamlit/React) to call the API----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (frontend apps)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc)
    allow_headers=["*"],  # Allows all headers
    )


#Creating an instance (this will handle all the logic operations)
user_logic = UserLogic()
category_logic = CategoryLogic()
transaction_logic = TransactionLogic()
budgets_logic = BudgetsLogic()
saving_goals_logic = SavingGoals()


#----------Data Models----------
#USER
class User(BaseModel):
    """Schema for creating a new user."""
    email: str
    name: str

class UserUpdate(BaseModel):
    """ Schema for updating user details."""
    email: str | None = None
    name: str | None = None

#CATEGORY
class Category(BaseModel):
    """Schema for creating a new category."""
    name: str

class CategoryUpdate(BaseModel):
    name: str | None = None

#TRANSACTION
class Transaction(BaseModel):
    """Schema for creating a new transaction."""
    user_id: str
    category_id: str
    type: str  # 'income' or 'expense'
    amount: float
    description: str | None = None
    date: str | None = None  # ISO format date string
    receipt_url: str | None = None
class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    category_id: str | None = None
    type: str | None = None  # 'income' or 'expense'
    amount: float | None = None
    description: str | None = None


#BUDGET
class Budget(BaseModel):
    """Schema for creating a new budget."""
    user_id: str
    category_id: str
    amount: float
    month: str  # Format: 'YYYY-MM'
class BudgetUpdate(BaseModel):
    """Schema for updating a budget."""
    category_id: str | None = None
    amount: float | None = None
    month: str | None = None  # Format: 'YYYY-MM'


#SAVING GOAL
class SavingGoal(BaseModel):
    """Schema for creating a new saving goal."""
    user_id: str
    name: str
    target_amount: float
    saved_amount: float = 0.0
    deadline: str  # ISO format date string
    status: str  # 'active', 'completed', 'paused'
class SavingGoalUpdate(BaseModel):
    """Schema for updating a saving goal."""
    name: str | None = None
    target_amount: float | None = None
    saved_amount: float | None = None
    deadline: str | None = None  # ISO format date string
    status: str | None = None  # 'active', 'completed', 'paused'


#----------User Endpoints----------
@app.get("/")
def home():
    """
    Check if API is running.
    """
    return {"message": "FinTrack API is running!"}
@app.get("/users")
def get_users():
    """
    Fetch all users.
    """
    return user_logic.fetch_all_users()
@app.post("/users")
def create_user(user: User):
    """
    Create a new user.
    """
    result = user_logic.create_user(user.email, user.name)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail = result.get("message"))
    return result
@app.put("/users/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    """
    Update user details.
    """
    result = user_logic.modify_user(user_id, email=user.email, name=user.name) if user.email or user.name else user_logic.modify_user(user_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    """
    Delete a user.
    """
    result = user_logic.remove_user(user_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result



#----------Category Endpoints----------
@app.get("/categories")
def get_categories():
    """Fetch all categories."""
    return category_logic.fetch_all_categories()

@app.post("/categories")
def create_category(category: Category):
    """Create a new Category."""
    result = category_logic.create_category(category.name)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.put("/categories/{category_id}")
def update_category(category_id: str, category: CategoryUpdate):
    """Update category details."""
    result = category_logic.modify_category(
        category_id, 
        name=category.name
    ) if category.name else category_logic.modify_category(category_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/categories/{category_id}")
def delete_category(category_id: str):
    """Delete a category."""
    result = category_logic.remove_category(category_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result



#----------Transaction Endpoints----------
@app.get("/transactions")
def get_transactions():
    return transaction_logic.fetch_all_transactions()
@app.post("/transactions")
def create_transaction(transaction: Transaction):
    result = transaction_logic.create_transaction(
        user_id = transaction.user_id,
        category_id = transaction.category_id,
        t_type = transaction.type,
        amount = transaction.amount,
        description = transaction.description,
        date = transaction.date,        
        receipt_url= transaction.receipt_url
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: str, transaction: TransactionUpdate):
    result = transaction_logic.modify_transaction(
        transaction_id,
        category_id = transaction.category_id,
        t_type = transaction.type,
        amount = transaction.amount,
        description = transaction.description
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: str):
    result = transaction_logic.remove_transaction(transaction_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


#----------Budget Endpoints----------
@app.get("/budgets")
def get_budgets(user_id: str | None = None):
    """Fetch all budgets, optionally filtered by user_id."""
    return budgets_logic.fetch_all_budgets(user_id)
@app.post("/budgets")
def create_budget(budget: Budget):
    result = budgets_logic.create_budget(
        user_id = budget.user_id,
        category_id = budget.category_id,
        amount = budget.amount,
        month = budget.month
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.put("/budgets/{budget_id}")
def update_budget(budget_id: str, budget: BudgetUpdate):
    result = budgets_logic.modify_budget(
        budget_id,
        category_id = budget.category_id,
        amount = budget.amount,
        month = budget.month
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.delete("/budgets/{budget_id}")
def delete_budget(budget_id: str):
    result = budgets_logic.remove_budget(budget_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


#----------Saving Goals Endpoints----------
@app.get("/saving_goals")
def get_saving_goals(user_id: str | None = None):
    """Fetch all saving goals, optionally filtered by user_id."""
    return saving_goals_logic.fetch_all_saving_goals(user_id)

@app.post("/saving_goals")
def create_saving_goal(saving_goal: SavingGoal):
    result = saving_goals_logic.create_saving_goal(
        user_id = saving_goal.user_id,
        name = saving_goal.name,
        target_amount = saving_goal.target_amount,
        saved_amount = saving_goal.saved_amount,
        target_date = saving_goal.deadline,
        status = saving_goal.status
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.put("/saving_goals/{goal_id}")
def update_saving_goal(goal_id: str, saving_goal: SavingGoalUpdate):
    result = saving_goals_logic.modify_saving_goal(
        goal_id,
        name = saving_goal.name,
        target_amount = saving_goal.target_amount,
        saved_amount = saving_goal.saved_amount,
        target_date = saving_goal.deadline,
        status = saving_goal.status
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.delete("/saving_goals/{goal_id}")
def delete_saving_goal(goal_id: str):
    result = saving_goals_logic.remove_saving_goal(goal_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


#----------Run----------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
