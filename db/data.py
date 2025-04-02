import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("DELETE FROM User")
cursor.execute("DELETE FROM LibraryItem")
cursor.execute("DELETE FROM Event")
cursor.execute("DELETE FROM Personnel")
cursor.execute("DELETE FROM FutureItem")
cursor.execute("DELETE FROM Attends")
cursor.execute("DELETE FROM Borrows")
cursor.execute("DELETE FROM Fine")

names = ["Hiroshi Tanaka", "Aisha Ahmed", "Carlos Mendoza", "Elena Petrova", "Samuel Johnson", "Fatima Al-Farsi", 
    "Pierre Dubois", "Chen Wei", "Nina Kowalska", "Rajesh Patel", "Liam O'Connor", "Giulia Romano", 
    "Amara Okafor", "Javier González", "Anna Müller", "Seong-Ho Kim", "Nguyen Minh", "Isla McKenzie", 
    "Youssef Haddad", "Natalia Sousa", "Dmitry Ivanov", "Mohammed Hassan", "Sophia Andersson", "Lucas Moreau", 
    "Tenzin Wangchuk", "Kofi Mensah", "Diego Ferreira", "Kaori Nakamura", "Omar El-Sayed", "Marta Nowak", 
    "Ravi Sharma", "Gustavo López", "Lin Xia", "Anders Berg", "Mehmet Demir", "Juanita Cruz", 
    "Mateo Rodríguez", "Hana Veselá", "Stavros Papadopoulos", "Ava Kowalczyk",
    "Fatou Diop", "Viktor Horváth", "Hassan Jafari", "Sofia Eriksson", "Miguel Pereira", "Anika Mehra", 
    "Yuki Takahashi", "Zainab Suleiman", "Ivan Stojanović", "Lena Bauer", "Arif Rahman", "Luciana Barros", 
    "Tarek Khalil", "Sonam Lama", "Dae-Hyun Park", "Vera Kuznetsova", "Ousmane Diallo", "Simone Conti", 
    "Fernando Castillo", "Leila Karimi", "Bashir Al-Mansouri", "Kateryna Shevchenko", "Ibrahim Syed", "Hana Kimura", 
    "Mohamed Salem", "Irina Smirnova", "Nico Schmidt", "Alejandro Torres", "Mina Jovanović", "Elias Håkansson", 
    "Amina Hassan", "Pavel Mikhailov", "Santiago Rojas", "Tamara Petrovic", "Jianhong Wu", "Yara Al-Mutairi", 
    "Nikolai Volkov", "Chloe Tremblay", "Ismael Haddou", "Emilia Kaczmarek"
]
audiences = ['General', 'Adults', 'Teens', 'Children']
books = {
    "To Kill a Mockingbird": "Harper Lee", "1984": "George Orwell", 
    "Pride and Prejudice": "Jane Austen", "The Great Gatsby": "F. Scott Fitzgerald",
    "The Hobbit": "J.R.R. Tolkien", "Dune": "Frank Herbert", 
    "The Catcher in the Rye": "J.D. Salinger", "Brave New World": "Aldous Huxley",
    "The Lord of the Rings": "J.R.R. Tolkien", "The Alchemist": "Paulo Coelho",
    "Sapiens: A Brief History of Humankind": "Yuval Noah Harari", 
    "The Hitchhiker's Guide to the Galaxy": "Douglas Adams",
    "The Da Vinci Code": "Dan Brown", "The Silent Patient": "Alex Michaelides",
    "Atomic Habits": "James Clear", "The Road": "Cormac McCarthy",
    "Gone Girl": "Gillian Flynn", "The Martian": "Andy Weir",
    "Educated": "Tara Westover", "The Name of the Wind": "Patrick Rothfuss"
}

directions = ['North', 'South', 'East', 'West']

# added more duplicate librarian options to increase probability that random personnel is a librarian
positions = ['Librarian', 'Janitor', 'Director', 'Librarian', 'Librarian']

