"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route('/')
def home_page():
    """Show home Page"""

    return redirect('/users')

@app.route('/users')
def users_page():
    """Shows list of all users"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def create_user_page():
    """Show form to create new users"""
    
    return render_template('create_user.html')

@app.route('/users/new', methods=["POST"])
def create_user_db_update():
    """Add new user to db and redirect to users page"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    image_url = str(image_url) if image_url else None

    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>")
def user_detail_page(user_id):
    """Show user details"""
    user = User.query.get_or_404(user_id)

    return render_template("user_details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user_page(user_id):
    """Show form to edit user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_db_update(user_id):
    """Update user in db and redirect to users page"""
    user = User.query.get_or_404(user_id)

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user from db and redirect to users page"""
    User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/users')