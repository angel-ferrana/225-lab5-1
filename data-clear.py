import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_test_books():
    """Clear only the test books from the database."""
    db = connect_db()
    db.execute("DELETE FROM books WHERE title LIKE 'Test Book %'")
    db.commit()
    print('Test books have been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_test_books()
