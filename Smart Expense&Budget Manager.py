# Author: Abishek's Assistant 😊

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import schedule
import time
from plyer import notification

FILE_NAME = "expenses.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Type"])
    df.to_csv(FILE_NAME, index=False)

def add_transaction(category, amount, t_type):
    date = datetime.now().strftime("%Y-%m-%d")
    df = pd.read_csv(FILE_NAME)
    new_row = {"Date": date, "Category": category, "Amount": amount, "Type": t_type}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    print(f"{t_type} of ₹{amount} added under {category}.")

def show_summary():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No records yet.")
        return

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    msg = f"Total Income: ₹{income}\nTotal Expense: ₹{expense}\nBalance: ₹{balance}"
    print("\n------ Monthly Summary ------")
    print(msg)
    print("-----------------------------")

    exp_data = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()

    if not exp_data.empty:
        exp_data.plot(kind="pie", autopct="%1.1f%%", startangle=90)
        plt.title("Expense Distribution by Category")
        plt.ylabel("")
        plt.show()

    return msg

def send_monthly_notification():
    today = datetime.now()
    last_day = pd.Timestamp(today.year, today.month, 1) + pd.offsets.MonthEnd(1)
    
    if today.day == last_day.day:  
        msg = show_summary()
        notification.notify(
            title="📅 Monthly Expense Summary",
            message=msg,
            timeout=10  
        )

def run_scheduler():
    schedule.every().day.at("20:00").do(send_monthly_notification)  

    print("✅ Monthly notifier started. Running in background...")
    while True:
        schedule.run_pending()
        time.sleep(60)  

# 🔹 Step 6: Menu for manual use
def menu():
    while True:
        print("\n=== Smart Expense & Budget Manager ===")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show Summary")
        print("4. Start Monthly Notification (background)")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            cat = input("Enter income source: ")
            amt = float(input("Enter amount: "))
            add_transaction(cat, amt, "Income")

        elif choice == "2":
            cat = input("Enter expense category: ")
            amt = float(input("Enter amount: "))
            add_transaction(cat, amt, "Expense")

        elif choice == "3":
            show_summary()

        elif choice == "4":
            run_scheduler()

        elif choice == "5":
            print("Exiting... Have a great day!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()