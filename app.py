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
    """Shows list of all pets in db"""
    
    return render_template('create_user.html')

@app.route("/users/<int:user_id>")
def user_detail_page(user_id):
    """Show details about a single pet"""
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)