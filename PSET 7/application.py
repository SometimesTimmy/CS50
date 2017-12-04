from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
# html table with user's portfolio showing stocks owned, shares owned for each stock, current price of each stock, and total value of each holding
    # user's current cash balanc
        # db.execute will always return an array
    rows = db.execute("SELECT cash FROM users WHERE id = :id", \
        id = session["user_id"])
    fund = float(rows[0]['cash'])

    # grand total of cash + stocks' total value
    grand_total = fund # for now only. total value of each holding will be added by the for loop below

    portfolio = db.execute("SELECT * FROM portfolio WHERE id = :id", \
        id = session["user_id"])

    for stock in portfolio:
        symbol = stock["symbol"]
        shares = stock["shares"]
        quote = lookup(symbol)
        name = quote["name"]
        price = quote["price"]
        total = shares*price
        # since the previously recorded stock price may have changed, portfolio db should be updated each time index.html is displayed
        db.execute("UPDATE portfolio SET price = :price, total = :total WHERE id = :id AND symbol = :symbol", \
            price = usd(price), \
            total = usd(total), \
            id = session["user_id"], \
            symbol = symbol)
        grand_total += total

    return render_template("index.html", portfolio = portfolio, cash=usd(fund), grand_total=usd(grand_total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    #1 display form
    # ask for symbol and number of shares
    if request.method == "GET":
        return render_template("buy.html")

    else: # request.method == "POST"

    # check if valid input: valid symbol and number > 0
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("both symbol and number of shares desired to be purchased must be entered")

        shares = request.form.get("shares")
        if not shares.isnumeric():
            return apology("invalid quantity of shares")

        shares = float(shares)
        if shares < 0:
            return apology("number of shares must be greater than 0")

        quote = lookup(request.form.get("symbol")) # from helpers.py
        if not quote:
            return apology("invalid stock symbol. re-enter")

    #2 add stock to user's portfolio if they have enough cash
        rows = db.execute("SELECT cash FROM users WHERE id = :id", \
            id = session["user_id"])
        fund = float(rows[0]['cash'])
        price = float(quote['price'])
        cost = shares*price
        if cost > fund:
            return apology("insufficient fund")
        else:
            # reminder before actually "buying", CREATE TABLE within finance.db
            # record the purchase into history
            db.execute("INSERT INTO history (id, symbol, shares, price) VALUES(:id, :symbol, :shares, :price)", \
                id = session["user_id"], \
                symbol = request.form.get("symbol"), \
                shares = shares, \
                price = price)

            # add the purchased stock into the portfolio db
            rows = db.execute("SELECT * FROM portfolio where id = :id AND symbol = :symbol", \
                id = session["user_id"], \
                symbol = request.form.get("symbol"))

            if not rows: # first time purchasing this stock on this account
                db.execute("INSERT INTO portfolio (id, symbol, name, shares, price, total) VALUES(:id, :symbol, :name, :shares, :price, :total)", \
                    id = session["user_id"], \
                    symbol = request.form.get("symbol"), \
                    name = quote["name"], \
                    shares = shares, \
                    price = quote["price"], \
                    total = usd(cost))
            else: # add the newly purchase quantity of shares into the existing portfolio
                current_shares = db.execute("SELECT * FROM portfolio where id = :id AND symbol = :symbol", \
                    id = session["user_id"], \
                    symbol = request.form.get("symbol"))
                current_shares = float(current_shares[0]["shares"])
                db.execute("UPDATE portfolio SET shares = :shares WHERE id = :id AND symbol = :symbol", \
                    shares = current_shares + shares, \
                    id = session["user_id"], \
                    symbol = request.form.get("symbol"))

    #3 update cash to reflect the purchase that was just made^
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", \
                cash = fund - cost, \
                id = session["user_id"])

            return redirect(url_for("index"))

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    rows = db.execute("SELECT * FROM history WHERE id = :id", \
        id = session["user_id"])

    return render_template("history.html", histories = rows)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", \
            username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # POST supplies data from the client to the database
    #1 display form
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must enter symbol")
    #2 retrieve stock quote
        symbol = request.form.get("symbol")
        symbol = symbol.upper()
        quote = lookup(symbol) # from helpers.py
            # "name": symbol.upper(), # for backward compatibility with Yahoo
            # "price": price,
            # "symbol": symbol.upper()

    #3 display stock quote
        # ensure the stock is valid
        if not quote:
            return apology("invalid stock symbol. re-enter")
        else:
            # lookup will return a dict that contains name, price, symbol
            quote['price'] = usd(quote['price']) # from helpers.py
            return render_template("display_quote.html", stock=quote)

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget an user_id
    session.clear()

    # make sure to use a POST request
    # https://www.diffen.com/difference/GET-vs-POST-HTTP-Requests
    # POST supplies data from the client to the database

    #1 display form

    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

    #2 valid passwords?
        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password confirmation was submitted
        elif not request.form.get("confirmpassword"):
            return apology("must provide password confirmation")

        # ensure password and password confirmation matches
        elif not request.form.get("password") == request.form.get("confirmpassword"):
            return apology("passwords do not match. re-enter")

        #else register the user per below

    #3 add user to database
        # hash password
        # username and id should be unique
        # in case user already exist db.execute will fail.
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", \
            username = request.form.get("username"), \
            hash = pwd_context.hash(request.form.get("password")))

        if not result:
            return apology("username taken")

        # from "def login():"
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", \
            username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

    #4 log them in
        #once registered successfully, log the user in automatically
        session["user_id"] = rows[0]["id"]

        return redirect(url_for("index")) # send the user to their main page to get started

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    #1 display form
    # ask for symbol and number of shares
    if request.method == "GET":
        return render_template("sell.html")

    else: # request.method == "POST"

    # check if valid input: valid symbol and number > 0
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("both symbol and number of shares desired to be purchased must be entered")

        quote = lookup(request.form.get("symbol")) # from helpers.py
        shares_sell = float(request.form.get("shares"))

        if shares_sell < 0:
            return apology("number of shares must be greater than 0")
        if not quote:
            return apology("invalid stock symbol. re-enter")

    #2 check user's portfolio to confirm if sufficient shares are available to sell
        shares_available = db.execute("SELECT shares FROM portfolio WHERE id = :id and symbol = :symbol", \
            id = session["user_id"], \
            symbol = request.form.get("symbol"))
        shares_available = float(shares_available[0]["shares"])

        if not shares_available:
            return apology("you do not own any shares of this stock")

        if shares_sell > shares_available:
            return apology("insufficient quantity of shares")

        price = float(quote['price'])

        # log a sale as a negative quantity into the history db
        db.execute("INSERT INTO history (id, symbol, shares, price) VALUES(:id, :symbol, :shares, :price)", \
            id = session["user_id"], \
            symbol = request.form.get("symbol"), \
            shares = -shares_sell, \
            price = price)

        # log a sale as a negative quantity into the portfolio db
        current_shares = db.execute("SELECT * FROM portfolio where id = :id AND symbol = :symbol", \
                id = session["user_id"], \
                symbol = request.form.get("symbol"))

        current_shares = float(current_shares[0]["shares"])

        if current_shares > shares_sell:
            db.execute("UPDATE portfolio SET shares = :shares WHERE id = :id AND symbol = :symbol", \
                shares = current_shares - shares_sell, \
                id = session["user_id"], \
                symbol = request.form.get("symbol"))
        elif current_shares == shares_sell:
            db.execute("DELETE FROM portfolio WHERE id = :id AND symbol = :symbol", \
                id = session["user_id"], \
                symbol = request.form.get("symbol"))

    #3 update cash to reflect the sale that was just made^
        rows = db.execute("SELECT cash FROM users WHERE id = :id", \
            id = session["user_id"])
        fund = float(rows[0]['cash'])
        sale = shares_sell*price

        db.execute("UPDATE users SET cash = :cash WHERE id = :id", \
            cash = fund + sale, \
            id = session["user_id"])

        return redirect(url_for("index"))

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Update user's password."""

    if request.method == "POST":
    # confirm all fields are entered
        if not request.form.get("password"):
            return apology("must provide existing password")
        elif not request.form.get("confirmpassword"):
            return apology("must confirm existing password")
        elif not request.form.get("new_password"):
            return apology("must provide new password")
        elif not request.form.get("new_confirmpassword"):
            return apology("must confirm new password")

    # confirm old and new passwords match
        if not request.form.get("password") == request.form.get("confirmpassword"):
            return apology("existing passwords do not match. re-enter")
        elif not request.form.get("new_password") == request.form.get("new_confirmpassword"):
            return apology("new passwords do not match. re-enter")

        if pwd_context.hash(request.form.get("password")) == db.execute("SELECT hash FROM users WHERE id = :id", \
            id = session["user_id"]):
                return apology("existing password does not match the record. re-enter")

        db.execute("UPDATE users SET hash = :hash WHERE id = :id", \
            hash = pwd_context.hash(request.form.get("new_password")), \
            id = session["user_id"])

        session.clear() # log the user out and...
        return redirect(url_for("login")) # return the user to the log-in page to log back in

    else:
        return render_template("password.html")