import unittest
import sqlite3
import os

DB_PATH = '/nfs/demo.db'  # Your SQLite database

class DatabaseLightTests(unittest.TestCase):

    def test_database_exists(self):
        """Check that the SQLite database file exists"""
        self.assertTrue(os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}")

    def test_books_table_exists(self):
        """Check that the 'books' table exists in the database"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books';")
        table = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table, "Books table does not exist in the database")

    def test_sample_data_exists(self):
        """Check that at least one book exists"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM books LIMIT 1;")
        row = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(row, "No data found in 'books' table")

if __name__ == "__main__":
    unittest.main()

