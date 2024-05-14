import sqlite3
#

def emails_db():
    # Define connection and cursor objects
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()

    # Create the table named 'contacts' with columns 'name' (text) and 'email' (text)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        sr INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        email TEXT UNIQUE
    )
    """)
    conn.commit()



def add(name, email):
    emails_db()
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO contacts (name , email) VALUES(?,?)", (name, email))
        conn.commit()
    except:
        return False
    return True

def retrieve(name):
    emails_db()
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM contacts WHERE name=?", (name,))
    email = cursor.fetchone()
    return email if email else False


# Function to delete data from emails.db
def delete_emails_data():
    try:
        # Connect to the database
        conn = sqlite3.connect('emails.db')
        cursor = conn.cursor()

        # SQL DELETE statement to delete all data from the table
        cursor.execute('DELETE FROM emails')

        # Commit the transaction
        conn.commit()
        print("Data deleted from 'emails.db' successfully.")

    except Exception as e:
        print("Error deleting data from 'emails.db':", e)

    finally:
        # Close the connection
        if conn:
            conn.close()

def chats():
    conn = sqlite3.connect('Chats.db')
    cursor = conn.cursor()

    # Create the table named 'contacts' with columns 'name' (text) and 'email' (text)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            sr INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            reply TEXT
        )
        """)
    conn.commit()

def add_chats(command, reply):
    chats()
    conn = sqlite3.connect('Chats.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Chats   (command, reply) VALUES(?,?)", (command, reply))
    conn.commit()

# Function to delete data from chats.db
def delete_chats_data():
    try:
        conn = sqlite3.connect('chats.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM chats')

        conn.commit()
        print("Data deleted from 'chats.db' successfully.")

    except Exception as e:
        print("Error deleting data from 'chats.db':", e)

    finally:
        if conn:
            conn.close()