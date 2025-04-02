import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

def connect():
    conn = sqlite3.connect("library.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Utility functions
def contains_user(user_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM User WHERE UserID = ?", (user_id,))
        return cur.fetchone() is not None

def contains_item(item_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM LibraryItem WHERE ItemID = ?", (item_id,))
        return cur.fetchone() is not None

def item_is_available(item_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT Status FROM LibraryItem WHERE ItemID = ?", (item_id,))
        row = cur.fetchone()
        return row and row[0] == "Available"

# Feature Functions
def find_item():
    win = tk.Toplevel(root)
    win.title("Find Item")

    tk.Label(win, text="Search by Title:").pack()
    title_entry = tk.Entry(win)
    title_entry.pack()

    def search():
        title = title_entry.get()
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM LibraryItem WHERE Title LIKE ?", (f"%{title}%",))
            results = cur.fetchall()

        if not results:
            messagebox.showinfo("No Results", "No matching items found.")
        else:
            msg = "\n".join([f"{r[0]}: {r[1]} by {r[2]} ({r[3]}) - {r[4]}" for r in results])
            messagebox.showinfo("Search Results", msg)

    tk.Button(win, text="Search", command=search).pack()

def borrow_item():
    win = tk.Toplevel(root)
    win.title("Borrow Item")

    tk.Label(win, text="User ID:").pack()
    uid_entry = tk.Entry(win)
    uid_entry.pack()

    tk.Label(win, text="Item ID:").pack()
    iid_entry = tk.Entry(win)
    iid_entry.pack()

    def borrow():
        uid = uid_entry.get()
        iid = iid_entry.get()
        if not contains_user(uid) or not contains_item(iid) or not item_is_available(iid):
            messagebox.showerror("Error", "❌ Invalid user/item or item not available.")
            return
        with connect() as conn:
            cur = conn.cursor()
            borrow_date = datetime.today().strftime('%Y-%m-%d')
            due_date = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')
            cur.execute("INSERT INTO Borrows (BorrowDate, DueDate, ReturnDate, UserID, ItemID) VALUES (?, ?, NULL, ?, ?)",
                        (borrow_date, due_date, uid, iid))
            conn.commit()
        messagebox.showinfo("Success", "✅ Item borrowed!")

    tk.Button(win, text="Borrow", command=borrow).pack()

def return_item():
    win = tk.Toplevel(root)
    win.title("Return Item")

    tk.Label(win, text="User ID:").pack()
    uid_entry = tk.Entry(win)
    uid_entry.pack()

    tk.Label(win, text="Item ID:").pack()
    iid_entry = tk.Entry(win)
    iid_entry.pack()

    def ret():
        uid = uid_entry.get()
        iid = iid_entry.get()
        if not contains_user(uid) or item_is_available(iid):
            messagebox.showerror("Error", "❌ Invalid user or item is already available.")
            return
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT TransactionID FROM Borrows WHERE UserID=? AND ItemID=? AND ReturnDate IS NULL ORDER BY BorrowDate DESC",
                        (uid, iid))
            row = cur.fetchone()
            if not row:
                messagebox.showerror("Error", "❌ No borrow record found.")
                return
            transaction_id = row[0]
            return_date = datetime.today().strftime('%Y-%m-%d')
            cur.execute("UPDATE Borrows SET ReturnDate=? WHERE TransactionID=?", (return_date, transaction_id))
            conn.commit()
        messagebox.showinfo("Success", "✅ Item returned.")

    tk.Button(win, text="Return", command=ret).pack()

def donate_item():
    win = tk.Toplevel(root)
    win.title("Donate Item")

    labels = ["Title", "Author", "Type", "Audience"]
    entries = {}

    for label in labels:
        tk.Label(win, text=label + ":").pack()
        entry = tk.Entry(win)
        entry.pack()
        entries[label] = entry

    def donate():
        title = entries["Title"].get()
        author = entries["Author"].get()
        type_ = entries["Type"].get()
        audience = entries["Audience"].get()
        date_added = datetime.today().strftime('%Y-%m-%d')
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO LibraryItem (Title, Author, Type, Status, Audience, DateAdded) VALUES (?, ?, ?, 'Available', ?, ?)",
                        (title, author, type_, audience, date_added))
            conn.commit()
        messagebox.showinfo("Success", "🎁 Thank you for your donation!")

    tk.Button(win, text="Donate", command=donate).pack()

def find_event():
    win = tk.Toplevel(root)
    win.title("Find Event")

    tk.Label(win, text="Audience (General, Adults, Teens, Children):").pack()
    entry = tk.Entry(win)
    entry.pack()

    def search():
        audience = entry.get()
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Event WHERE RecommendedAudience = ?", (audience,))
            events = cur.fetchall()

        if not events:
            messagebox.showinfo("Events", "No events found.")
            return

        result = "\n".join([f"{e[0]} | {e[1]} @ {e[4]} on {e[5]}" for e in events])
        messagebox.showinfo("Upcoming Events", result)

    tk.Button(win, text="Search", command=search).pack()

def register_event():
    win = tk.Toplevel(root)
    win.title("Register for Event")

    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT EventID, Name, DateTime FROM Event ORDER BY DateTime")
        events = cur.fetchall()

    tk.Label(win, text="Events:").pack()
    for e in events:
        tk.Label(win, text=f"ID: {e[0]} | {e[1]} on {e[2]}").pack()

    tk.Label(win, text="Your UserID:").pack()
    user_entry = tk.Entry(win)
    user_entry.pack()

    tk.Label(win, text="EventID to register:").pack()
    event_entry = tk.Entry(win)
    event_entry.pack()

    def register():
        uid = user_entry.get()
        eid = event_entry.get()
        with connect() as conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Attends (UserID, EventID) VALUES (?, ?)", (uid, eid))
                conn.commit()
                messagebox.showinfo("Registered", "✅ You are registered!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "❌ Already registered or invalid input.")

    tk.Button(win, text="Register", command=register).pack()

def volunteer():
    win = tk.Toplevel(root)
    win.title("Volunteer")

    tk.Label(win, text="Name:").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Phone:").pack()
    phone_entry = tk.Entry(win)
    phone_entry.pack()

    tk.Label(win, text="Address:").pack()
    address_entry = tk.Entry(win)
    address_entry.pack()

    def submit():
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO Personnel (Name, Role, Phone, Address) VALUES (?, 'Volunteer', ?, ?)",
                        (name_entry.get(), phone_entry.get(), address_entry.get()))
            conn.commit()
        messagebox.showinfo("Thank You", "✅ You're now a volunteer!")

    tk.Button(win, text="Submit", command=submit).pack()

def ask_help():
    win = tk.Toplevel(root)
    win.title("Ask a Librarian")

    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT Name, Phone FROM Personnel WHERE Role = 'Librarian'")
        results = cur.fetchall()

    if not results:
        tk.Label(win, text="No librarians available.").pack()
    else:
        for r in results:
            tk.Label(win, text=f"{r[0]} - {r[1]}").pack()

# Main App
root = tk.Tk()
root.title("Library GUI")
root.geometry("350x500")

tk.Button(root, text="Find Item", width=30, command=find_item).pack(pady=5)
tk.Button(root, text="Borrow Item", width=30, command=borrow_item).pack(pady=5)
tk.Button(root, text="Return Item", width=30, command=return_item).pack(pady=5)
tk.Button(root, text="Donate Item", width=30, command=donate_item).pack(pady=5)
tk.Button(root, text="Find Event", width=30, command=find_event).pack(pady=5)
tk.Button(root, text="Register for Event", width=30, command=register_event).pack(pady=5)
tk.Button(root, text="Volunteer", width=30, command=volunteer).pack(pady=5)
tk.Button(root, text="Ask a Librarian", width=30, command=ask_help).pack(pady=5)
tk.Button(root, text="Exit", width=30, command=root.destroy).pack(pady=20)

root.mainloop()
