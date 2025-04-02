import sqlite3
from datetime import datetime, timedelta

DB = "library.db"

def connect():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

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

def borrow_item():
    user_id = input("Enter your UserID: ")
    item_id = input("Enter ItemID to borrow: ")
    if not contains_user(user_id) or not contains_item(item_id) or not item_is_available(item_id):
        print("❌ Cannot borrow: invalid user, item not found, or item unavailable.")
        return
    borrow_date = datetime.today().strftime('%Y-%m-%d')
    due_date = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO Borrows (BorrowDate, DueDate, ReturnDate, UserID, ItemID) VALUES (?, ?, NULL, ?, ?)",
                    (borrow_date, due_date, user_id, item_id))
    print("✅ Item borrowed successfully!")

def return_item():
    user_id = input("Enter your UserID: ")
    item_id = input("Enter ItemID to return: ")
    if not contains_user(user_id) or item_is_available(item_id):
        print("❌ Cannot return: invalid user or item already marked available.")
        return
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT TransactionID FROM Borrows WHERE UserID=? AND ItemID=? AND ReturnDate IS NULL ORDER BY BorrowDate DESC",
                    (user_id, item_id))
        row = cur.fetchone()
        if not row:
            print("❌ No matching borrow record found.")
            return
        transaction_id = row[0]
        return_date = datetime.today().strftime('%Y-%m-%d')
        cur.execute("UPDATE Borrows SET ReturnDate=? WHERE TransactionID=?", (return_date, transaction_id))
    print("✅ Item returned successfully!")

def donate_item():
    title = input("Enter title of item to donate: ")
    author = input("Enter author: ")
    item_type = input("Enter type (Book, CD, etc.): ")
    audience = input("Enter audience (General, Adults, Teens, Children): ")
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO LibraryItem (Title, Author, Type, Status, Audience, DateAdded) VALUES (?, ?, ?, 'Available', ?, ?)",
                    (title, author, item_type, audience, datetime.today().strftime('%Y-%m-%d')))
    print("🎁 Thank you for your donation!")

def find_event():
    audience = input("Enter audience (General, Adults, Teens, Children): ")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Event WHERE RecommendedAudience = ?", (audience,))
    for row in cursor.fetchall():
        print(row)
    conn.close()

def register_event():
    conn = connect()
    cursor = conn.cursor()
    print("\n📅 Upcoming Events:")
    cursor.execute("SELECT EventID, Name, DateTime, Location FROM Event ORDER BY DateTime")
    events = cursor.fetchall()
    for event in events:
        print(f"ID: {event[0]} | {event[1]} @ {event[3]} on {event[2]}")
    user_id = input("\nEnter your UserID: ")
    event_id = input("Enter EventID to register for: ")
    try:
        cursor.execute("INSERT INTO Attends (UserID, EventID) VALUES (?, ?)", (user_id, event_id))
        conn.commit()
        print("✅ Registered for the event!")
    except sqlite3.IntegrityError:
        print("❌ Already registered or invalid IDs.")
    conn.close()

def volunteer():
    name = input("Your full name: ")
    phone = input("Phone number: ")
    address = input("Address: ")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Personnel (Name, Role, Phone, Address) VALUES (?, 'Volunteer', ?, ?)",
                   (name, phone, address))
    conn.commit()
    print("✅ Thank you for volunteering!")
    conn.close()

def ask_help():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Phone FROM Personnel WHERE Role = 'Librarian'")
    librarians = cursor.fetchall()
    if librarians:
        print("📚 Available Librarians:")
        for lib in librarians:
            print(f"- {lib[0]} | Phone: {lib[1]}")
    else:
        print("No librarians available right now.")
    conn.close()

def main():
    while True:
        print("\n=== Library App Menu ===")
        print("1. Find an item")
        print("2. Borrow an item")
        print("3. Return a borrowed item")
        print("4. Donate an item")
        print("5. Find an event")
        print("6. Register for an event")
        print("7. Volunteer for the library")
        print("8. Ask a librarian for help")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter title: ")
            with connect() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM LibraryItem WHERE Title LIKE ?", (f"%{title}%",))
                results = cur.fetchall()
                for row in results:
                    print(row)
        elif choice == "2": borrow_item()
        elif choice == "3": return_item()
        elif choice == "4": donate_item()
        elif choice == "5": find_event()
        elif choice == "6": register_event()
        elif choice == "7": volunteer()
        elif choice == "8": ask_help()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
