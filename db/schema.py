import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Define your schema (copy-paste from step 5 with renamed tables)
cursor.executescript("""
-- 1. LibraryItem
CREATE TABLE IF NOT EXISTS LibraryItem (
    ItemID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Author TEXT,
    Type TEXT CHECK(Type IN ('Book', 'Magazine', 'Journal', 'CD', 'Record', 'Other')),
    Status TEXT CHECK(Status IN ('Available', 'Borrowed')) NOT NULL,
    Audience TEXT CHECK(Audience IN ('General', 'Adults', 'Teens', 'Children')),
    DateAdded DATE
);

-- 2. User
CREATE TABLE IF NOT EXISTS User (
    UserID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Phone TEXT,
    Address TEXT,
    Membership TEXT CHECK(Membership IN ('Active', 'Inactive')) DEFAULT 'Active',
    Fines REAL DEFAULT 0 CHECK(Fines >= 0)
);

-- 3. Borrows
CREATE TABLE IF NOT EXISTS Borrows (
    TransactionID INTEGER PRIMARY KEY,
    BorrowDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    UserID INTEGER NOT NULL,
    ItemID INTEGER NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (ItemID) REFERENCES LibraryItem(ItemID) ON DELETE CASCADE
);

-- 4. Fine
CREATE TABLE IF NOT EXISTS Fine (
    FineID INTEGER PRIMARY KEY,
    Amount REAL CHECK(Amount >= 0),
    Status TEXT CHECK(Status IN ('Unpaid', 'Paid')) NOT NULL,
    UserID INTEGER NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);

-- 5. Event
CREATE TABLE IF NOT EXISTS Event (
    EventID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Description TEXT,
    RecommendedAudience TEXT CHECK(RecommendedAudience IN ('General', 'Adults', 'Teens', 'Children')),
    Location TEXT,
    DateTime DATETIME NOT NULL
);

-- 6. Attends
CREATE TABLE IF NOT EXISTS Attends (
    UserID INTEGER,
    EventID INTEGER,
    PRIMARY KEY (UserID, EventID)
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (EventID) REFERENCES Event(EventID) ON DELETE CASCADE
);

-- 7. Personnel
CREATE TABLE IF NOT EXISTS Personnel (
    StaffID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Role TEXT NOT NULL,
    Phone TEXT,
    Address TEXT
);

-- 8. FutureItem
CREATE TABLE IF NOT EXISTS FutureItem (
    FutureItemID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Type TEXT,
    ExpectedArrivalDate DATE
);        
""")

# Commit and close
conn.commit()
conn.close()

print("Database schema created!")
