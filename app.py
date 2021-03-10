"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User, Post, Tag, PostTag

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
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template("home.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


###################### USER ROUTES ###############################

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
    tags = Tag.query.all()
    
    return render_template('new_post.html', user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post_db_update(user_id):
    """Add new post for user to db and redirect to user details page"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    
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
    tags = Tag.query.all()

    return render_template("post_details_edit.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_db_update(post_id):
    """Update post details in db and redirect to post details page"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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



########### Tags  ###########


@app.route('/tags')
def tags_list_page():
    """Shows list of all users"""

    tags = Tag.query.order_by(Tag.name).all()

    return render_template('tags.html', tags=tags)


@app.route('/tags/new', methods=["GET"])
def create_tag_page():
    """Show form to create new users"""
    
    return render_template('create_tag.html')


@app.route('/tags/new', methods=["POST"])
def create_tag_db_update():
    """Add new user to db and redirect to users page"""

    name = request.form["tag-name"]

    new_tag  = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def tag_details_page(tag_id):
    """Shows list of all users"""

    tag = Tag.query.get_or_404(tag_id)

    posts = tag.posts

    return render_template('tag_details.html', tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["GET"])
def edit_tag_page(tag_id):
    """Show post detail edit form."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag_db_update(tag_id):
    """Update post details in db and redirect to post details page"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tag-name"]

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags/{tag.id}")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tag_delete(tag_id):
    """Handle form submission for deleting an existing post"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name} deleted.")

    return redirect("/tags")