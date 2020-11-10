# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

```sh
python -m virtualenv env
source env/bin/activate
```
For more information see [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
### Create database
```bash
createdb trivia_db -U postgres
```
### Run migrations
```sh
FLASK_APP=flaskr flask db upgrade
```
### Run seed
```sh
python seed.py
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test -U postgres
python test_flaskr.py
```

## API Documentation
### Introduction
    This a RESTful API to serve trivia questions and quizzes app.
### Errors
#### Unproccessable 422
- message: "Request cannot be processed"
- status code: 422
- [reference](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#422)
- Response Example
```
{
	"error": 422,
	"success": false,
	"message": "Request cannot be processed"
}
```
#### NotAllowedMethod 400
- message: "Bad request"
- status code: 400
- [reference](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#400)
- Response Example
```
{
	"error": 400,
	"success": false,
	"message": "Bad request"
}
```
#### NotFound 404
- message: "Resource not found"
- status code: 404
- [reference](https://en.wikipedia.org/wiki/HTTP_404)
- Response Example
```
{
	"error": 404,
	"success": false,
	"message": "Resource not found"
}
```
#### NotAllowedMethod 405
- message: "Method not Allowed"
- status code: 405
- [reference](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#405)
- Response Example
```
{
	"error": 405,
	"success": false,
	"message": "Method not Allowed"
}
```
#### InternalServerError 500
- message: "Internal server Error"
- status code: 500
- [reference](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#500)
- Response Example
```
{
	"error": 500,
	"success": false,
	"message": "Internal server Error"
}
```

### Endpoints

#### GET '/categories'
- Fetches all categories 
- Request Arguments: None
- Returns: 
	- success:
		- description: Success status
		- type: Boolean
	- categories:
		-  An object with keys correspond with categories ids and values correspond with categories types 
- Response Example:
```
{
	"success":true
	"categories":{"1": "Science",
		 "2": "Art",
		 "3": "Geography",
		 "4": "History",
		 "5": "Entertainment",
		 "6": "Sports"}
 }
```
- Expected Errors:
	- NotAllowedMethod 405

#### GET '/questions'
- Fetches paginated questions 
- Request Arguments: 
	- page
		- required: False
		- type: Integer
		- source: query string
- Returns: 
	- success:
		- description: Success status
		- type: Boolean
	- questions:
		- description: A paginated list of questons in page size of 10 per page
		- type: list
	- categories:
		-  description: An object with keys correspond with categories ids and values correspond with categories types 
		- type: Object
	- total_questions:
		-  description: total number of questions in the database
		- type: Integer
	- current_category:
		- description: always returns null  
		- type: null
- Response Example
```
{
  "success": true, 
  "categories": {
    "1": "Science", 
    "2": "Art"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "total_questions": 17
}
```

#### POST '/questions'
##### Option 1
- Create a new question 
- Request Arguments: 
	- question
		- required: True
		- type: String
		- source: json data object
	- answer
		- required: True
		- type: String
		- source: json data object
	- category
		- required: True
		- description: Id of the category to which the question belong.
		- type: Integer
		- source: json data object
	- difficulty
		- required: True
		- description: difficulty of the question.
		- range: [1:5]
		- type: Integer
		- source: json data object
- Returns: 
	- success:
		- description: Success status
		- type: Boolean
- Response Example
```
{
  "success": true, 
}
```
- Expected Errors:
	- NotAllowedMethod 405
	- InternalServerError 500
	- Unproccessable 422

##### Option 2
- Searches all questions
- Request Arguments: 
	- searchTerm
		- required: True
		- type: String
		- source: json data object
- Returns: 
	- success:
		- description: Success status
		- type: Boolean
	- questions:
		- description: A paginated list of questons in page size of 10 per page
		- type: list
	- categories:
		-  description: An object with keys correspond with categories ids and values correspond with categories types 
		- type: Object
	- total_questions:
		-  description: total number of questions in the database
		- type: Integer
	- current_category:
		- description: always returns null  
		- type: null
- Response Example
```
{
  "success": true, 
  "categories": {
    "1": "Science", 
    "2": "Art"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "total_questions": 17
}
```
- Expected Errors:
	- NotAllowedMethod 405
	- InternalServerError 500
	- Unproccessable 422


#### DELETE '/questions/<question_id>'
- Deletes a question with specific id 
- Request Arguments: 
	- 
		- required: True
		- type: Integer
		- source: path
- Returns: 
	- success:
		- description: Success status
		- type: Boolean
- Response Example
```
{
  "success": true, 
}
```
- Expected Errors:
	- NotAllowedMethod 405
	- NotFound 404
	- InternalServerError 500
	- Unproccessable 422

#### GET '/categories/<category_id>/questions'
- Fetches all questions that belong to specific category
- Request Arguments: 
	- category_id
		- required: True
		- type: String
		- source: path
- Returns: 
	- success:
		- description: Success status
		- type: Boolean
	- questions:
		- description: A paginated list of questons in page size of 10 per page
		- type: list
	- categories:
		-  description: A object with keys correspond with categories ids and values correspond with categories types 
		- type: Object
	- total_questions:
		-  description: total number of questions in the database
		- type: Integer
	- current_category:
		- description: the id of the current category  
		- type: Integer
- Response Example
```
{
  "success": true, 
  "categories": {
    "1": "Science", 
    "2": "Art"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "total_questions": 17
}
```
- Expected Errors:
	- NotFound 404
	- NotAllowedMethod 405
	- InternalServerError 500
	- Unproccessable 422

#### POST '/quizzes'
- Fetches a random question of a specific category or all categories.
- Request Arguments: 
	- quiz_category:
		- required: True
		- type: Object
			- type: category type or "ALL"
			- id: id of category 
		- source: json data object
	- previous_questions:
		- required: False
		- decription:
			- list of previous questions ids
		- type: list of Integers 
- Returns: 
	- success:
		- description: Success status
		- type: Boolean
	- question:
		- description: A paginated list of questons in page size of 10 per page
		- type: object
- Response Example
```
{
  "success": true, 
  "question": {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
}
```
- Expected Errors:
	- NotFound 404
	- NotAllowedMethod 405
	- InternalServerError 500
	- Unproccessable 422