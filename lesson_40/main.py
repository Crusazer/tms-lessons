from typing import Union
from fastapi import FastAPI, HTTPException
from polls_models import Question, PaginatedQuestions, Database, QuestionVote

app = FastAPI()
db = Database()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/questions/")
async def get_questions(ordering: str = "-pub_date", page_size: int = 5,
                        page: int = 1) -> PaginatedQuestions:
    data = db.get_questions()[(page - 1) * page_size:page * page_size]
    return PaginatedQuestions(count=len(data), results=data)


@app.get("/questions/{question_id}/", responses={404: {}})
async def get_question(question_id: int) -> Question:
    question = db.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail=f"Question {question_id} not found")
    return question


@app.post("/questions/{question_id}/vote/")
async def vote_question(question_id: int, question_vote: QuestionVote) -> Question:
    question = db.get_question(question_id)

    if question is None:
        raise HTTPException(status_code=404, detail=f"Question {question_id} not found")

    for choice in question.choices:
        if choice.id == question_vote.choice_id:
            choice.votes += 1
            return question

    raise HTTPException(status_code=404,
                        detail=f"Question {question_id} doesn't have choice with id {question_vote.choice_id}")
