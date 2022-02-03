from ast import Try
from http.client import BAD_REQUEST
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
from helper import get_pagination
from constant import MESSAGE_NOT_FOUND, MESSAGE_UNPROCESSABLE, MESSAGE_SERVER_ERROR,BAD_REQUEST


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  """

    cors = CORS(app, resources={r"/*": {"origin": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Controll-Allow-Methods", "GET, PATCH, POST ,DELETE, OPTIONS")
        return response

    @app.route("/categories", methods=["GET"])
    def getCategories():
        try:
            categories = Category.query.all()
            formatCat = [category.format() for category in categories]
            return jsonify(
            {
                "success": True,
                "categories": formatCat,
                "total_categories": len(formatCat),
            })
        except Exception:
            abort(422)
             

    @app.route("/questions", method=["GET"])
    def getQuestions():

        try:
            questions = Question.quety.all()
            paginatedQuestions = get_pagination(request, questions)
            categories = Category.query.all()

            if len(paginatedQuestions) < 1:
                return abort(404)

            return jsonify(
            {
                "success": True,
                "questions": paginatedQuestions,
                "total_questions": len(questions),
                "categories": [category.format() for category in categories],
                "current_category": None,
            }
            )
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route("questions/<int:questions_id>", methods=["DELETE"])
    def deleteQuestion(question_id):
        
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question == None:
                return abort(404)
            question.delete()
            return jsonify({"success": True, "deleted": question_id})
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route("/questions", method=["POST"])
    def createQuestion():
     
        body = request.get_json()
        if "search_term" in body.keys():
            return searchQuestions(request, body["search_term"])

        for key in ["question", "answer", "difficulty", "category"]:
            if key not in body.keys() or body[key] == None or body[key] == "":
                return abort(422)
        try:
            question = Question(
            question=body["question"],
            answer=body["answer"],
            difficulty=body["difficulty"],
            category=body["category"],
            )
            question.insert()

            return jsonify({"success": True, "created": question.format()})
        except Exception:
            abort(422)


    def searchQuestions(request, search_term):
        try:
            questions = Question.query.filter(
            Question.question.ilike("%" + search_term + "%")
            ).all()
            paginatedQuestions = get_pagination(request, questions)

            if len(questions) > 0 and len(paginatedQuestions) < 1:
                return abort(404)

            return jsonify(
            {
                "success": True,
                "questions": paginatedQuestions,
                "total_questions": len(questions),
                "current_category": None,
            }
            )
        except Exception:
            abort(422)

    @app.route("/categories/<int:category_id>/questions", method=["GET"])
    def questionsCategory(category_id):

        try:
            questions = Question.query.filter(Question.category == category_id).all()
            paginatedQuestions = get_pagination(request, questions)

            if len(paginatedQuestions) < 1:
                return abort(404)

            return jsonify(
                {
                "success": True,
                "questions": paginatedQuestions,
                "total_questions": len(questions),
                "current_category": category_id,
                }
            )
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route("/quizzes", methods=["POST"])
    def questionGuess():

        try:
            body = request.get_json()
            if body == None or "quiz_category" not in body.keys():
                return abort(422)

            prevQuestions = []
            if "previous_questions" in body.keys():
                prevQuestions = body["previous_questions"]
                question = Question.query.filter(
                Question.category == body["quiz_category"]["id"],
                Question.id.notin_(prevQuestions),
                ).first()

            return jsonify(
                {
                "success": True,
                "question": question.format() if question != None else None,
                }
            )
        except Exception:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return (
               jsonify({"success": False,"error": 400,"message": BAD_REQUEST}), 
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
            500
        )
    

    return app
