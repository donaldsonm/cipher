import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Create important lists
    symbols = []
    amounts = []
    stockprices = []
    totalprices = []

    # Obtain type and amount of stocks that the user has
    symbol_select = db.execute(
        "SELECT symbol FROM transactions WHERE id = :id GROUP BY symbol ORDER BY symbol", id=session["user_id"])
    amount_select = db.execute(
        "SELECT SUM(amount) AS amounts FROM transactions WHERE id = :id GROUP BY symbol ORDER BY symbol", id=session["user_id"])

    # Insert the necessary information (symbol, quantity, stock price, total price) into multiple lists
    for item in range(len(symbol_select)):
        if amount_select[item]['amounts'] == 0:
            continue
        symbols.append(symbol_select[item]['symbol'])
        amounts.append(amount_select[item]['amounts'])
        stockprices.append((lookup(symbol_select[item]['symbol']))["price"])
        totalprices.append((lookup((symbol_select[item]['symbol'])))["price"] * (amount_select[item]['amounts']))

    # Combine multiple list into one list that can be displayed via HTML
    stocks = list(zip(symbols, amounts, stockprices, totalprices))

    # Obtain current cash of user
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

    # Calculate grand total cash
    grandtotal = cash[0]['cash'] + sum(totalprices)

    # Display table
    return render_template("index.html", stocks=stocks, cash=cash, total=grandtotal)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure symbol is valid
        elif lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol", 400)

        elif (request.form.get("shares")).isdigit() == False:
            return apology("shares must be integer", 400)

        elif int(request.form.get("shares")) < 0:
            return apology("shares must be positive", 400)

        quotes = lookup(request.form.get("symbol"))

        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        stockprice = quotes["price"]

        # Total cost of share(s) of stock
        total = float(stockprice) * float(request.form.get("shares"))

        # Check whether user has enough money to buy share(s) of stock
        if cash[0]['cash'] < total:
            return apology("can't afford", 400)

        # Update portfolio by adding who bought what for how much at what time
        db.execute("INSERT INTO transactions (id, symbol, amount, totalprice, datetime, stockprice) VALUES (:id, :symbol, :amount, :totalprice, datetime('now'), :stockprice)",
                   id=session["user_id"], symbol=(request.form.get("symbol")).upper(), amount=request.form.get("shares"), totalprice=total, stockprice=stockprice)

        # Update amount of cash that user has
        db.execute("UPDATE users SET cash = cash - :total WHERE id = :user_id", total=total, user_id=session["user_id"])

        # Redirect to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Grab information from transaction database
    history = db.execute("SELECT symbol, amount, totalprice, datetime FROM transactions WHERE id = :id",
                         id=session["user_id"])

    # Display table of transaction history
    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # Send user to form where they can enter which stock they would like to check
    if request.method == "GET":
        return render_template("quote.html")

    # Display stock quote
    else:
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure symbol is valid
        if lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol", 400)

        quotes = lookup(request.form.get("symbol"))

        # Return price of stock
        return render_template("quoted.html", name=quotes["symbol"], price=quotes["price"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords didn't match", 400)

        # Ensure password meets requirements
        elif len(request.form.get("password")) < 6 or (request.form.get("password")).isalpha() == True:
            return apology("password must meet requirements", 400)

        hash_pass = generate_password_hash(request.form["password"])

        # Add username and hashed password to database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=hash_pass)

        # Ensure username is unique
        if not result:
            return apology("username taken", 400)

        # Log in user right after they register
        session["user_id"] = result

        # Redirect to homepage of website
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # Ensure user inputted symbol
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Ensure user inputted shares
        elif not request.form.get("shares"):
            return apology("missing shares", 400)

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Obtain total amount of stocks that the user owns of a particular type
        stocknumber = db.execute("SELECT SUM(amount) AS amounts FROM transactions WHERE id = :id AND symbol = :symbol GROUP BY symbol ORDER by symbol",
                                 id=session["user_id"], symbol=symbol)

        # Ensure the user has enough shares to sell
        if int(stocknumber[0]['amounts']) < int(shares):
            return apology("not enough shares", 400)

        # Calculate the total amount of money they will get
        money = (lookup(symbol))["price"] * int(request.form.get("shares"))

        # Insert transaction as a negative quantity (selling)
        sell = db.execute("INSERT INTO transactions (id, symbol, amount, totalprice, datetime, stockprice) VALUES (:id, :symbol, :amount, :totalprice, datetime('now'), :stockprice)",
                          id=session["user_id"], symbol=symbol, amount=int(shares) * -1, totalprice=money, stockprice=(lookup(symbol))["price"])

        # Update cash that user has
        user_cash = (db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]))[0]['cash']

        db.execute("UPDATE users SET cash = :cash WHERE id = :id", id=session["user_id"], cash=user_cash + money)

        return redirect("/")

    else:
        # Obtain type of stocks that user owns
        symbol = db.execute("SELECT symbol FROM transactions WHERE id = :id GROUP BY symbol ORDER BY symbol",
                            id=session["user_id"])

        # Display form
        return render_template("sell.html", stocks=symbol)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

app.jinja_env.globals.update(usd=usd)