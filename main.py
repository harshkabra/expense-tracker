from expense import (
    add_expenses,
    view_expenses,
    search_expense,
    delete_expense,
    total_expense,
    category_wise_total
)


# ============================================================
#                    MAIN MENU
# ============================================================

def main():

    while True:

        print("\n" + "=" * 60)
        print("                  EXPENSE TRACKER")
        print("=" * 60)

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search Expense")
        print("4. Delete Expense")
        print("5. Total Expense")
        print("6. Category-Wise Total")
        print("7. Exit")

        print("=" * 60)

        choice = input("Enter your choice: ")

        if choice == "1":

            add_expenses()

        elif choice == "2":

            view_expenses()

        elif choice == "3":

            search_expense()

        elif choice == "4":

            delete_expense()

        elif choice == "5":

            total_expense()

        elif choice == "6":

            category_wise_total()

        elif choice == "7":

            print("\nThank you for using Expense Tracker!")
            break

        else:

            print("\nPlease enter a choice between 1 and 7.")


# ============================================================
#                    START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()