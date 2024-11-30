import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3
import json
from datetime import datetime
import matplotlib.pyplot as plt


# Database Setup
def setup_database():
    connection = sqlite3.connect("finance_tracker.db")
    cursor = connection.cursor()

    # Table for daily transactions (expenses)
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT NOT NULL,
                        details TEXT NOT NULL,
                        date TEXT NOT NULL,
                        month TEXT NOT NULL
                    )''')

    # Table for monthly income
    cursor.execute('''CREATE TABLE IF NOT EXISTS monthly_income (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        details TEXT NOT NULL,
                        month TEXT NOT NULL
                    )''')
    
    connection.commit()
    connection.close()


class FinanceTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Tracker")
        self.geometry("400x400")

        setup_database()
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ctk.CTkLabel(self, text="Personal Finance Tracker", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Buttons for each option
        buttons = [
            ("Add Daily Expense", self.add_daily_expenses),
            ("View Expenses Grouped by Month", self.view_expenses_grouped_by_month),
            ("Add Monthly Income", self.add_monthly_income),
            ("View Monthly Income", self.view_monthly_income),
            ("Show Expense Chart", self.show_expense_chart),
            ("Delete Record by ID", self.delete_record),
            ("Exit", self.quit),
        ]

        for text, command in buttons:
            button = ctk.CTkButton(self, text=text, command=command, width=200, height=40)
            button.pack(pady=5)

    # Function to validate date input
    @staticmethod
    def is_valid_date(date_str, date_format):
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            return False

    # Function to add daily expenses
    def add_daily_expenses(self):
        def save_expense():
            date = date_entry.get().strip()

            # Validate the date format (YYYY-MM-DD)
            if not self.is_valid_date(date, "%Y-%m-%d"):
                messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
                return

            month = date[:7]
            expenses = {}

            for entry in expense_entries:
                category = entry[0].get().strip()
                try:
                    amount = float(entry[1].get())
                    if category:
                        expenses[category] = amount
                except ValueError:
                    continue

            if expenses:
                connection = sqlite3.connect("finance_tracker.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO transactions (type, details, date, month) VALUES (?, ?, ?, ?)",
                               ("Expense", json.dumps(expenses), date, month))
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", f"Daily expenses for {date} added successfully!")
                add_expense_window.destroy()
            else:
                messagebox.showerror("Error", "No valid expenses were entered!")

        # Expense entry form
        add_expense_window = ctk.CTkToplevel(self)
        add_expense_window.title("Add Daily Expense")
        add_expense_window.geometry("500x400")

        ctk.CTkLabel(add_expense_window, text="Enter the Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = ctk.CTkEntry(add_expense_window, width=200)
        date_entry.pack(pady=5)

        ctk.CTkLabel(add_expense_window, text="Enter Expenses:").pack(pady=5)
        expense_entries = []
        for _ in range(5):  # Allow up to 5 entries
            frame = ctk.CTkFrame(add_expense_window)
            frame.pack(pady=2)
            category_entry = ctk.CTkEntry(frame, width=150, placeholder_text="Category")
            category_entry.pack(side="left", padx=5)
            amount_entry = ctk.CTkEntry(frame, width=100, placeholder_text="Amount")
            amount_entry.pack(side="left", padx=5)
            expense_entries.append((category_entry, amount_entry))

        ctk.CTkButton(add_expense_window, text="Save Expenses", command=save_expense).pack(pady=10)

    # Function to view expenses grouped by month
    def view_expenses_grouped_by_month(self):
        connection = sqlite3.connect("finance_tracker.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, date, details, month FROM transactions WHERE type = 'Expense' ORDER BY month ASC, date ASC")
        records = cursor.fetchall()
        connection.close()

        if not records:
            messagebox.showinfo("No Data","No expense records found.")
            return

        # Create a new window to display grouped expenses
        view_window = ctk.CTkToplevel(self)
        view_window.title("Expenses Grouped by Month")
        tree = ttk.Treeview(
            view_window,
            columns=("ID", "Month", "Date", "Details", "Daily Total"),
            show="headings",
        )
        tree.heading("ID", text="ID")
        tree.heading("Month", text="Month")
        tree.heading("Date", text="Date")
        tree.heading("Details", text="Details")
        tree.heading("Daily Total", text="Daily Total")
        tree.pack(fill="both", expand=True)

        # Process records to group by month and calculate monthly totals
        grouped_records = {}
        for record in records:
            record_id, date, details, month = record
            expenses = json.loads(details)  # Decode the JSON details
            daily_total = sum(expenses.values())  # Calculate daily total

            if month not in grouped_records:
                grouped_records[month] = {"daily_records": [], "monthly_total": 0}
            grouped_records[month]["daily_records"].append((record_id, date, details, daily_total))
            grouped_records[month]["monthly_total"] += daily_total

        # Populate the Treeview with grouped expense records
        for month, data in grouped_records.items():
            monthly_total = data["monthly_total"]

            # Add a row for the month's total
            tree.insert("", "end", values=("", month, "Total for Month", "", f"{monthly_total} ៛"), tags=("total",))
            
            # Add rows for each day's expenses
            for record_id, date, details, daily_total in data["daily_records"]:
                formatted_details = ", ".join(f"{key}: {value} ៛" for key, value in json.loads(details).items())
                tree.insert("", "end", values=(record_id, month, date, formatted_details, f"{daily_total} ៛"))

        # Add styling for monthly total rows
        tree.tag_configure("total", background="#d3d3d3", font=("Arial", 10, "bold"))



    # Function to add monthly income
    def add_monthly_income(self):
        def save_income():
            month = month_entry.get().strip()

            # Validate the month format (YYYY-MM)
            if not self.is_valid_date(month, "%Y-%m"):
                messagebox.showerror("Invalid Month", "Please enter a valid month in YYYY-MM format.")
                return

            income_details = {}

            for entry in income_entries:
                source = entry[0].get().strip()
                try:
                    amount = float(entry[1].get())
                    if source:
                        income_details[source] = amount
                except ValueError:
                    continue

            if income_details:
                connection = sqlite3.connect("finance_tracker.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO monthly_income (details, month) VALUES (?, ?)",
                               (json.dumps(income_details), month))
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", f"Monthly income for {month} added successfully!")
                add_income_window.destroy()
            else:
                messagebox.showerror("Error", "No valid income details were entered!")

        # Income entry form
        add_income_window = ctk.CTkToplevel(self)
        add_income_window.title("Add Monthly Income")
        add_income_window.geometry("500x400")

        ctk.CTkLabel(add_income_window, text="Enter the Month (YYYY-MM):").pack(pady=5)
        month_entry = ctk.CTkEntry(add_income_window, width=200)
        month_entry.pack(pady=5)

        ctk.CTkLabel(add_income_window, text="Enter Income Details:").pack(pady=5)
        income_entries = []
        for _ in range(5):  # Allow up to 5 entries
            frame = ctk.CTkFrame(add_income_window)
            frame.pack(pady=2)
            source_entry = ctk.CTkEntry(frame, width=150, placeholder_text="Source")
            source_entry.pack(side="left", padx=5)
            amount_entry = ctk.CTkEntry(frame, width=100, placeholder_text="Amount")
            amount_entry.pack(side="left", padx=5)
            income_entries.append((source_entry, amount_entry))

        ctk.CTkButton(add_income_window, text="Save Income", command=save_income).pack(pady=10)
        
        # Function to view monthly income
    def view_monthly_income(self):
        connection = sqlite3.connect("finance_tracker.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, details, month FROM monthly_income ORDER BY month ASC")
        records = cursor.fetchall()
        connection.close()

        if not records:
            messagebox.showinfo("No Data", "No monthly income records found.")
            return

        # Create a new window to display monthly income
        view_window = ctk.CTkToplevel(self)
        view_window.title("Monthly Income Records")
        tree = ttk.Treeview(
            view_window,
            columns=("ID", "Month", "Details", "Monthly Total"),
            show="headings",
        )
        tree.heading("ID", text="ID")
        tree.heading("Month", text="Month")
        tree.heading("Details", text="Details")
        tree.heading("Monthly Total", text="Monthly Total")
        tree.pack(fill="both", expand=True)

        # Populate the Treeview with monthly income records
        for record in records:
            record_id, details, month = record
            income_details = json.loads(details)  # Decode the stored JSON
            monthly_total = sum(income_details.values())  # Calculate monthly total
            details_formatted = ", ".join(f"{key}: {value} ៛" for key, value in income_details.items())
            tree.insert("", "end", values=(record_id, month, details_formatted, f"{monthly_total} ៛"))
            
            
    # Function to display a chart for total expenses of each month
    def show_expense_chart(self):
        connection = sqlite3.connect("finance_tracker.db")
        cursor = connection.cursor()
        cursor.execute("SELECT month, details FROM transactions WHERE type = 'Expense'")
        records = cursor.fetchall()
        connection.close()

        if not records:
            messagebox.showinfo("No Data", "No expense records found.")
            return

        # Process data to calculate monthly totals
        monthly_totals = {}
        for record in records:
            month, details = record
            expenses = json.loads(details)  # Decode JSON details
            monthly_total = sum(expenses.values())  # Calculate total for the record
            if month not in monthly_totals:
                monthly_totals[month] = 0
            monthly_totals[month] += monthly_total

        # Sort monthly totals by month (key)
        sorted_months = sorted(monthly_totals.keys())
        sorted_totals = [monthly_totals[month] for month in sorted_months]

        # Plot the data using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.bar(sorted_months, sorted_totals, color='purple', label="Total Expenses")
        plt.xlabel("Month")
        plt.ylabel("Total Expense ៛")
        plt.title("Total Expenses Per Month")
        plt.legend(loc="upper right")
        plt.xticks(rotation=45)  # Rotate month labels for better readability
        plt.tight_layout()  # Adjust layout to fit everything
        plt.show()


    # Function to delete a record by ID
    def delete_record(self):
        def delete_from_table():
            try:
                record_id = int(id_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid ID.")
                return

            table_name = table_var.get()

            connection = sqlite3.connect("finance_tracker.db")
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", f"Record with ID {record_id} deleted from {table_name}")
            delete_window.destroy()

        delete_window = ctk.CTkToplevel(self)
        delete_window.title("Delete Record")
        delete_window.geometry("400x200")

        ctk.CTkLabel(delete_window, text="Select Table:").pack(pady=5)
        table_var = ctk.StringVar(value="transactions")
        table_dropdown = ctk.CTkComboBox(delete_window, values=["transactions", "monthly_income"], variable=table_var)
        table_dropdown.pack(pady=5)

        ctk.CTkLabel(delete_window, text="Enter Record ID:").pack(pady=5)
        id_entry = ctk.CTkEntry(delete_window, width=200)
        id_entry.pack(pady=5)

        ctk.CTkButton(delete_window, text="Delete Record", command=delete_from_table).pack(pady=10)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
    ctk.set_default_color_theme("dark-blue")  # Themes: "blue", "dark-blue", "green"

    app = FinanceTrackerApp()
    app.mainloop()
