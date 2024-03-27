import json

from lesson_45.models import create_database_session, Choice, Question

session = create_database_session()


def populate_database(path: str = 'data.json'):
    session.query(Question).delete()
    session.query(Choice).delete()

    with open('questions.json', 'r') as file:
        data = json.load(file)

        for question_text, choice_data in data.items():
            question = Question(text=question_text)
            for choice_text, votes in choice_data.items():
                choice = Choice(text=choice_text, votes=votes)
                question.choices.append(choice)
            session.add(question)
        session.commit()


def print_all_question_with_choices() -> None:
    questions = session.query(Question).all()
    for question in questions:
        choices = ', '.join(f"{choice.text}({choice.votes})" for choice in question.choices)
        print(f"{question.text}: {choices}")


if __name__ == "__main__":
    populate_database()
    print_all_question_with_choices()
