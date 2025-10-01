import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import tkinter as tk
import pandas as pd
import datetime
import os

# Appearance and Theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# App Setup
app = ctk.CTk()
app.title("Expense Tracker")
app.state("zoomed")
app.configure(bg="#f0f8ff")

# Save path to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
csv_path = os.path.join(os.path.dirname(__file__), "expenses.csv")


# Load existing data if available
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

# Header Banner
header = ctk.CTkFrame(app, fg_color="#2196f3")
header.pack(fill="x")
ctk.CTkLabel(header, text="💸 Expense Tracker", font=("Arial", 28, "bold"), text_color="white").pack(pady=10)

# Calendar Date Picker
calendar_frame = ctk.CTkFrame(app, fg_color="transparent")
calendar_frame.pack(pady=10)
ctk.CTkLabel(calendar_frame, text="Select Date:", font=("Arial", 16)).pack(side="left", padx=10)
date_picker = DateEntry(calendar_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date_picker.pack(side="left")

# Input Fields
category_entry = ctk.CTkComboBox(app, values=["Food", "Transport", "Bills", "Entertainment", "Other"], width=300)
category_entry.set("Select Category")
amount_entry = ctk.CTkEntry(app, placeholder_text="Amount", width=300)
note_entry = ctk.CTkEntry(app, placeholder_text="Note (optional)", width=300)

for widget in [category_entry, amount_entry, note_entry]:
    widget.pack(pady=10)

# Add Expense
def add_expense():
    date = date_picker.get()
    category = category_entry.get()
    amount = amount_entry.get()
    note = note_entry.get()

    if not date or category == "Select Category" or not amount:
        messagebox.showwarning("Missing Info", "Please fill all required fields.")
        return

    try:
        amount = float(amount)
        df.loc[len(df)] = [date, category, amount, note]
        df.to_csv(csv_path, index=False)
        messagebox.showinfo("Success", "Expense added and saved!")
        clear_fields()
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")

# Clear Fields
def clear_fields():
    category_entry.set("Select Category")
    amount_entry.delete(0, 'end')
    note_entry.delete(0, 'end')

# Export to CSV
def export_data():
    df.to_csv(csv_path, index=False)
    messagebox.showinfo("Exported", f"Data saved to Desktop:\n{csv_path}")

# View Total Summary
def view_summary():
    total = df["Amount"].sum()
    messagebox.showinfo("Summary", f"Total Expenses: ₹{total:.2f}")

# View All Expenses
def show_expenses():
    if df.empty:
        messagebox.showinfo("No Data", "No expenses recorded yet.")
        return

    top = tk.Toplevel(app)
    top.title("All Expenses")
    top.geometry("700x400")

    text_widget = tk.Text(top, wrap="none", font=("Courier", 12))
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
    text_widget.insert("1.0", df.to_string(index=False))
    text_widget.config(state="disabled")

# Monthly Summary by Category
def monthly_summary():
    if df.empty:
        messagebox.showinfo("No Data", "No expenses recorded yet.")
        return
    df["Date"] = pd.to_datetime(df["Date"])
    this_month = df[df["Date"].dt.month == datetime.date.today().month]
    summary = this_month.groupby("Category")["Amount"].sum()
    messagebox.showinfo("Monthly Summary", summary.to_string())

# Delete Expense by Index
def delete_expense():
    if df.empty:
        messagebox.showinfo("No Data", "No expenses to delete.")
        return

    delete_window = tk.Toplevel(app)
    delete_window.title("Delete Expense")
    delete_window.geometry("300x150")

    tk.Label(delete_window, text="Enter row number to delete:", font=("Arial", 12)).pack(pady=10)
    index_entry = tk.Entry(delete_window, font=("Arial", 12))
    index_entry.pack(pady=5)

    def confirm_delete():
        try:
            idx = int(index_entry.get())
            if idx < 0 or idx >= len(df):
                raise IndexError
            df.drop(index=idx, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df.to_csv(csv_path, index=False)
            messagebox.showinfo("Deleted", f"Expense at row {idx} deleted.")
            delete_window.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
        except IndexError:
            messagebox.showerror("Out of Range", "No expense found at that index.")

    tk.Button(delete_window, text="Delete", command=confirm_delete).pack(pady=10)

# Button Styles
button_style_add = {"width": 250, "height": 40, "corner_radius": 10, "font": ("Arial", 16), "fg_color": "#4caf50", "hover_color": "#388e3c"}
button_style_summary = {"width": 250, "height": 40, "corner_radius": 10, "font": ("Arial", 16), "fg_color": "#03a9f4", "hover_color": "#0288d1"}
button_style_monthly = {"width": 250, "height": 40, "corner_radius": 10, "font": ("Arial", 16), "fg_color": "#ff9800", "hover_color": "#f57c00"}
button_style_view = {"width": 250, "height": 40, "corner_radius": 10, "font": ("Arial", 16), "fg_color": "#9c27b0", "hover_color": "#7b1fa2"}
button_style_export = {"width": 250, "height": 40, "corner_radius": 10, "font": ("Arial", 16), "fg_color": "#607d8b", "hover_color": "#455a64"}
button_style_delete = {"width": 250, "height": 40, "corner_radius": 10, "font": ("Arial", 16), "fg_color": "#f44336", "hover_color": "#d32f2f"}

# Buttons
ctk.CTkButton(app, text="📥 Add Expense", command=add_expense, **button_style_add).pack(pady=10)
ctk.CTkButton(app, text="📊 View Summary", command=view_summary, **button_style_summary).pack(pady=5)
ctk.CTkButton(app, text="📅 Monthly Summary", command=monthly_summary, **button_style_monthly).pack(pady=5)
ctk.CTkButton(app, text="📋 View All Expenses", command=show_expenses, **button_style_view).pack(pady=5)
ctk.CTkButton(app, text="💾 Export to CSV", command=export_data, **button_style_export).pack(pady=5)
ctk.CTkButton(app, text="🗑️ Delete Expense", command=delete_expense, **button_style_delete).pack(pady=5)

app.mainloop()