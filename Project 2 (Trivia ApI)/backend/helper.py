from flask import request, abort
from constant import QUESTIONS_PER_PAGE


def get_pagination(request, selection):
    page = request.args.get("page", 1, type=int)
    if page < 1:
        return abort(422)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted = [question.format() for question in selection]

    return formatted[start:end]
