from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

bot = Flask(__name__)
bot.secret_key = "quiz_secret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mot1v@tion",
    database="chatBot"
)

cursor = db.cursor()

# ---------------- WELCOME PAGE ----------------
@bot.route("/")
def welcome():
    return render_template("welcome.html")

# ---------------- SIGNUP ----------------
@bot.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM bot_users WHERE mail=%s",(email,))
        user = cursor.fetchone()

        if user:
            return render_template("signup.html",msg="Email already exists!")

        cursor.execute(
        "INSERT INTO bot_users (name,password,mail) VALUES (%s,%s,%s)",
        (name,password,email)
        )
        db.commit()

        return render_template("login.html",msg="Signup successful! Login now")

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@bot.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
        "SELECT * FROM bot_users WHERE mail=%s AND password=%s",
        (email,password)
        )

        user = cursor.fetchone()

        if user:
            session["user"] = user[1]   # save username
            return redirect(url_for("welcome"))

        return render_template("login.html",msg="Invalid email or password")

    return render_template("login.html")


# ---------------- START QUIZ ----------------
@bot.route("/quiz")
def quiz():

    if "user" not in session:
        return render_template("welcome.html",msg="Please login or signup first")

    return render_template("index.html",name=session["user"])


# ---------------- LOGOUT ----------------
@bot.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("welcome"))


if __name__ == "__main__":
    bot.run(debug=True)