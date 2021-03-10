from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                     nullable=False)
    
    last_name = db.Column(db.String(50),
                     nullable=False)
    
    image_url = db.Column(db.String(300),
                     nullable=False,
                     default='https://media.istockphoto.com/vectors/no-image-available-sign-vector-id922962354?k=6&m=922962354&s=612x612&w=0&h=_KKNzEwxMkutv-DtQ4f54yA5nc39Ojb_KPvoV__aHyU=')

    # Relationship to posts table
    posts = db.relationship('Post', backref='user',cascade="all, delete-orphan")

    def __repr__(self):
        user = self
        return f"<User id={user.id} first_name={user.first_name} last_name={user.last_name} image_url={user.image_url}>"

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # assignments = db.relationship('EmployeeProject', backref='employee')

    tags = db.relationship('Tag', secondary="posts_tags", backref="posts")

    def __repr__(self):
        return f"<Post id={self.id} title={self.title} create_at={self.create_at} user_id={self.user_id} >"

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %#d  %Y, %#I:%M %p")

class PostTag(db.Model):
    """Posts/Tags Model"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True)

class Tag(db.Model):
    """Tag Model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)