# 📚 BookVerse - Digital Bookstore

Welcome to **BookVerse**, a secure, lightweight, and modern digital bookstore web application. Built with **Flask** and **SQLite3**, BookVerse offers users an intuitive platform to browse educational books, securely register and login, manage their profiles, make purchases, and track order histories. It also provides a robust **Admin Panel** to monitor analytics, total revenue, and order transactions.

---

## ✨ Features

### 👤 User Features
*   **Secure Authentication**: User signup, login, and session-based authentication with password hashing (`SHA-256` and Werkzeug security integration).
*   **Password Management**: Users can update their accounts and change passwords securely.
*   **Digital Book Catalog**: Interactive catalog containing items such as *Ethical Hacking*, *Python Programming*, and *Networking*.
*   **Interactive Checkout & Order Success**: Checkout form requiring customer name, phone, address, and payment method selection, leading to an automated confirmation screen.
*   **Order History**: A personal "My Purchases" area where users can track all their successfully ordered books and payment methods.

### 🛡️ Admin Features
*   **Admin Dashboard**: A secure portal (`/admin`) dedicated to bookstore managers.
*   **Real-time Analytics**: Displays total registered users, total books purchased, and live cumulative revenue calculations.
*   **Detailed Audit Log**: Chronological feed of recent transactions displaying purchaser emails, book titles, and payment methods.

---

## 🏗️ Project Structure

```text
BookVerse/
│
├── database/                   # Database files and schemas
│   ├── db.py                   # Schema initialization script
│   ├── bookverse.db            # SQLite database file (auto-generated)
│   └── users.db                # SQLite user database file (legacy)
│
├── static/                     # Static files (CSS, images, etc.)
│   ├── css/
│   │   └── style.css           # Core styling for the app
│   └── images/                 # Image assets
│
├── templates/                  # Flask HTML view templates
│   ├── admin.html              # Admin panel view
│   ├── admin_login.html        # Admin login page
│   ├── book.html               # Book details page
│   ├── change_password.html    # Update password form
│   ├── checkout.html           # Checkout billing page
│   ├── dashboard.html          # User profile homepage
│   ├── index.html              # Main welcome page
│   ├── login.html              # User login form
│   ├── my_purchases.html       # Purchases history table
│   ├── purchase.html           # Purchasing details layout
│   ├── register.html           # User signup form
│   └── success.html            # Thank you/order success page
│
├── app.py                      # Main Flask server logic & routing
├── requirements.txt            # Python dependencies lists
└── .gitignore                  # Git untracked files pattern
```

---

## ⚡ Quick Start Guide (Local Setup)

Follow these steps to run the application locally on your machine.

### Prerequisites
Make sure you have **Python 3.8+** installed. You can verify this by running:
```bash
python --version
```

### 1. Clone the Repository
Open a terminal in your workspace and run:
```bash
git clone https://github.com/xxKrishna2609xx/Book_Service_123.git
cd BookVerse
```

### 2. Create and Activate a Virtual Environment (Recommended)
Setting up a virtual environment ensures dependencies don't conflict with other Python projects on your machine.

*   **On Windows (PowerShell/CMD):**
    ```powershell
    python -m venv venv
    venv\Scripts\activate
    ```
*   **On macOS / Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Install Dependencies
Install all required libraries using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Initialize the Database
Run the setup script inside the `database` folder to generate the SQLite database structure:
```bash
python database/db.py
```
> [!NOTE]
> This creates a new file `database/bookverse.db` and populates the `users` and `purchases` tables.

### 5. Launch the Server
Start the Flask development server:
```bash
python app.py
```
Once run, you will see output similar to this:
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser to access the website!

---

## 🔑 Demo Access Credentials

To test both the customer and admin flows out of the box, use the following details:

### User Account (To test purchases & checkout)
1. Navigate to **Register** and create a new customer account.
2. Log in and purchase books to verify checkout, order history, and payment success flows.

### Admin Dashboard (To inspect bookstore metrics)
1. Go to URL path: [http://127.0.0.1:5000/admin-login](http://127.0.0.1:5000/admin-login)
2. Log in with the following default administrator credentials:
    *   **Email**: `admin@bookverse.com`
    *   **Password**: `admin123`
3. Check the real-time statistics and recent purchases logged.

---

## 🚀 Deployment Guide

When deploying BookVerse to cloud environments, you have multiple options. Below is the configuration walkthrough for deploying on **Render** (a popular, free-tier hosting alternative to Heroku).

### 🖥️ Option A: Deploying on Render (Web Service)
1. Sign in to [Render](https://render.com/).
2. Click **New** ➡️ **Web Service**.
3. Connect your GitHub repository (`Book_Service_123`).
4. Configure the Web Service settings as follows:
    *   **Name**: `bookverse-store`
    *   **Language**: `Python`
    *   **Branch**: `main` (or your active branch)
    *   **Region**: Select a region close to your user base.
    *   **Build Command**:
        ```bash
        pip install -r requirements.txt && python database/db.py
        ```
    *   **Start Command**:
        ```bash
        gunicorn app:app
        ```
5. Choose the **Free** instance type and click **Create Web Service**.

> [!WARNING]
> **Important SQLite Limitation in Ephemeral Hosting:**
> Cloud platforms like Render have an **ephemeral file system**. When your Web Service restarts (e.g. during a deploy or automatically once a day), any changes written directly to local files—including your SQLite database `database/bookverse.db`—will be lost.
> 
> **To solve this for production, you have two options:**
> 1.  **Render Persistent Disks (Recommended for SQLite):** Under your service dashboard in Render, go to **Disks** ➡️ **Add Disk**. Mount it at `/opt/render/project/src/database` with a size of 1GB. This prevents database resets.
> 2.  **External Database:** Modify `app.py` to use an external PostgreSQL database (e.g., Neon or Supabase) by changing the connection driver.

### 🐧 Option B: Running on a VPS (Ubuntu/Nginx)
If you deploy to a Virtual Private Server (DigitalOcean, AWS EC2, Linode):
1. Clone the project onto the VPS.
2. Install Python, create a virtual environment, and run the dependencies installation.
3. Configure `gunicorn` to run as a system service daemon (systemd).
4. Configure **Nginx** as a reverse proxy, mapping port `80` (HTTP) or `443` (HTTPS) to Gunicorn's default port (`8000`).

---

## 🔒 Security Best Practices
For public production deployments:
1.  **Change Secret Key**: Update the `secret_key` variable in `app.py` to use an environment variable:
    ```python
    import os
    app.secret_key = os.environ.get("SECRET_KEY", "fallback_local_secret")
    ```
2.  **Update Default Admin Password**: Change the hardcoded admin password in `app.py` (lines 301-303) or move it to environment variables.
3.  **Enable HTTPS**: Ensure your hosting provider handles SSL/TLS termination to protect user login passwords during transit.
