from datetime import date
import pandas as pd

from database import (
    add_expense_db,
    get_all_expenses,
    search_expense_db,
    delete_expense_db,
    get_total_expense,
    get_category_wise_total
)


# ============================================================
#                    EXPENSE CLASS
# ============================================================

class Expense:

    def __init__(self, expense_id, name, amount, category, expense_date):

        self.id = expense_id
        self.name = name
        self.amount = amount
        self.category = category
        self.date = expense_date

    def display(self):

        print(f"ID       : {self.id}")
        print(f"Name     : {self.name}")
        print(f"Amount   : ₹{self.amount}")
        print(f"Category : {self.category}")
        print(f"Date     : {self.date}")

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_amount(self):
        return self.amount

    def get_category(self):
        return self.category

    def get_date(self):
        return self.date

    def update_name(self, name):

        if name.strip():
            self.name = name

    def update_amount(self, amount):

        if amount > 0:
            self.amount = amount

    def update_category(self, category):

        if category.strip():
            self.category = category


# ============================================================
#                    EXPENSE LIST
# ============================================================

expenses = []


# ============================================================
#                    LOAD EXPENSES
# ============================================================

def load_expenses():

    expenses.clear()

    records = get_all_expenses()

    for record in records:

        expense = Expense(
            record[0],
            record[1],
            record[2],
            record[3],
            record[4]
        )

        expenses.append(expense)


# ============================================================
#                    ADD EXPENSE
# ============================================================

def add_expenses():

    print("\n" + "=" * 60)
    print("                     ADD EXPENSE")
    print("=" * 60)

    name = input("Enter expense name: ").strip()

    if not name:

        print("Expense name cannot be empty.")
        return

    try:

        amount = float(input("Enter amount: "))

        if amount <= 0:

            print("Amount must be greater than 0.")
            return

    except ValueError:

        print("Please enter a valid amount.")
        return

    category = input("Enter category: ").strip()

    if not category:

        print("Category cannot be empty.")
        return

    expense_date = date.today()

    add_expense_db(
        name,
        amount,
        category,
        expense_date
    )

    print("\nExpense added successfully!")

    load_expenses()


# ============================================================
#                    VIEW EXPENSES
# ============================================================

def view_expenses():

    print("\n" + "=" * 60)
    print("                    ALL EXPENSES")
    print("=" * 60)

    records = get_all_expenses()

    if not records:

        print("No expenses found.")
        return

    print(
        f"{'ID':<8}"
        f"{'Name':<20}"
        f"{'Amount':<12}"
        f"{'Category':<15}"
        f"{'Date':<12}"
    )

    print("-" * 67)

    for record in records:

        print(
            f"{record[0]:<8}"
            f"{record[1]:<20}"
            f"₹{record[2]:<11}"
            f"{record[3]:<15}"
            f"{record[4]:<12}"
        )


# ============================================================
#                    SEARCH EXPENSE
# ============================================================

def search_expense():

    print("\n" + "=" * 60)
    print("                   SEARCH EXPENSE")
    print("=" * 60)

    name = input("Enter expense name: ").strip()

    records = search_expense_db(name)

    if not records:

        print("Expense not found.")
        return

    print("\nExpense Found!")

    print("-" * 60)

    for record in records:

        expense = Expense(
            record[0],
            record[1],
            record[2],
            record[3],
            record[4]
        )

        expense.display()

        print("-" * 60)


# ============================================================
#                    DELETE EXPENSE
# ============================================================

def delete_expense():

    print("\n" + "=" * 60)
    print("                   DELETE EXPENSE")
    print("=" * 60)

    records = get_all_expenses()

    if not records:

        print("No expenses found.")
        return

    print(
        f"{'ID':<8}"
        f"{'Name':<20}"
        f"{'Amount':<12}"
        f"{'Category':<15}"
    )

    print("-" * 55)

    for record in records:

        print(
            f"{record[0]:<8}"
            f"{record[1]:<20}"
            f"₹{record[2]:<11}"
            f"{record[3]:<15}"
        )

    try:

        expense_id = int(
            input("\nEnter expense ID to delete: ")
        )

    except ValueError:

        print("Please enter a valid numeric ID.")
        return

    deleted = delete_expense_db(expense_id)

    if deleted == 0:

        print("Expense not found.")

    else:

        print("Expense deleted successfully!")

        load_expenses()


# ============================================================
#                    TOTAL EXPENSE
# ============================================================

def total_expense():

    print("\n" + "=" * 60)
    print("                    TOTAL EXPENSE")
    print("=" * 60)

    total = get_total_expense()

    print(f"Total Expense: ₹{total}")


# ============================================================
#                 CATEGORY-WISE TOTAL
# ============================================================

def category_wise_total():

    print("\n" + "=" * 60)
    print("                 CATEGORY-WISE TOTAL")
    print("=" * 60)

    records = get_category_wise_total()

    if not records:

        print("No expenses found.")
        return

    for category, total in records:

        print(
            f"{category.capitalize():<20}"
            f"₹{total}"
        )


# ============================================================
#                    SHOW DATAFRAME
# ============================================================

def show_dataframe():

    records = get_all_expenses()

    if not records:

        return

    df = pd.DataFrame(
        records,
        columns=[
            "ID",
            "Name",
            "Amount",
            "Category",
            "Date"
        ]
    )

    print("\n" + "=" * 60)
    print("                    DATAFRAME")
    print("=" * 60)

    print(df)