from datetime import timedelta, datetime
import sys
from models import db, setup_db, Question, Category
from flaskr import create_app

import json
import random

app = create_app()


def main():
    with open('seed_data.json') as json_file:
        data = json.load(json_file)
        print("Seeding...")
        try:
            for category in data['categories']:
                category_obj = Category(
                    type=category['type']
                )
                db.session.add(category_obj)
            db.session.commit()

            for question in data['questions']:
                question_obj = Question(question=question['question'],
                                  answer=question["answer"],
                                  difficulty=question["difficulty"],
                                  category=question['category'],
                                  )
                db.session.add(question_obj)
            db.session.commit()
            print("Done seeding.")
        except:
            db.session.rollback()
            print(sys.exc_info())
            print("Error seeding.")
        finally:
            db.session.close()


if __name__ == "__main__":
    main()
