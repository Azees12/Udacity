import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


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
    def test_get_Categories(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_Categories_BadRequest(self):
        response = self.client().put("/categories")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["success"], False)

    def test_add_Questions(self):
        Question = {
            "question": "Cool question kid?",
            "answer": "Cool",
            "difficulty": 2,
            "category": 3,
        }
        response = self.client().post("/questions", json=Question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_Question(self):
        response = self.client().delete("/questions/2")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_Question_NotFound(self):
        response = self.client().delete("/questions/200")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], True)

    def test_questions_Category(self):
        response = self.client().get("/categories/2/questions")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_questions_Category_NotFound(self):
        response = self.client().get("/categories/55/questions")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_search(self):
        response = self.client().post("/search", json={"search_term": "What is"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(len(data["questions"]), 10)

    def test_search_NotFound(self):
        response = self.client().post("/search", json={"search_term": "1123234"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(len(data["questions"]), 0)

    def test_quiz_category_Previous_Valid(self):
        quiz = {"previous_questions": [], "quiz_category": {"type": "All", "id": "0"}}
        response = self.client().post("/quizzes", json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"])

    def test_quiz_category_Previous_Valid(self):
        quiz = {"previous_questions": [13], "quiz_category": {"type": "3", "id": "14"}}
        response = self.client().post("/quizzes", json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"]["category"], "3")

    def test_quiz_category_invalid(self):
        quiz = {"previous_questions": [1], "quiz_category": {"type": "bb", "id": "b"}}
        response = self.client().post("/quizzes", json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_quiz_Previous_questions_none(self):
        quiz = {"previous_questions": [], "quiz_category": {"type": "3", "id": "14"}}
        response = self.client().post("/quizzes", json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"]["category"], "3")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
