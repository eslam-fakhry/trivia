import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import not_, func
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

TRIVIA_FRONTEND_ORIGIN = os.environ.get(
    "FRONTEND_ORIGIN", "http://localhost:3000")

# helpers
def get_dict_from_categories(categories):
    # https://stackoverflow.com/a/1993848
    return dict(((c.id, c.type) for c in categories))


def create_custom_bad_request(field):
    return jsonify({
        "error": 400,
        "success": False,
        "message": f"Field: {field} is invalid"
    }), 400


# APP
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)

    cors = CORS(app, resources={
        "/*": {"origins": TRIVIA_FRONTEND_ORIGIN}
    })

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             "Content-Type, Authorization")
        response.headers.add('Access-Control-Allow-Methods',
                             "GET,POST,PUT,OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials',
                             "true")
        return response

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

        question_input = data.get('question', None)
        answer_input = data.get('answer', None)
        category_input = data.get('category', None)
        difficulty_input = data.get('difficulty', None)

        # Validations
        if not question_input:
            return create_custom_bad_request("question")

        if not answer_input:
            return create_custom_bad_request("answer")

        if not Category.query.get(category_input):
            return create_custom_bad_request("category")

        if (not difficulty_input) or (difficulty_input < 1) or (difficulty_input > 5):
            return create_custom_bad_request("difficulty")

        question = Question(
            question=question_input,
            answer=answer_input,
            category=category_input,
            difficulty=difficulty_input,
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

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        category = Category.query.get_or_404(category_id)
        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [q.format() for q in questions]
        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "current_category": category.id,
            "total_questions": len(formatted_questions)
        })

    @app.route('/quizzes', methods=["POST"])
    def quizzes():
        category = None

        data = request.get_json()

        quiz_category = data.get("quiz_category", None)
        previous_questions = data.get("previous_questions", [])
        if not quiz_category:
            abort(400)

        if quiz_category['type'] != "ALL":
            category = Category.query.get_or_404(quiz_category['id'])

        query = Question.query
        if category:
            query = query.filter(Question.category == category.id)

        # from https://stackoverflow.com/a/60815
        query = query.filter(not_(Question.id.in_(previous_questions))) \
            .order_by(func.random()).limit(1)

        question = query.first()

        if question:
            question = question.format()

        return jsonify({
            "success": True,
            "question":  question
        })

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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": 400,
            "success": False,
            "message": "Bad request"
        }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "error": 500,
            "success": False,
            "message": "Internal server Error"
        }), 500

    @app.errorhandler(405)
    def not_allowed_method(error):
        return jsonify({
            "error": 405,
            "success": False,
            "message": "Method not allowed"
        }), 405
    return app