events = [
    "movie night",
    "board game tournament",
    "book swap",
    "story time",
    "craft workshop",
    "themed reading event",
    "escape room challenge",
    "poetry slams",
    "book club meeting",
    "author signing event",
    "literary quiz night",
    "library scavenger hunt",
    "karaoke night",
    "diy bookbinding workshop",
    "children's talent show",
    "library picnic"
]

# Populate User table
namesStartingIndex = random.randrange(-1,len(names)-10);
for i in range(1,11) :
    user = (i, f"{names[namesStartingIndex + i]}", f"{random.randrange(100,1000):03}-{random.randrange(100,1000):03}-{random.randrange(1000,10000):04}", f"{random.randrange(1000,3000)} {random.choice(directions)} {random.randrange(1,50)} Ave", "Active" if i % 2 == 0 else "Inactive", round(i * 1.25 % 7, 2))
    cursor.execute("INSERT INTO User VALUES (?, ?, ?, ?, ?, ?)", user)

# Populate LibraryItem table
for i in range(1, 11) :
    randomTitle, randomAuthor = random.choice(list(books.items()))
    item = (i, f"{randomTitle}", f"{randomAuthor}", "Book", "Available", f"General", f"{datetime.today().strftime('%Y-%m-%d')}")
    cursor.execute("INSERT INTO LibraryItem VALUES (?, ?, ?, ?, ?, ?, ?)", item)

# Populate Event table
my_set = set()
for i in range(1, 11) :
    event = random.choice(events);
    while event in my_set :
        event = random.choice(events)

    event = (i, f"{event}", f"TBA", random.choice(audiences), f"Room {random.randrange(100,301)}", f"{(datetime.today() + timedelta(days=random.randrange(1,366))).strftime('%Y-%m-%d')} {random.randrange(1,21)}:00")
    cursor.execute("INSERT INTO Event VALUES (?, ?, ?, ?, ?, ?)", event)

# Populate Personnel table
namesStartingIndex = random.randrange(-1,len(names)-10);
for i in range(1, 11) :
    personnel = (i, f"{names[namesStartingIndex + i]}", f"{random.choice(positions)}", f"{random.randrange(100,1000):03}-{random.randrange(100,1000):03}-{random.randrange(1000,10000):04}", f"{random.randrange(1000,3000)} {random.choice(directions)} {random.randrange(1,10)} Ave")
    cursor.execute("INSERT INTO Personnel VALUES (?, ?, ?, ?, ?)", personnel)

# Populate FutureItem table
future_items = [(i, f"{random.choice(list(books.keys()))}", "Book", (datetime.today() + timedelta(days=random.randrange(1,366))).strftime('%Y-%m-%d')) for i in range(1, 11)]
cursor.executemany("INSERT INTO FutureItem VALUES (?, ?, ?, ?)", future_items)

# Populate Attends table
my_set = set()
for i in range(1, 11) :
    
    randUserID = random.randrange(1,11)
    randEventID = random.randrange(1,11)
    
    while (randUserID, randEventID) in my_set :
        randUserID = random.randrange(1,11)
        randEventID = random.randrange(1,11)
    
    my_set.add((randUserID, randEventID))

    attends = [(randUserID, randEventID) ]
    cursor.executemany("INSERT INTO Attends VALUES (?, ?)", attends)

# Populate Borrows table
my_set = set()
for i in range(1, 11) :
    # have a random user borrow a random book
    randUserID = random.randrange(1,11)

    timeNow = datetime.today().strftime('%Y-%m-%d')
    timeIn2Weeks = (datetime.today() + timedelta(weeks=2)).strftime('%Y-%m-%d')

    borrows = (i, timeNow, timeIn2Weeks, None, randUserID, i)
    cursor.execute("INSERT INTO Borrows VALUES (?, ?, ?, ?, ?, ?)", borrows)

# Populate Fine table
for i in range(1, 11) :
    fine = (i, round(random.random() + random.randrange(0,50),2), "Unpaid" if i % 2 == 0 else "Paid", random.randrange(1,11))
    cursor.execute("INSERT INTO Fine VALUES (?, ?, ?, ?)", fine)

conn.commit()
conn.close()
print("All tables populated with 10+ rows!")
