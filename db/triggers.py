import sqlite3

# Connect to the existing database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Enable foreign key enforcement
cursor.execute("PRAGMA foreign_keys = ON;")

# Trigger 1: Set item status to 'Borrowed' after an item is borrowed
cursor.execute("""
CREATE TRIGGER IF NOT EXISTS SetItemBorrowed
AFTER INSERT ON Borrows
FOR EACH ROW
BEGIN
    UPDATE LibraryItem SET Status = 'Borrowed'
    WHERE ItemID = NEW.ItemID;
END;
""")

# Trigger 2: Set item status to 'Available' when an item is returned
cursor.execute("""
CREATE TRIGGER IF NOT EXISTS SetItemAvailable
AFTER UPDATE OF ReturnDate ON Borrows
FOR EACH ROW
WHEN NEW.ReturnDate IS NOT NULL
BEGIN
    UPDATE LibraryItem SET Status = 'Available'
    WHERE ItemID = NEW.ItemID;
END;
""")

# Trigger 3: Prevent overlapping events in the same room within 1 hour
cursor.execute("""
CREATE TRIGGER IF NOT EXISTS PreventEventOverlap
BEFORE INSERT ON Event
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN EXISTS (
            SELECT 1 FROM Event
            WHERE Location = NEW.Location
              AND ABS(strftime('%s', DateTime) - strftime('%s', NEW.DateTime)) < 3600
        )
        THEN RAISE(ABORT, 'Another event is scheduled in the same room within 1 hour.')
    END;
END;
""")

conn.commit()
conn.close()

print("Triggers created")
