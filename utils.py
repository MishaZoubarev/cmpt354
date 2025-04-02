import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("library.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor();

def askForInput(message) :
    value = input(message)
    return value


def containsUserID(userID) :
    usersWhichHaveID = cursor.execute("SELECT * FROM User WHERE UserID=?", (userID,)).fetchall()
    return len(usersWhichHaveID) > 0
def containsItemID(itemID) : 
    itemsWhichHaveID = cursor.execute("SELECT * FROM LibraryItem WHERE ItemID=?", (itemID,)).fetchall()
    return len(itemsWhichHaveID) > 0

# Assume a VALID itemID is passed
def itemAvailable(itemID) : 
    itemWhichHaveID = cursor.execute("SELECT * FROM LibraryItem WHERE ItemID=?", (itemID,)).fetchone()
    availability = itemWhichHaveID[4];
    return availability == 'Available'


# Return : A list of attributes of a SINGLE tuple.
def getItem(title, author, type) :
    return cursor.execute("SELECT * FROM LibraryItem WHERE title=? AND author=? AND type=?", (title, author, type)).fetchone()
def getItemByID(itemID) :
    return cursor.execute("SELECT * FROM LibraryItem WHERE ItemID=?", (itemID,)).fetchone()

# Return : A list of library items/tuples.
def getItemsByTitle(title) :
    return cursor.execute("SELECT * FROM LibraryItem WHERE title=?", (title,)).fetchall()

def getItemsByAuthor(author) :
    return cursor.execute("SELECT * FROM LibraryItem WHERE author=?", (author,)).fetchall()

def getItemsByType(type) :
    return cursor.execute("SELECT * FROM LibraryItem WHERE type=?", (type,)).fetchall()


# The following functions used to borrow and return item from/to library.
# Return (both functions) : Boolean if operation was successful or not.
def borrowItem(userID, itemID) :
    if((not containsUserID(userID)) or (not containsItemID(itemID)) or (not itemAvailable(itemID))) :
        return False
    else :
        timeCheckedOut = datetime.today().strftime('%Y-%m-%d')
        dueDate = (datetime.today() + timedelta(weeks=2)).strftime('%Y-%m-%d')
        cursor.execute("INSERT INTO Borrows (BorrowDate, DueDate, ReturnDate, UserID, ItemID) VALUES (?, ?, ?, ?, ?)", (timeCheckedOut, dueDate, None, userID, itemID))
        conn.commit()
        return True
    
def returnItem(userID, itemID) : 
    if((not containsUserID(userID)) or itemAvailable(itemID)) :
        return False
    else :
        returnDate = datetime.today().strftime('%Y-%m-%d')

        transactionID = cursor.execute("SELECT * FROM Borrows WHERE userID=? AND itemID=? ORDER BY borrowDate DESC", (userID, itemID)).fetchone()[0]
        
        cursor.execute("UPDATE Borrows SET returnDate=? WHERE TransactionID=?", (returnDate, transactionID))

        conn.commit()
        return True

# Also used to for donated items.
def addItem(title, author, type, audience) : 
    newItem = (title, author, type, "Available", audience, datetime.today().strftime('%Y-%m-%d'))
    cursor.execute("INSERT INTO LibraryItem (Title, Author, Type, Status, Audience, DateAdded) VALUES (?,?,?,?,?,?)", newItem)
    conn.commit()


def main() : 
    addItem("new book", "Paul", "Book", "Teens")
    conn.close()


main()