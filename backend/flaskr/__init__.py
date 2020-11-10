import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             "Content-Type, Authorization")
        response.headers.add('Access-Control-Allow-Methods',
                             "GET,POST,PUT,OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials',
                             "true")
        return response

    def get_dict_from_categories(categories):
        # https://stackoverflow.com/a/1993848
        return dict(((c.id, c.type) for c in categories))

    @app.route('/categories')
    def categories():
        categories = Category.query.all()

        return jsonify({
            "success": True,
            "categories": get_dict_from_categories(categories)
        })

    @app.route("/questions")
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start_question = (page - 1) * QUESTIONS_PER_PAGE
        end_question = start_question + QUESTIONS_PER_PAGE

        # https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.slice
        questions = db.session.query(Question).order_by(Question.id).slice(
            start_question, end_question).all()

        categories = Category.query.all()

        if page != 1 and not len(questions):
            abort(404)
        total_questions = Question.query.count()
        formatted_questions = [q.format() for q in questions]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": total_questions,
            "categories": get_dict_from_categories(categories),
            "current_category": None
        })

    @app.route('/questions/<int:id>', methods=["DELETE"])
    def delete_question(id):
        error = False
        question = Question.query.get_or_404(id)
        try:
            question.delete()
        except:
            db.session.rollback()
            print(sys.exc_info())
            error = True
        finally:
            db.session.close()
        if not error:
            return jsonify({
                "success": True
            })

        abort(422)

    @app.route('/questions', methods=["POST"])
    def create_question():
        error = False
        data = request.get_json()

        search = data.get('searchTerm', None)

        if search:
            questions = Question.query.filter(
                Question.question.ilike(f"%{search}%")) \
                .all()

            formatted_questions = [q.format() for q in questions]

            return jsonify({
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(questions),
                "current_category": None
            })

        question = Question(
            question=data.get('question', None),
            answer=data.get('answer', None),
            category=data.get('category', None),
            difficulty=data.get('difficulty', None),
        )

        try:
            question.insert()
        except:
            db.session.rollback()
            print(sys.exc_info())
            error = True
        finally:
            db.session.close()
        if not error:
            return jsonify({
                "success": True
            })

        abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        print(404)
        return jsonify({
            "error": 404,
            "success": False,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "error": 422,
            "success": False,
            "message": "Request cannot be processed"
        }), 422

    return app
