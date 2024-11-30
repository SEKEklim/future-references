### Personal Financial Tracker
- The Personal Finance Tracker is a desktop application designed to help users track their daily expenses and monthly income efficiently. Its primary purpose is to empower users, especially those facing financial challenges, to manage their budgets effectively and gain better control of their financial situation.
### Problems Addressed
```markdown
  1. Lack of Awareness: Many individuals struggle to understand where their money is being spent.
  2. Inadequate Budgeting Tools: Current tools may not cater to specific needs like expense categorization and visualization.
  3. Unorganized Financial Records: Difficulty in tracking and grouping expenses over time leads to financial mismanagement.
```
### Solutions
```markdown
  1. Simplified Input System: Easy-to-use forms for entering daily expenses and monthly income.
  2. Data Visualization: Charts and grouped records allow users to see trends in their spending habits.
  3. Categorization: Users can categorize expenses, providing a detailed overview of where money is spent.
  4. Database Storage: All data is securely stored in an SQLite database, ensuring accessibility and reliability.
```
### Current Progress
```markdown
- Developed the main interface using CustomTkinter, ensuring a user-friendly design.
- Implemented core functionalities like adding expenses and income, viewing records, and visualizing expenses with charts.
- Set up a database for storing financial data persistently.
- Added features to delete records and validate input for accuracy.
```
### Features
```markdown
  1. Daily Expense Tracker: Users can input their expenses with categories and amounts for each day.
  2. Monthly Income Tracker: Allows users to record income sources and amounts.
  3. Expense Visualization: Displays monthly expenses as a bar chart for easy analysis.
  4. Expense Grouping: Groups expenses by month, showing details and totals for each day.
  5. Record Deletion: Enables users to delete erroneous or outdated entries.
```
### Expected Pages
```markdown
- Home Page: Displays main menu options.
- Add Daily Expense: Form to input daily spending details.
- View Expenses Grouped by Month: Displays records with monthly and daily totals.
- Add Monthly Income: Form to input income details.
- View Monthly Income: Displays a summary of income sources by month.
- Expense Chart: Graphical representation of monthly spending.
- Delete Record: Interface for removing specific records by ID.
```
### How to Run the Code
```markdown
  1. Install the required Python libraries:
      pip install customtkinter matplotlib
  2. Save the provided code to a file, e.g., finance_tracker.py.
  3. Run the script using Python:
      python finance_tracker.py
```
### How It Works
```markdown
  1. Home Screen: Users select an option from the menu (e.g., Add Daily Expense, View Expenses, etc.).
  2. Add Expense/Income: Opens a form for entering financial data, which is validated and saved to the database.
  3. View Records: Displays grouped or detailed records retrieved from the database.
  4. Expense Chart: Generates a bar chart using Matplotlib, showing total expenses for each month.
  5. Delete Record: Allows users to delete records by specifying their ID.
```














