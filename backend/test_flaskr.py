import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
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

    # get_categories

    def test_get_categories(self):
        db.session.add(Category(type="Art"))
        db.session.add(Category(type="Sport"))
        db.session.commit()

        result = self.client().get("/categories")
        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['categories']), 2)
        self.assertEqual(type(body['categories']), dict)

    def test_get_empty_categories_list(self):
        result = self.client().get("/categories")

        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['categories']), 0)

    def test_categories_errored_for_bad_method(self):
        result = self.client().put("/categories")

        self.assertEqual(result.status_code, 405)

    # get_questions
    def test_get_questions(self):
        db.session.add(Category(type="Art"))
        db.session.add(Category(type="Sport"))
        db.session.add(Question(
            question="question1",
            answer="answer1",
            difficulty=1,
            category=2))
        db.session.add(Question(
            question="question2",
            answer="answer2",
            difficulty=2,
            category=1))
        db.session.commit()

        result = self.client().get("/questions")
        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['categories']), 2)
        self.assertEqual(len(body['questions']), 2)
        self.assertEqual(body['total_questions'], 2)
        self.assertEqual(body['current_category'], None)
        self.assertEqual(type(body['categories']), dict)

    def test_questions_are_paginated(self):
        db.session.add(Category(type="Art"))
        for i in range(12):
            db.session.add(Question(
                question=f"question{i}",
                answer="answer{i}",
                difficulty=1,
                category=1))
        db.session.commit()

        result = self.client().get("/questions")
        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['questions']), QUESTIONS_PER_PAGE)
        self.assertEqual(body['total_questions'], 12)

    def test_get_empty_question_list_from_first_page(self):
        result = self.client().get("/questions")

        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['questions']), 0)

    def test_get_404_from_second_page(self):
        result = self.client().get("/questions?page=2")

        self.assertEqual(result.status_code, 404)

    def test_categories_errored_for_bad_method(self):
        result = self.client().put("/questions")

        self.assertEqual(result.status_code, 405)

    # delete_questions
    def test_delete_questions(self):
        db.session.add(Category(type="Art"))
        question = Question(
            question="question1",
            answer="answer1",
            difficulty=1,
            category=1)
        db.session.add(question)
        db.session.commit()

        self.assertEqual(Question.query.count(), 1)

        result = self.client().delete(f"/questions/{question.id}")

        self.assertEqual(result.status_code, 200)
        self.assertEqual(Question.query.count(), 0)

    def test_delete_questions_returns_404_if_does_not_exist(self):

        result = self.client().delete(f"/questions/1")

        self.assertEqual(result.status_code, 404)

    # create_question
    def test_create_question_adds_new_question(self):
        self.assertEqual(Question.query.count(), 0)
        result = self.client().post("/questions", json=dict(
            question="question1",
            answer="answer1",
            difficulty=1,
            category=1
        ))

        self.assertEqual(result.status_code, 200)
        self.assertEqual(Question.query.count(), 1)

    # search questions
    def test_search_questions_with_results(self):
        db.session.add(Question(
            question="question1",
            answer="answer1",
            difficulty=1,
            category=1))
        db.session.add(Question(
            question="question2",
            answer="answer2",
            difficulty=1,
            category=1))
        db.session.commit()

        result1 = self.client().post("/questions", json=dict(
            searchTerm="quest"
        ))

        body1 = json.loads(result1.data)

        self.assertEqual(result1.status_code, 200)
        self.assertEqual(len(body1['questions']), 2)

        result2 = self.client().post("/questions", json=dict(
            searchTerm="question1"
        ))

        body2 = json.loads(result2.data)

        self.assertEqual(result2.status_code, 200)
        self.assertEqual(len(body2['questions']), 1)

    def test_search_questions_without_results(self):
        result = self.client().post("/questions", json=dict(
            searchTerm="quest"
        ))

        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['questions']), 0)

    # get_category_questions
    def test_get_questions_by_category(self):
        category = Category(type="Art")
        db.session.add(category)
        db.session.add(Question(
            question="question1",
            answer="answer1",
            difficulty=1,
            category=1))
        db.session.commit()

        result = self.client().get(f"/categories/{category.id}/questions")

        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['questions']), 1)
        self.assertEqual(body['current_category'], "Art")

    def test_get_questions_by_category_without_question(self):
        category = Category(type="Art")
        db.session.add(category)
        db.session.commit()

        result = self.client().get(f"/categories/{category.id}/questions")

        body = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(body['questions']), 0)
        self.assertEqual(body['current_category'], "Art")

    def test_get_questions_by_category_not_found(self):
        result = self.client().get(f"/categories/{1}/questions")

        self.assertEqual(result.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
