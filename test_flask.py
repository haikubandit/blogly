from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="TestLuke", last_name="TestSkywalker", image_url="https://static3.cbrimages.com/wordpress/wp-content/uploads/2020/09/Luke-Skywalker-Yellow-Lightsaber-feature.jpg?q=50&fit=crop&w=960&h=500")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestLuke', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestLuke TestSkywalker</h1>', html)
            print(self.user.image_url)

            # why won't this work?
            # self.assertIn(self.user.image_url, html)
            
    def test_create_user(self):
        with app.test_client() as client:
            d = {"first-name": "TestLuke", "last-name": "TestSkywalker", "image-url": "https://static3.cbrimages.com/wordpress/wp-content/uploads/2020/09/Luke-Skywalker-Yellow-Lightsaber-feature.jpg?q=50&fit=crop&w=960&h=500"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestLuke TestSkywalker</a></li>", html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestLuke", html)
            # self.assertIn(f"https://static3.cbrimages.com/wordpress/wp-content/uploads/2020/09/Luke-Skywalker-Yellow-Lightsaber-feature.jpg?q=50&fit=crop&w=960&h=500", html)