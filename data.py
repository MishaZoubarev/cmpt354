import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# Populate User table
users = [(i, f"User {i}", f"555-000-{i:04}", f"{i} Example St", "Active" if i % 2 == 0 else "Inactive", round(i * 1.25 % 7, 2)) for i in range(1, 11)]
cursor.executemany("INSERT INTO User VALUES (?, ?, ?, ?, ?, ?)", users)

# Populate LibraryItem table
items = [(i, f"Item {i}", f"Author {i}", "Book", "Available", "General", "2025-01-01") for i in range(1, 11)]
cursor.executemany("INSERT INTO LibraryItem VALUES (?, ?, ?, ?, ?, ?, ?)", items)

# Populate Event table
events = [(i, f"Event {i}", f"Description {i}", "General", f"Room {i}", f"2025-04-{i:02} 10:00") for i in range(1, 11)]
cursor.executemany("INSERT INTO Event VALUES (?, ?, ?, ?, ?, ?)", events)

# Populate Personnel table
personnel = [(i, f"Staff {i}", "Librarian", f"555-100-{i:04}", f"{i} Staff Rd") for i in range(1, 11)]
cursor.executemany("INSERT INTO Personnel VALUES (?, ?, ?, ?, ?)", personnel)

# Populate FutureItem table
future_items = [(i, f"Future Item {i}", "Book", f"2025-06-{i:02}") for i in range(1, 11)]
cursor.executemany("INSERT INTO FutureItem VALUES (?, ?, ?, ?)", future_items)

# Populate Attends table
attends = [(i, i) for i in range(1, 11)]
cursor.executemany("INSERT INTO Attends VALUES (?, ?)", attends)

# Populate Borrows table
borrows = [(i, "2025-03-01", "2025-03-15", None, i, i) for i in range(1, 11)]
cursor.executemany("INSERT INTO Borrows VALUES (?, ?, ?, ?, ?, ?)", borrows)

# Populate Fine table
fines = [(i, round(i * 0.75, 2), "Unpaid" if i % 2 == 0 else "Paid", i) for i in range(1, 11)]
cursor.executemany("INSERT INTO Fine VALUES (?, ?, ?, ?)", fines)

conn.commit()
conn.close()
print("All tables populated with 10+ rows!")
