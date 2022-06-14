from email.quoprimime import body_check
import os
from re import A
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from numpy import delete
from sqlalchemy import true
from constant import *
import random

from models import setup_db, Question, Category


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  """
    cors = CORS(app, resources={r"/*": {"origin": "*"}})

    """
  @TODO: Use the after_request decorator to set Access-Control-Allow
  """

    @app.after_request
    def after_resques(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add(
            "Access-Controll-Allow-Methods", "GET, PATCH, POST ,DELETE, OPTIONS"
        )
        return response

    """

  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  """

    @app.routes("/categories", methods=["GET"])
    def get_Categories():
        try:
            ##Categories retrived and ordered by id
            categories = Category.query.order_by(Category.id).all()
            ##Formatting the retrieved categories
            cat_Formated = [category.format() for category in categories]

            ## Returneed in desired format
            return jsonify(
                {
                    "categories": cat_Formated,
                    "total_categories": len(cat_Formated),
                    "success": True,
                }
            )

        except Exception:
            abort(422)

    """
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  """

    @app.route("/questions", method=["GET"])
    def get_Qeustions():
        try:

            # Pagination
            page = request.args.get("page", 1, type=int)

            # Retrieving all the questions paginated by 10 and categories ordered by id:
            questions = Question.query.order_by(Question.id).paginate(
                page=page, per_page=QUESTIONS_PER_PAGE
            )
            categories = Category.query.order_by(Category.id).all()

            ##Formating questions and categories retrived
            cat_Formatted = [category.format() for category in categories]
            ques_Formatted = [questions.format() for question in questions.items]

            # Checking if questions were found
            if len(ques_Formatted) < 1:
                abort(404)

            else:
                return jsonify(
                    {
                        "questions": ques_Formatted,
                        "categories": cat_Formatted,
                        "current_category": None,
                        "total_questions": questions.total,
                        "success": True,
                    }
                )

        except Exception as e:
            if "404" in str(e):
                abort(404)
            else:
                abort(422)

    """
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  """

    @app.route("/questions/<int:questions_id>", method=["DELETE"])
    def delete_Question(question_id):
        try:
            ##Finding the desired question to be deleted
            question = Question.query.filter(Question.id == question_id).one_or_none()

            ##Checking if questions were found
            if question == None:
                abort(404)
            else:
                ##Removing the desired question
                question.delete()

                return jsonify({"deleted": question_id, "success": True})

        except Exception as e:
            if "404" in str(e):
                abort(404)
            else:
                abort(422)

    """
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  """

    @app.route("/questions", method=["POST"])
    def create_Question():

        ##Retriving question values to be inserted from request body
        body = request.get_json()
        question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)

        try:

            ##Inserting new question into databae
            question = Question(
                question=body["question"],
                answer=body["answer"],
                difficulty=body["difficulty"],
                category=body["category"],
            )
            question.insert()

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                }
            )
        except Exception:
            abort(422)

    """
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  """

    @app.route("/search", method=["POST"])
    def search():

        ##Retrieveing search term from request body
        body = request.get_json()
        search_Term = body.get("searchTerm", None)

        try:
            ##Retriving questions filtered by search term and formatting
            questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search))
            )
            ques_Formatted = [questions.format() for question in questions]

            return jsonify(
                {
                    "questions": ques_Formatted,
                    "total_questions": len(ques_Formatted),
                    "current_category": None,
                    "success": True,
                }
            )
        except Exception as e:
            if "404" in str(e):
                abort(404)
            else:
                abort(422)

    """
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  """

    @app.route("/categories/<int:category_id>/questions", method=["GET"])
    def questions_Category(category_id):
        try:
            ##Pagination
            page = request.args.get("page", 1, type=int)

            ##Retrived Questions filtered by category and formatting
            questions = (
                Question.query.order_by(Question.id)
                .filter(Question.category == category_id)
                .paginate(page=page, per_page=QUESTIONS_PER_PAGE)
            )
            ques_Formatted = [questions.format() for question in questions.items]

            # Checking if atleast 1 question was retreived
            if len(ques_Formatted) < 1:
                abort(404)

            else:
                return jsonify(
                    {
                        "questions": ques_Formatted,
                        "total_questions": questions.total,
                        "current_category": category_id,
                        "success": True,
                    }
                )

        except Exception as e:
            if "404" in str(e):
                abort(404)
            else:
                abort(422)

    """
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  """

    @app.route("/quizzes", method=["POST"])
    def get_Quizzes():
        try:

            ##Retrive required variables from request body
            questions = None
            body = request.get_json()
            quiz_Category = body.get("quiz_category", None)
            prev_Questions = body.get("previous_questions", None)
            category = quiz_Category.get("id")

            if category == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == category).all()

            randomized = random.randint(0, len(questions) - 1)
            random_Question = questions[randomized]

            while random_Question.id not in prev_Questions:
                random_Question = questions[randomized]
                return jsonify(
                    {
                        "question": random_Question.format(),
                        "previous_questions": prev_Questions,
                        "success": True,
                    }
                )

        except Exception as e:
            if "404" in str(e):
                abort(404)
            else:
                abort(422)

    """
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  """

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": BAD_REQUEST}),
            400,
        )

    @app.errorhandler(404)
    def notFound(error):
        return (
            jsonify({"success": False, "error": 404, "message": MESSAGE_NOT_FOUND}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"sucess": False, "error": 422, "message": MESSAGE_UNPROCESSABLE}),
            422,
        )

    @app.errorhandler(500)
    def servererror(error):
        return (
            jsonify({"success": False, "error": 500, "message": MESSAGE_SERVER_ERROR}),
            500,
        )

    return app
