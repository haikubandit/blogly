"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User, Post

import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

# db.create_all()

@app.route('/')
def home_page():
    """Show home Page"""

    return redirect('/users')

@app.route('/users')
def users_page():
    """Shows list of all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=["GET"])
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
    posts = db.session.query(Post).filter(Post.user_id == user_id)

    return render_template("user_details.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def edit_user_page(user_id):
    """Show form to edit user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_db_update(user_id):
    """Update user in db and redirect to users page"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user from db and redirect to users page"""
    User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/users')



########### Routes for User Posts ###########


@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post_page(user_id):
    """Show form to create new post from a user's page"""

    user = User.query.get_or_404(user_id)
    
    return render_template('new_post.html', user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post_db_update(user_id):
    """Add new post for user to db and redirect to user details page"""

    title = request.form["title"]
    content = request.form["content"]

    new_post  = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def post_detail_page(post_id):
    """Show post details"""
    post = Post.query.get_or_404(post_id)

    return render_template("post_details.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post_page(post_id):
    """Show post detail edit form."""
    post = Post.query.get_or_404(post_id)

    return render_template("post_details_edit.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_db_update(post_id):
    """Update post details in db and redirect to post details page"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post from db and redirect to user details page"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")