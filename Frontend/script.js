const API_URL = "http://127.0.0.1:8000";

const expenseForm = document.getElementById("expenseForm");
const expenseTableBody = document.getElementById("expenseTableBody");
const summaryResult = document.getElementById("summaryResult");


// ===============================
// LOAD ALL EXPENSES
// ===============================

async function loadExpenses() {
    try {
        const response = await fetch(`${API_URL}/expenses`);

        if (!response.ok) {
            throw new Error("Failed to load expenses");
        }

        const expenses = await response.json();

        expenseTableBody.innerHTML = "";

        expenses.forEach((expense) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${expense.id}</td>
                <td>${expense.name}</td>
                <td>₹${expense.amount}</td>
                <td>${expense.category}</td>
                <td>${expense.date}</td>

                <td>
                    <button
                        class="edit-btn"
                        onclick="editExpense(${expense.id})"
                    >
                        Edit
                    </button>

                    <button
                        class="delete-btn"
                        onclick="deleteExpense(${expense.id})"
                    >
                        Delete
                    </button>
                </td>
            `;

            expenseTableBody.appendChild(row);
        });
    }
    catch (error) {
        console.error("Error loading expenses:", error);

        alert(
            "Could not connect to FastAPI server.\n\n" +
            "Make sure FastAPI is running on port 8000."
        );
    }
}


// ===============================
// ADD EXPENSE
// ===============================

expenseForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const name =
            document
                .getElementById("expenseName")
                .value
                .trim();

        const amount =
            Number(
                document
                    .getElementById("expenseAmount")
                    .value
            );

        const category =
            document
                .getElementById("expenseCategory")
                .value
                .trim();

        const date =
            document
                .getElementById("expenseDate")
                .value;


        const expense = {
            name: name,
            amount: amount,
            category: category,
            date: date
        };


        try {

            const response =
                await fetch(
                    `${API_URL}/expenses`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(expense)
                    }
                );


            const data =
                await response.json();


            if (response.ok) {

                alert(
                    "Expense added successfully!"
                );

                expenseForm.reset();

                loadExpenses();

            }
            else {

                alert(
                    data.detail ||
                    "Failed to add expense."
                );
            }

        }
        catch (error) {

            console.error(
                "Error adding expense:",
                error
            );

            alert(
                "Could not connect to FastAPI server.\n\n" +
                "Start FastAPI using:\n" +
                "uvicorn api:app --reload"
            );
        }
    }
);


// ===============================
// EDIT EXPENSE
// ===============================

async function editExpense(expenseId) {

    try {

        const response =
            await fetch(
                `${API_URL}/expenses/${expenseId}`
            );


        const expense =
            await response.json();


        if (!response.ok) {

            alert(
                expense.detail ||
                "Expense not found."
            );

            return;
        }


        const newName =
            prompt(
                "Enter expense name:",
                expense.name
            );


        if (newName === null) {
            return;
        }


        const newAmount =
            prompt(
                "Enter amount:",
                expense.amount
            );


        if (newAmount === null) {
            return;
        }


        const newCategory =
            prompt(
                "Enter category:",
                expense.category
            );


        if (newCategory === null) {
            return;
        }


        const updatedExpense = {

            name: newName.trim(),

            amount: Number(newAmount),

            category: newCategory.trim(),

            date: expense.date
        };


        const updateResponse =
            await fetch(
                `${API_URL}/expenses/${expenseId}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            updatedExpense
                        )
                }
            );


        const data =
            await updateResponse.json();


        if (updateResponse.ok) {

            alert(
                "Expense updated successfully!"
            );

            loadExpenses();

        }
        else {

            alert(
                data.detail ||
                "Failed to update expense."
            );
        }

    }
    catch (error) {

        console.error(
            "Error updating expense:",
            error
        );

        alert(
            "Could not connect to FastAPI server."
        );
    }
}


// ===============================
// DELETE EXPENSE
// ===============================

async function deleteExpense(expenseId) {

    const confirmDelete =
        confirm(
            "Are you sure you want to delete this expense?"
        );


    if (!confirmDelete) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/expenses/${expenseId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (response.ok) {

            alert(
                "Expense deleted successfully!"
            );

            loadExpenses();

        }
        else {

            alert(
                data.detail ||
                "Failed to delete expense."
            );
        }

    }
    catch (error) {

        console.error(
            "Error deleting expense:",
            error
        );

        alert(
            "Could not connect to FastAPI server."
        );
    }
}


// ===============================
// SEARCH EXPENSE
// ===============================

async function searchExpense() {

    const name =
        document
            .getElementById("searchName")
            .value
            .trim();


    if (!name) {

        alert(
            "Please enter an expense name."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/expenses/search/${encodeURIComponent(name)}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.detail ||
                "Expense not found."
            );

            return;
        }


        expenseTableBody.innerHTML = "";


        data.forEach((expense) => {

            const row =
                document.createElement("tr");


            row.innerHTML = `
                <td>${expense.id}</td>
                <td>${expense.name}</td>
                <td>₹${expense.amount}</td>
                <td>${expense.category}</td>
                <td>${expense.date}</td>

                <td>
                    <button
                        class="edit-btn"
                        onclick="editExpense(${expense.id})"
                    >
                        Edit
                    </button>

                    <button
                        class="delete-btn"
                        onclick="deleteExpense(${expense.id})"
                    >
                        Delete
                    </button>
                </td>
            `;


            expenseTableBody.appendChild(row);
        });

    }
    catch (error) {

        console.error(
            "Error searching expense:",
            error
        );

        alert(
            "Could not connect to FastAPI server."
        );
    }
}


// ===============================
// TOTAL EXPENSE
// ===============================

async function showTotalExpense() {

    try {

        const response =
            await fetch(
                `${API_URL}/expenses/summary/total`
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.detail ||
                "Could not calculate total."
            );

            return;
        }


        summaryResult.innerHTML = `
            <p>
                <strong>
                    Total Expense:
                </strong>

                ₹${data.total_expense}
            </p>
        `;

    }
    catch (error) {

        console.error(
            "Error getting total expense:",
            error
        );

        alert(
            "Could not connect to FastAPI server."
        );
    }
}


// ===============================
// CATEGORY-WISE TOTAL
// ===============================

async function showCategoryWiseTotal() {

    try {

        const response =
            await fetch(
                `${API_URL}/expenses/summary/category`
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.detail ||
                "Could not calculate category totals."
            );

            return;
        }


        summaryResult.innerHTML = "";


        if (data.length === 0) {

            summaryResult.innerHTML =
                "<p>No expenses found.</p>";

            return;
        }


        data.forEach((item) => {

            const paragraph =
                document.createElement("p");


            paragraph.innerHTML = `
                <strong>
                    ${item.category}:
                </strong>

                ₹${item.total}
            `;


            summaryResult.appendChild(
                paragraph
            );
        });

    }
    catch (error) {

        console.error(
            "Error getting category totals:",
            error
        );

        alert(
            "Could not connect to FastAPI server."
        );
    }
}


// ===============================
// LOAD DATA WHEN PAGE OPENS
// ===============================

loadExpenses();