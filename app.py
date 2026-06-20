from flask import Flask, render_template, request, redirect, session, abort,url_for
from markupsafe import escape
import hashlib
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "bookverse_secret"


BOOKS = {
    "ethical-hacking": {
        "title": "Ethical Hacking",
        "price": "₹499",
        "description": "Complete Cyber Security and Ethical Hacking Guide.",
    },
    "python-programming": {
        "title": "Python Programming",
        "price": "₹699",
        "description": "Learn Python from Beginner to Advanced.",
    },
    "networking": {
        "title": "Networking",
        "price": "₹599",
        "description": "Master Computer Networking Fundamentals.",
    },
}


def get_db_connection():
    conn = sqlite3.connect("database/bookverse.db")
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(stored_password, password):
    if stored_password.startswith(("pbkdf2:", "scrypt:", "argon2:")):
        return check_password_hash(stored_password, password)

    if len(stored_password) == 64:
        return stored_password == hash_password(password)

    return stored_password == password


# Home Page
@app.route("/")
def home():
    user = session.get("user")
    return render_template("index.html", user=user)


# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "Email already exists!"

        cursor.execute(
            "INSERT INTO users(name, email, password) VALUES (?, ?, ?)",
            (name, email, hash_password(password))
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        if not user or not verify_password(user["password"], password):
            conn.close()
            return "Invalid Email or Password"

        if len(user["password"]) != 64:
            cursor.execute(
                "UPDATE users SET password=? WHERE email=?",
                (hash_password(password), email)
            )
            conn.commit()

        conn.close()

        session["user"] = email
        return redirect("/dashboard")

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        email=session["user"]
    )


# Logout
@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/")


# Book Details
@app.route("/book/<book_name>")
def book_details(book_name):

    book = BOOKS.get(book_name)

    if book is None:
        abort(404)

    return render_template(
        "book.html",
        book=book,
        book_slug=book_name
    )


@app.route('/purchase/<book_name>')
def purchase(book_name):
    if 'user' not in session:
        return redirect('/login')

    book = BOOKS.get(book_name)

    if book is None:
        abort(404)

    return render_template(
        'purchase.html',
        book_name=book["title"],
        book_slug=book_name,
        book_price=book["price"],
        book_description=book["description"],
        user_email=session['user']
    )


@app.route('/checkout/<book_name>')
def checkout(book_name):
    return purchase(book_name)


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            return 'New password and confirm password do not match.'

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT password FROM users WHERE email=?', (session['user'],))
        user = cursor.fetchone()

        if not user or not verify_password(user['password'], current_password):
            conn.close()
            return 'Current password is incorrect.'

        cursor.execute(
            'UPDATE users SET password=? WHERE email=?',
            (hash_password(new_password), session['user'])
        )
        conn.commit()
        conn.close()

        return 'Password updated successfully.'

    return render_template('change_password.html')


@app.route('/success', methods=['POST'])
def success():

    if 'user' not in session:
        return redirect('/login')

    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    payment_method = request.form['payment_method']
    book_slug = request.form['book_slug']

    book = BOOKS.get(book_slug)

    if book is None:
        abort(404)

    email = session['user']
    book_name = book['title']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO purchases (email, book_name, payment_method) VALUES (?, ?, ?)",
        (email, book_name, payment_method)
    )

    conn.commit()
    conn.close()

    return render_template(
        'success.html',
        name=name,
        email=email,
        phone=phone,
        address=address,
        payment_method=payment_method,
        book_name=book_name
    )


@app.route('/my-purchases')
def my_purchases():

    if 'user' not in session:
        return redirect('/login')

    email = session['user']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM purchases WHERE email=?",
        (email,)
    )

    purchases = cursor.fetchall()

    conn.close()

    return render_template(
        'my_purchases.html',
        purchases=purchases
    )


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        if email == "admin@bookverse.com" and password == "admin123":
            session['admin'] = True
            return redirect('/admin')

        return "Wrong Admin Credentials"

    return render_template('admin_login.html')


@app.route('/admin')
def admin():

    if 'admin' not in session:
        return redirect('/admin-login')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Total Users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Total Purchases
    cursor.execute("SELECT COUNT(*) FROM purchases")
    total_purchases = cursor.fetchone()[0]

    # Revenue
    cursor.execute("""
        SELECT SUM(
            CASE
                WHEN book_name='Ethical Hacking' THEN 499
                WHEN book_name='Python Programming' THEN 699
                WHEN book_name='Networking' THEN 599
                ELSE 0
            END
        )
        FROM purchases
    """)

    revenue = cursor.fetchone()[0]

    if revenue is None:
        revenue = 0

    # Recent Purchases
    cursor.execute("""
        SELECT email, book_name, payment_method
        FROM purchases
        ORDER BY id DESC
    """)

    purchases = cursor.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        total_users=total_users,
        total_purchases=total_purchases,
        revenue=revenue,
        purchases=purchases
    )


if __name__ == "__main__":
    app.run(debug=True)
