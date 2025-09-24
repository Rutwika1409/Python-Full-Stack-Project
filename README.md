# FinTrack

## Project Description
**FinTrack** is a full-stack web application designed to help users manage their personal finances effectively. It allows users to **track income and expenses**, **plan monthly budgets by category**, and **save for specific goals** such as trips, gadgets, or emergency funds. Users can see a clear overview of their financial health, monitor spending patterns, and track progress toward their savings goals.

This project demonstrates full-stack development skills using **Python for the backend**, **Supabase** as the database and authentication layer, and a modern frontend with **Streamlit**.

---

## Features
- **User Authentication:** Sign up, login, and manage your profile (via Supabase Auth).  
- **Income & Expense Tracking:** Add, edit, and view transactions with optional receipts.  
- **Budget Planning:** Set monthly budgets for categories and monitor spending.  
- **Savings Goals:** Create goals (e.g., trip, gadget) and track progress toward each goal.  
- **Category Management:** Organize transactions into categories like Food, Transport, or Salary.  
- **Analytics & Visualization:** Interactive charts to analyze spending patterns and goal progress.  
- **Real-time Dashboard:** Get a clear overview of financial health in one place.   

---

## Project Structure
FINTRACK/
|
|---src/            # Core application logic
|   |---logic.py    # Business logic and task
|   |__db.py        # Database operations
|
|---api/            # Backend API
|   |__main.py      # FastAPI endpoints
|
|---frontend/       # Frontend application
|   |__app.py       # Streamlit web interface
|
|___requirements.txt    # Python Dependencies
|
|___README.md       # Project Documentation
|
|___.env            # Python Variables

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git (Push, Cloning)

### 1. Clone or Download the Project
# Option 1: Clone with Git
git clone [<repository-url>](https://github.com/Rutwika1409/Python-Full-Stack-Project.git)

# Option 2: Download and extract the ZIP file

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Set Up Supabase Database
1) create a supabase project
2) create the task table
-go to sql editor in your supabase dashboard
- run this sql command:

```
sql:
-- 1) Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT
);

-- 2) Categories
CREATE TABLE categories (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL
);

-- 3) Transactions
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    type TEXT CHECK (type IN ('income', 'expense')),
    amount NUMERIC NOT NULL,
    description TEXT,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    receipt_url TEXT
);

-- 4) Budgets
CREATE TABLE budgets (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    month DATE NOT NULL,
    amount NUMERIC NOT NULL
);

-- 5) Savings Goals
CREATE TABLE savings_goals (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    target_amount NUMERIC NOT NULL,
    saved_amount NUMERIC DEFAULT 0,
    target_date DATE NOT NULL,
    status TEXT CHECK (status IN ('active', 'completed', 'paused')) DEFAULT 'active'
);


```
3) **Get Your Credentials:

### 4. Configure Environment Variables

1. Create a `.env` file in the project root

2. Add your Supabase credentials to `.env`:
SUPABASE_URL = your_project_url
SUPABASE_KEY = your_anon_key

### 5. Run the Application

## Streamlit Frontend
streamlit run frontend/app.py

The app will open in your browser at `http://localhost:8501`

## FastAPI Backend
cd api
python main.py

The API will be available at `http://localhost:8000`

## How to use

For a README, you don’t need to be *this* detailed. You can condense it so that it’s clear, readable, and doesn’t overwhelm the reader. Here’s a shorter version for the **“How to Use”** section:

---

## How to Use FinTrack

1. **Sign Up / Login**

   * Open the Streamlit app:

     ```bash
     streamlit run frontend/app.py
     ```
   * Create an account or log in with your email.

2. **Add Categories**

   * Predefined categories exist (Food, Transport, Salary).
   * You can also add, edit, or remove categories.

3. **Track Transactions**

   * Add `income` or `expense` transactions with amount, category, date, and optional description or receipt.
   * Edit or delete transactions as needed.

4. **Plan Budgets**

   * Set monthly budgets for each category.
   * Compare actual spending with planned budgets.

5. **Set Savings Goals**

   * Create goals (e.g., trip, gadget) with target amount and deadline.
   * Track saved amount and goal status: active, completed, or paused.

6. **View Dashboard**

   * See charts of spending, income, and savings progress.

## Technical details

### Technologies Used
- **Frontend:** Streamlit  (Python web framework)
- **Backend:** FastAPI  (Python REST API framework)
- **Database:** Supabase (PostgreSQL-based backend-as-a-service)  
- **Language:** Python 3.8+

### Key Components
1. **`src/db.py`** – Handles all database operations (CRUD) and interactions with Supabase.

2. **`src/logic.py`** – Contains business logic, such as calculating budget usage, savings progress, and transaction summaries.

3. **`api/main.py`** – FastAPI endpoints for the backend API (transactions, budgets, goals, users).

4. **`frontend/app.py`** – Streamlit frontend for user interaction, dashboards, and visualizations.

5. **`.env`** – Environment variables for Supabase credentials and configuration.

6. **`requirements.txt`** – Python dependencies needed to run the project.


## Troubleshooting

## Common Issues

1. **"Module not found" errors**
    -Make sure you've installed all dependencies: `pip install -r requirements.txt`
    -Check that you're running commands from the correct directory


## Future Enhancements

- **Multi-Currency Support:** Track and convert transactions in multiple currencies.
- **Recurring Transactions:** Automatically log recurring income or expenses.
- **Notifications & Reminders:** Alerts for upcoming bills, budget limits, or goal deadlines.
- **Advanced Analytics:** Predictive insights and spending trends.
- **Mobile App Version:** Mobile-friendly interface or native app.
- **Collaborative Budgeting:** Share budgets and goals with family or roommates.
- **Custom Categories & Tags:** Nested categories or tags for flexible tracking.
- **Export & Reports:** Generate PDF/CSV reports for budgets, transactions, and savings goals.

## Support
<<<<<<< HEAD
if you encounter any issues or have questions: "rutwikagoparaju1409@gmail.com"
=======
if you encounter any issues or have questions: `rutwikagoparaju1409@gmail.com`
>>>>>>> a0a1190 (First commit)







