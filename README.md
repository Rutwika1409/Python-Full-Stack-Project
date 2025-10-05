
```markdown
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
├── src/                # Core application logic
│   ├── logic.py        # Business logic and tasks
│   └── db.py           # Database operations
├── api/                # Backend API
│   └── main.py         # FastAPI endpoints
├── frontend/           # Frontend application
│   └── app.py          # Streamlit web interface
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .env                # Environment variables

---

## Quick Start

### Prerequisites
- Python 3.8 or higher  
- A Supabase account  
- Git (optional for cloning)  

### 1. Clone or Download the Project

**Option 1: Clone with Git**
```bash
git clone https://github.com/Rutwika1409/Python-Full-Stack-Project.git
````

**Option 2: Download ZIP**

* Extract the ZIP file to your local machine.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Supabase Database

1. Create a Supabase project.
2. Create the tables via the SQL editor with the following commands:

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT
);

-- Categories
CREATE TABLE categories (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL
);

-- Transactions
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

-- Budgets
CREATE TABLE budgets (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    month DATE NOT NULL,
    amount NUMERIC NOT NULL
);

-- Savings Goals
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

3. **Get your credentials** for the `.env` file.

---

### 4. Configure Environment Variables

1. Create a `.env` file in the project root.
2. Add your Supabase credentials:

```env
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
```

---

### 5. Run the Application

**Streamlit Frontend**

```bash
streamlit run frontend/app.py
```

* The app opens in your browser at `http://localhost:8501`.

**FastAPI Backend**

```bash
cd api
python main.py
```

* API available at `http://localhost:8000`.

---

## How to Use FinTrack

1. **Sign Up / Login**

   * Open the Streamlit app.
   * Create an account or log in with your email.

2. **Add Categories**

   * Predefined categories exist (Food, Transport, Salary).
   * You can add, edit, or remove categories.

3. **Track Transactions**

   * Add `income` or `expense` transactions with amount, category, date, and optional description/receipt.
   * Edit or delete transactions as needed.

4. **Plan Budgets**

   * Set monthly budgets per category.
   * Compare actual spending with planned budgets.

5. **Set Savings Goals**

   * Create goals with target amount and deadline.
   * Track saved amount and goal status (active, completed, paused).

6. **View Dashboard**

   * See charts of spending, income, and savings progress.

---

## Technical Details

### Technologies Used

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **Database:** Supabase (PostgreSQL)
* **Language:** Python 3.8+

### Key Components

1. **`src/db.py`** – Database operations (CRUD).
2. **`src/logic.py`** – Business logic (budgets, savings, transactions).
3. **`api/main.py`** – FastAPI endpoints.
4. **`frontend/app.py`** – Streamlit frontend.
5. **`.env`** – Environment variables for Supabase.
6. **`requirements.txt`** – Python dependencies.

---

## Troubleshooting

### Common Issues

1. **"Module not found" errors**

   * Ensure dependencies are installed: `pip install -r requirements.txt`
   * Run commands from the correct project directory.

---

## Future Enhancements

* **Multi-Currency Support**
* **Recurring Transactions**
* **Notifications & Reminders**
* **Advanced Analytics**
* **Mobile App Version**
* **Collaborative Budgeting**
* **Custom Categories & Tags**
* **Export & Reports (PDF/CSV)**

---

## Support

For questions or issues, contact: `rutwikagoparaju1409@gmail.com`

