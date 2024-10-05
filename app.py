from datetime import datetime, timezone

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///snake.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Load game settings"""    
    rows = get_user_settings()
    session['user_score'] = 0
    session['speed_value'] = rows[0]["speed"]
    session['border_obstacle'] = rows[0]["border_obstacle"] == 1
    game_settings = {
        "score": 0,
        "speed": get_game_speed(rows[0]["speed"]),
        "speed_value": rows[0]["speed"],
        "food_color": rows[0]["food_color"],
        "snake_color": rows[0]["snake_color"],
        "background_color": rows[0]["background_color"],
        "border_obstacle": session['border_obstacle']
    }
    return render_template("index.html", settings=game_settings)


@app.route("/catch_food")
@login_required
def catch_food():
    """Update game score"""
    session['user_score'] += session['speed_value']
    if session['border_obstacle']:
        session['user_score'] += 2
    return ('', 200)


@app.route("/game_over")
@login_required
def game_over():
    """Process game over"""
    db.execute("INSERT INTO scores (user_id, score) VALUES(?, ?)", session["user_id"], session['user_score'])
    return ('', 200)


@app.route("/scores")
@login_required
def scores():
    """Show top 15 best game scores"""
    rows = db.execute("select S.score as score, U.username as login, S.createdOn as date, U.id as user_id from scores S join users U on U.id = S.user_id ORDER BY S.score DESC LIMIT 15")
    for item in rows:
        item['style_class'] = 'bold_row' if item['user_id'] == session["user_id"] else 'common_row'
    return render_template("scores.html", scores=rows)


@app.route("/about")
@login_required
def about():
    """Show project description"""
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        db.execute("UPDATE users SET visitedOn = ? WHERE id = ?", datetime.now(timezone.utc), session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)
        # Ensure confirmation was submitted
        elif not confirmation:
            return apology("must provide password confirmation", 400)
        # Ensure password was submitted
        elif not confirmation == password:
            return apology("password and its confirmation don't match", 400)
        # Try save new user
        try:
            hash_psd = generate_password_hash(password)
            # Query database for username
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash_psd)
            rows = db.execute("SELECT id FROM users WHERE username = ?", username)
            user_id = rows[0]["id"]
            db.execute("INSERT INTO settings (user_id, food_color, snake_color, background_color, speed, border_obstacle) VALUES(?, ?, ?, ?, ?, ?)", user_id, "#0e7707", "#e56f0a", "#2a73be", 5, 0)
            return redirect("/login")
        except ValueError:
            return apology("User already exists", 400)
    return render_template("/register.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Open settings section"""
    rows = get_user_settings()
    if request.method == "POST":
        speed = request.form.get("speed")
        food_color = request.form.get("food_color")
        snake_color = request.form.get("snake_color")
        background_color = request.form.get("background_color")
        border_obstacle = 1 if request.form.get("border_obstacle") else 0
        db.execute("UPDATE settings SET food_color = ?, snake_color = ?, background_color = ?, speed = ?, border_obstacle = ? WHERE user_id = ?", food_color, snake_color, background_color, speed, border_obstacle, session['user_id'])
        return redirect("/")
    user_settings = {
        "speeds": [1,2,3,4,5,6,7,8,9,10],
        "speed": rows[0]["speed"] - 1,
        "food_color": rows[0]["food_color"],
        "snake_color": rows[0]["snake_color"],
        "background_color": rows[0]["background_color"],
        "border_obstacle": rows[0]["border_obstacle"] == 1
    }
    return render_template("settings.html", settings=user_settings)


def get_user_settings():
    """Return user settings"""
    return db.execute("SELECT food_color, snake_color, background_color, speed, border_obstacle FROM settings WHERE user_id = ?", session['user_id'])


def get_game_speed(speed_key):
    """Process game speed values"""
    game_speed_values = {
        1: 500,
        2: 450,
        3: 400,
        4: 350,
        5: 300,
        6: 250,
        7: 200,
        8: 150,
        9: 100,
        10: 50
    }
    return game_speed_values[speed_key]
