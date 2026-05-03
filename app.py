import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from ai_generator import get_questions, get_chatbot_response
import os

app = Flask(__name__)
app.secret_key = "quiz_secret"

DB_NAME = "chatbot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bot_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            mail TEXT UNIQUE NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exam TEXT NOT NULL,
            subject TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES bot_users(id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB
init_db()

# ---------------- WELCOME PAGE ----------------
@app.route("/")
def welcome():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("welcome.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template("signup.html", msg="Please fill out all fields.")

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        c.execute("SELECT * FROM bot_users WHERE mail=?",(email,))
        user = c.fetchone()

        if user:
            conn.close()
            return render_template("signup.html",msg="Email already exists!")

        c.execute(
        "INSERT INTO bot_users (name,password,mail) VALUES (?,?,?)",
        (name,password,email)
        )
        conn.commit()
        conn.close()

        return render_template("login.html",msg="Signup successful! Login now")

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        if not email or not password:
            return render_template("login.html", msg="Please fill out all fields.")

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
        "SELECT * FROM bot_users WHERE mail=? AND password=?",
        (email,password)
        )
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]   # save username
            session["user_id"] = user[0] # save user_id
            return redirect(url_for("dashboard"))

        return render_template("login.html",msg="Invalid email or password")

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("welcome"))

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template('dashboard.html', name=session["user"])

# ---------------- QUIZ PAGE ----------------
@app.route('/quiz-page')
def quiz_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template('quiz.html')

# ---------------- GENERATE QUIZ API ----------------
@app.route('/generate', methods=['POST'])
def generate():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    try:
        questions = get_questions(
            data.get('exam'), 
            data.get('subject'), 
            data.get('difficulty')
        )
        return jsonify(questions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- CHATBOT PAGE ----------------
@app.route('/chatbot')
def chatbot_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template('chatbot.html', name=session["user"])

# ---------------- CHAT API ----------------
@app.route('/chat', methods=['POST'])
def chat():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    user_message = data.get("message")
    chat_history = data.get("history", [])
    
    try:
        response = get_chatbot_response(user_message, chat_history)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- QUIZ ANALYTICS API ----------------
def get_user_id():
    if "user_id" in session:
        return session["user_id"]
    if "user" in session:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id FROM bot_users WHERE name=?", (session["user"],))
        user = c.fetchone()
        conn.close()
        if user:
            session["user_id"] = user[0]
            return user[0]
    return None

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    uid = get_user_id()
    if not uid:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    exam = data.get("exam")
    subject = data.get("subject")
    score = data.get("score")
    total = data.get("total")
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO quiz_results (user_id, exam, subject, score, total) VALUES (?, ?, ?, ?, ?)",
        (uid, exam, subject, score, total)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/analytics-data', methods=['GET'])
def analytics_data():
    uid = get_user_id()
    if not uid:
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT subject, SUM(score), SUM(total) FROM quiz_results WHERE user_id=? GROUP BY subject",
        (uid,)
    )
    results = c.fetchall()
    conn.close()
    
    data = []
    for r in results:
        subject = r[0]
        total_score = r[1]
        total_questions = r[2]
        percentage = round((total_score / total_questions) * 100) if total_questions > 0 else 0
        data.append({"subject": subject, "percentage": percentage})
        
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)