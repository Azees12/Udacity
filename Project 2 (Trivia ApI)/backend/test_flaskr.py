import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from constant import QUESTIONS_PER_PAGE, MESSAGE_NOT_FOUND, MESSAGE_UNPROCESSABLE


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.test_question = {
            "question": "Whats is 4 + 4 ?",
            "answer": "8",
            "difficulty": 1,
            "category": 4,
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    """ 
    GET /cateegories
    """
    "Test get Categories"

    def test_Catergories(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))
        self.assertTrue(data["total_categories"])

    """
    GET /questions/<int:category_id>/questions

    """

    "Test get questions per category"

    def test_questionsCategory(self):
        category_id = 1
        response = self.client().get("/categories/{}/questions".format(category_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], category_id)

    "Test get questions per category no results"

    def test_questionsCategory2(self):
        category_id = 555
        response = self.client().get("/categories/{}/questions".format(category_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_NOT_FOUND)

    "Test page not exist beyond valid page"

    def test_questionsCategory3(self):
        category_id = 1
        response = self.client().get(
            "/categories/{}/questions?page=10000".format(category_id)
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_NOT_FOUND)

    "Test questions in category page 0"

    def test_questionsCategory4(self):
        category_id = 1
        response = self.client().get(
            "/categories/{}/questions?page=0".format(category_id)
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    "Test questions in search question below page 0"

    def test_questionsCategory5(self):
        category_id = 1
        response = self.client().get(
            "/categories/{}/questions?page=-1".format(category_id)
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    """
    GET /questions
    """

    "Test get questions "

    def test_questions(self):
        response = self.client().get("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), QUESTIONS_PER_PAGE)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertIsNone(data["current_category"])

    "Test get question page not exist beyond valid page"

    def test_questions2(self):
        response = self.client().get("/questions?page=10000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_NOT_FOUND)

    "Test get question page = 0"

    def test_questions3(self):
        response = self.client().get("/questions?page=0")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    "Test get question page below zero"

    def test_questions4(self):
        response = self.client().get("/questions?page=-1")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    """
    POST /questions
    """

    "Test post create question "

    def test_createQuestion(self):
        response = self.client().post("/questions", json=self.new_question.copy())
        data = json.loads(response.data)

        new_question = Question.query.order_by(Question.id.desc()).first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertEqual(data["created"]["id"], new_question.id)
        self.assertEqual(data["created"]["question"], new_question.question)
        self.assertEqual(data["created"]["answer"], new_question.answer)
        self.assertEqual(data["created"]["difficulty"], new_question.difficulty)
        self.assertEqual(data["created"]["category"], new_question.category)

    "Test create question, question is missing"

    def test_createQuestion2(self):
        request = self.new_question.copy()
        del request["question"]

        response = self.client().post("/questions", json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    "Test create question, question is missing"

    def test_createQuestion3(self):
        request = self.new_question.copy()
        request["question"] = ""

        response = self.client().post("/questions", json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    "Test create question, answer is missing"

    def test_createQuestion4(self):
        request = self.new_question.copy()
        del request["answer"]

        response = self.client().post("/questions", json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    "Test create question, answer is empty"

    def test_createQuestion5(self):
        request = self.new_question.copy()
        request["answer"] = ""

        response = self.client().post("/questions", json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    "Test create question, difficulty is missing"

    def test_createQuestion6(self):
        request = self.new_question.copy()
        del request["difficulty"]

        response = self.client().post("/questions", json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    "Test create question, Catorgory is missing"

    def test_createQuestion7(self):
        request = self.new_question.copy()
        del request["category"]

        response = self.client().post("/questions", json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    """
    Search Function
    """

    "Test Search"

    def test_searchQuestions(self):
        response = self.client().post("/questions", json={"search_term": "title"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertIsNone(data["current_category"])

    "Test Search No reults"

    def test_searchQuestions2(self):
        response = self.client().post(
            "/questions", json={"search_term": "zzzzzzzzzzzzzzzz"}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 0)
        self.assertEqual(data["total_questions"], 0)
        self.assertIsNone(data["current_category"])

    "Test Search questions error page not exist beyond validpage "

    def test_searchQuestions3(self):
        response = self.client().post(
            "/questions?page=2000", json={"search_term": "title"}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_NOT_FOUND)

    "Test Search page = 0"

    def test_searchQuestions4(self):
        response = self.client().post(
            "/questions?page=0", json={"search_term": "title"}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    "Test Search page below zero"

    def test_searchQuestions4(self):
        response = self.client().post(
            "/questions?page=-1", json={"search_term": "title"}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)

    """
    DELETE /questions/<int:question_id>
    """

    "Test Delete question"

    def test_deleteQuestion(self):
        question = Question.query.order_by(Question.id.desc()).first()
        question_id = question.id

        response = self.client().delete("/questions/{}".format(question_id))
        data = json.loads(response.data)

        question = Question.query.get(question_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], question_id)
        self.assertIsNone(question)

    "Test Delete question, question does not exist"

    def test_deleteQuestion2(self):
        question_id = 99
        response = self.client().delete("/questions/{}".format(question_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_NOT_FOUND)

    """
    POST /quizzes
    """

    "Test Quiz guesses"

    def test_quiz(self):
        category = Category.query.first()
        response = self.client().post(
            "/quizzes", json={"quiz_category": category.format()}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    "Test Quiz guesses, wwith previous questions"

    def test_quiz2(self):
        category = Category.query.first()
        questions_in_category = Question.query.filter(
            Question.category == category.id
        ).all()

        expected_question = questions_in_category[0]
        previous_questions = [question.id for question in questions_in_category[1:]]

        response = self.client().post(
            "/quizzes",
            json={
                "quiz_category": category.format(),
                "previous_questions": previous_questions,
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertEqual(data["question"]["id"], expected_question.id)

    "Test Quiz guess, no more questions"

    def test_quiz3(self):
        category = Category.query.first()
        questions_in_category = Question.query.filter(
            Question.category == category.id
        ).all()

        previous_questions = [question.id for question in questions_in_category]

        response = self.client().post(
            "/quizzes",
            json={
                "quiz_category": category.format(),
                "previous_questions": previous_questions,
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNone(data["question"])

    "Test quiz guess, no category was specified"

    def test_quiz4(self):
        response = self.client().post("/quizzes")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], MESSAGE_UNPROCESSABLE)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
