from pydantic import BaseModel


class ChoiceScheme(BaseModel):
    id: int | None = None
    text: str
    votes: int
    question_id: int | None = None


class QuestionScheme(BaseModel):
    id: int | None = None
    text: str
    choices: list[ChoiceScheme] | None = None


class PaginateScheme(BaseModel):
    count: int = 0
    previous: int | None = None
    next: int | None = None


class PaginatedQuestions(PaginateScheme):
    results: list[QuestionScheme]


class PaginatedChoices(PaginateScheme):
    results: list[ChoiceScheme]


class QuestionVoteScheme(BaseModel):
    choice_id: int

