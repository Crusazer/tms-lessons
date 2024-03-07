from typing import Type, TypeVar, Any

from models_scheme import ChoiceScheme, QuestionScheme, PaginateScheme
from models import Choice, Question

T = TypeVar('T')


def serialize_choice(choice: Choice) -> ChoiceScheme:
    """ Serialize db choice to pydentic Choice """
    return ChoiceScheme(id=choice.id, text=choice.text, votes=choice.votes, question_id=choice.question_id)


def serialize_question(question: Question | Type[Question]) -> QuestionScheme:
    """ Serialize db question to pydentic Question """
    return QuestionScheme(id=question.id, text=question.text,
                          choices=[serialize_choice(choice) for choice in question.choices])


def paginate(model: T, list_scheme: list[Any], page_size: int, page: int) -> T:
    count = len(list_scheme)
    count_page: int = count // page_size
    if count % page_size > 0:
        count_page += 1

    previous_page: int = page - 1 if page - 1 > 0 else None
    next_page: int = page + 1 if page + 1 <= count_page else None
    return model(count=count, previous=previous_page, next=next_page, results=list_scheme)
