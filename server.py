"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""
    return render_template('homepage.html')

@app.route("/movies")
def all_movies():
    """View all movies"""
    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""
    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)
# Replace this with routes and view functions!

@app.route("/users",)
def all_users():
    """View all users"""
    users = crud.get_users()
    return render_template("all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user is True:
        flash("An account with this email already exists. Try again!")
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("You're now a true movie buFF!Your account was successfully created!")

    return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user =crud.get_user_by_id(user_id)

    return render_template("user_details.html",user=user)

@app.route("/login", methods=["POST"])
def login_form_submission():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user.email == False or user.password != password:
        flash("The email OR password you entered is incorrect! Try Again! ")
    else:
        session["email"] =user.email
        flash(f"Welcome! You are now logged in as {user.email}!")

    return redirect("/")

@app.route('/user_ratings' method=["POST"])
def user_rating():
    """Get user rating from submit button"""

    rating = request.form.get()


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
