from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import (
    add_expense_db,
    get_all_expenses,
    search_expense_db,
    update_expense_db,
    delete_expense_db,
    get_total_expense,
    get_category_wise_total
)

app = FastAPI(title="Expense Tracker API")


# ===============================
# CORS CONFIGURATION
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===============================
# EXPENSE MODEL
# ===============================

class Expense(BaseModel):
    name: str
    amount: float
    category: str
    date: str


# ===============================
# HOME
# ===============================

@app.get("/")
def home():
    return {
        "message": "Expense Tracker API is running"
    }


# ===============================
# GET ALL EXPENSES
# ===============================

@app.get("/expenses")
def get_expenses():

    records = get_all_expenses()

    expenses = []

    for record in records:

        expenses.append({
            "id": record[0],
            "name": record[1],
            "amount": record[2],
            "category": record[3],
            "date": record[4]
        })

    return expenses


# ===============================
# SEARCH EXPENSE
# ===============================

@app.get("/expenses/search/{name}")
def search_expense(name: str):

    records = search_expense_db(name)

    if not records:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    expenses = []

    for record in records:

        expenses.append({
            "id": record[0],
            "name": record[1],
            "amount": record[2],
            "category": record[3],
            "date": record[4]
        })

    return expenses


# ===============================
# TOTAL EXPENSE
# ===============================

@app.get("/expenses/summary/total")
def total_expense():

    total = get_total_expense()

    return {
        "total_expense": total
    }


# ===============================
# CATEGORY-WISE TOTAL
# ===============================

@app.get("/expenses/summary/category")
def category_wise_total():

    records = get_category_wise_total()

    result = []

    for category, total in records:

        result.append({
            "category": category,
            "total": total
        })

    return result


# ===============================
# ADD EXPENSE
# ===============================

@app.post(
    "/expenses",
    status_code=status.HTTP_201_CREATED
)
def add_expense(expense: Expense):

    if not expense.name.strip():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expense name cannot be empty"
        )

    if expense.amount <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0"
        )

    if not expense.category.strip():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category cannot be empty"
        )

    add_expense_db(
        expense.name,
        expense.amount,
        expense.category,
        expense.date
    )

    return {
        "message": "Expense added successfully"
    }


# ===============================
# UPDATE EXPENSE
# ===============================

@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    expense: Expense
):

    if not expense.name.strip():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expense name cannot be empty"
        )

    if expense.amount <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0"
        )

    if not expense.category.strip():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category cannot be empty"
        )

    updated = update_expense_db(
        expense_id,
        expense.name,
        expense.amount,
        expense.category
    )

    if updated == 0:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return {
        "message": "Expense updated successfully"
    }


# ===============================
# DELETE EXPENSE
# ===============================

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    deleted = delete_expense_db(expense_id)

    if deleted == 0:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully"
    }


# ===============================
# GET EXPENSE BY ID
# ===============================

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):

    records = get_all_expenses()

    for record in records:

        if record[0] == expense_id:

            return {
                "id": record[0],
                "name": record[1],
                "amount": record[2],
                "category": record[3],
                "date": record[4]
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found"
    )