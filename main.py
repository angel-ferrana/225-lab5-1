from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os
import math

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

DATABASE = '/nfs/demo.db'
PER_PAGE_DEFAULT = 10


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    """Initialize the database with a simple books-for-sale table."""
    with app.app_context():
        db = get_db()

        # Drop old table if it exists
        db.execute("DROP TABLE IF EXISTS books")

        # Create the new books table
        db.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL
            );
        ''')

        # Optional sample data
        sample_books = [
            ("The DevOps Handbook", 29.99),
            ("Python Crash Course", 24.50),
            ("Clean Code", 32.00)
        ]
        db.executemany(
            "INSERT INTO books (title, price) VALUES (?, ?)",
            sample_books
        )

        db.commit()
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():

    
    # POST (Add, Update, Delete)
    if request.method == 'POST':
        action = request.form.get('action')

        # DELETE BOOK
        if action == 'delete':
            book_id = request.form.get('book_id')
            if book_id:
                db = get_db()
                db.execute('DELETE FROM books WHERE id = ?', (book_id,))
                db.commit()
                db.close()
                flash('Book deleted successfully.', 'success')
            else:
                flash('Missing book id.', 'danger')
            return redirect(url_for('index'))

        # UPDATE BOOK
        if action == 'update':
            book_id = request.form.get('book_id')
            title = request.form.get('title')
            price = request.form.get('price')

            if book_id and title and price:
                db = get_db()
                db.execute('''
                    UPDATE books
                    SET title=?, price=?
                    WHERE id=?
                ''', (title, price, book_id))
                db.commit()
                db.close()
                flash('Book updated.', 'success')
            else:
                flash('Missing required fields for update.', 'danger')
            return redirect(url_for('index'))

        # ADD NEW BOOK
        title = request.form.get('title')
        price = request.form.get('price')

        if title and price:
            db = get_db()
            db.execute('''
                INSERT INTO books (title, price)
                VALUES (?, ?)
            ''', (title, price))
            db.commit()
            db.close()
            flash('Book added successfully.', 'success')
        else:
            flash('Title and price are required.', 'danger')

        return redirect(url_for('index'))

    
    try:
        page = max(int(request.args.get('page', 1)), 1)
    except ValueError:
        page = 1
    try:
        per_page = max(int(request.args.get('per', PER_PAGE_DEFAULT)), 1)
    except ValueError:
        per_page = PER_PAGE_DEFAULT

    offset = (page - 1) * per_page

    db = get_db()
    total = db.execute('SELECT COUNT(*) FROM books').fetchone()[0]
    books = db.execute(
        'SELECT * FROM books ORDER BY id DESC LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    db.close()

    pages = max(1, math.ceil(total / per_page))
    has_prev = page > 1
    has_next = page < pages
    start_page = max(1, page - 2)
    end_page = min(pages, page + 2)

    return render_template(
        'index.html',
        books=books,
        page=page, pages=pages, per_page=per_page,
        has_prev=has_prev, has_next=has_next, total=total,
        start_page=start_page, end_page=end_page
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)
