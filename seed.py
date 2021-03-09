"""Seed file to make sample data for db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Make a bunch of departments
u1 = User(first_name="Matt", last_name="B")
u2 = User(first_name="Bob", last_name="Knapparatus", image_url="https://media.istockphoto.com/vectors/no-image-available-sign-vector-id922962354?k=6&m=922962354&s=612x612&w=0&h=_KKNzEwxMkutv-DtQ4f54yA5nc39Ojb_KPvoV__aHyU=")
u3 = User(first_name="Daniel", last_name="Knapparatus", image_url="https://media-exp1.licdn.com/dms/image/C4E03AQHUq2o05_xlxw/profile-displayphoto-shrink_200_200/0/1610387942804?e=1620259200&v=beta&t=hROLK_UszkmR08VbM6OOI6j1mKj-nS7SY7tpgETrDuI")
u4 = User(first_name="Bob", last_name="Ross", image_url="https://www.bobross.com/content/bob_ross_img.png")
u5 = User(first_name="Luke", last_name="Skywalker", image_url="https://media.gq.com/photos/56da0101062ab67b27facbd2/1:1/w_1052,h_1052,c_limit/luke-skywalker-gay-.jpg")

db.session.add_all([u1, u2, u3, u4, u5])

db.session.commit()

# Make a bunch of employees

post1 = Post(title="What the hell", content="I don't know what to talk about, but what the hell.", user_id="3")

db.session.add_all([post1])

db.session.commit()