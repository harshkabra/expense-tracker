import sqlite3


def get_connection():
    conn = sqlite3.connect("expenses.db")
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense_db(name, amount, category, expense_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (name, amount, category, date)
        VALUES (?, ?, ?, ?)
    """, (name, amount, category, str(expense_date)))

    conn.commit()
    conn.close()


def get_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
    """)

    expenses = cursor.fetchall()

    conn.close()
    return expenses


def search_expense_db(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        WHERE LOWER(name) = LOWER(?)
    """, (name,))

    expenses = cursor.fetchall()

    conn.close()
    return expenses


def update_expense_db(expense_id, name, amount, category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET name = ?, amount = ?, category = ?
        WHERE id = ?
    """, (name, amount, category, expense_id))

    updated = cursor.rowcount

    conn.commit()
    conn.close()

    return updated


def delete_expense_db(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted


def get_total_expense():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
    """)

    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total


def get_category_wise_total():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT LOWER(category), SUM(amount)
        FROM expenses
        GROUP BY LOWER(category)
    """)

    result = cursor.fetchall()

    conn.close()
    return result


create_table()