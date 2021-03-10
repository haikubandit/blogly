"""Seed file to make sample data for db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()


# posts_tags.PostTag.query.delete()
# posts.Post.query.delete()
# users.User.query.delete()
# tags.Tag.query.delete()

# Make a bunch of users
u1 = User(first_name="Matt", last_name="B")
u2 = User(first_name="Bob", last_name="Knapparatus", image_url="https://media.istockphoto.com/vectors/no-image-available-sign-vector-id922962354?k=6&m=922962354&s=612x612&w=0&h=_KKNzEwxMkutv-DtQ4f54yA5nc39Ojb_KPvoV__aHyU=")
u3 = User(first_name="Daniel", last_name="Knapparatus", image_url="https://media-exp1.licdn.com/dms/image/C4E03AQHUq2o05_xlxw/profile-displayphoto-shrink_200_200/0/1610387942804?e=1620259200&v=beta&t=hROLK_UszkmR08VbM6OOI6j1mKj-nS7SY7tpgETrDuI")
u4 = User(first_name="Bob", last_name="Ross", image_url="https://www.bobross.com/content/bob_ross_img.png")
u5 = User(first_name="Luke", last_name="Skywalker", image_url="https://media.gq.com/photos/56da0101062ab67b27facbd2/1:1/w_1052,h_1052,c_limit/luke-skywalker-gay-.jpg")

db.session.add_all([u1, u2, u3, u4, u5])

db.session.commit()

# Make a bunch of posts

post1 = Post(title="What the hell", content="I don't know what to talk about, but what the hell.", user_id=u3.id)
post2 = Post(title="I love painting!", content="Birds and mountains are my favorite!", user_id=u4.id)
post3 = Post(title="Darkside", content="Had another scuffle with Vader", user_id=u5.id)
post4 = Post(title="Obiwan", content="Why did he leave me!!", user_id=u5.id)

db.session.add_all([post1, post2, post3, post4])

db.session.commit()

# Make a bunch of tags

art = Tag(name='Art')
star_wars = Tag(name='Star Wars')
vader = Tag(name='Vader')

db.session.add_all([art, star_wars, vader])
db.session.commit()

# Associate posts and tags by adding to posts_tags table

post2.tags.append(art)
post3.tags.append(star_wars)
post3.tags.append(vader)
post4.tags.append(star_wars)

db.session.commit()
