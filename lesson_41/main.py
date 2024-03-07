from typing import Type

from models import create_database_session, Question, Choice
from fastapi import FastAPI, HTTPException
from models_scheme import PaginatedQuestions, PaginatedChoices, QuestionScheme, ChoiceScheme, QuestionVoteScheme
from serializers import serialize_question, paginate

app = FastAPI()
session = create_database_session()

question_queryset = session.query(Question)
choice_queryset = session.query(Choice)


@app.get("/questions/")
async def get_questions(ordering: str = "-pub_date", page_size: int = 5,
                        page: int = 1) -> PaginatedQuestions | Type[PaginatedQuestions]:
    ordering_map = {
        'id': Question.id,
        '-id': Question.id.desc()
    }

    questions_db = question_queryset.order_by(ordering_map.get(ordering, Question.id)).offset(
        (page - 1) * page_size).limit(page_size)
    questions_scheme = [serialize_question(question) for question in questions_db.all()]

    return paginate(PaginatedQuestions, questions_scheme, page_size, page)


@app.get("/questions/{question_id}/", responses={404: {"description": "Question not found"}})
async def get_question(question_id: int) -> QuestionScheme:
    question_db = question_queryset.filter(Question.id == question_id).first()
    if not question_db:
        raise HTTPException(status_code=404, detail=f"Question {question_id} not found")
    return serialize_question(question_db)


@app.post("/questions/{question_id}/vote/")
async def vote_question(question_id: int, question_vote: QuestionVoteScheme) -> QuestionScheme:
    question_db = question_queryset.filter(Question.id == question_id).first()

    if question_db is None:
        raise HTTPException(status_code=404, detail=f"Question {question_id} not found")

    for choice in question_db.choices:
        if choice.id == question_vote.choice_id:
            choice.votes += 1
            session.commit()
            return serialize_question(question_db)

    raise HTTPException(status_code=404,
                        detail=f"Question {question_id} doesn't have choice with id {question_vote.choice_id}")
