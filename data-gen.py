import sqlite3
import random

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_books):
    """Generate test data for the books table."""
    db = connect_db()

    for i in range(num_books):
        title = f'Test Book {i}'
        price = round(random.uniform(5.0, 50.0), 2)

        db.execute(
            'INSERT INTO books (title, price) VALUES (?, ?)',
            (title, price)
        )

    db.commit()
    print(f'{num_books} test books added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test books
