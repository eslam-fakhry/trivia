import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_username = "postgres"
        self.database_path = "postgresql://{}@{}/{}".format(
            self.database_username,
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        # Clean up test database
        db.session.remove()
        db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        db.session.add(Category(type="Art"))
        db.session.add(Category(type="Sport"))
        db.session.commit()

        result = self.client().get("/categories")
        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['categories']), 2)

    def test_get_empty_categories_list(self):
        result = self.client().get("/categories")

        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['categories']), 0)

    def test_categories_errored_for_bad_method(self):
        result = self.client().put("/categories")

        self.assertEqual(result.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
