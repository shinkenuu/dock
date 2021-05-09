from datetime import datetime

from desafio.domain.interactors.accounts import PersonInteractor
from desafio.logger import get_logger

LOGGER = get_logger()


def load_people():
    # this could read a large file or yield results from a query
    people = [
        {
            "name": "Jão das Névi",
            "cpf": "060.215.473-14",
            "birth_date": None,
        },
        {
            "name": "Zé da Quitanda",
            "cpf": "62660388202",
            "birth_date": datetime(1994, 2, 23),
        },
    ]

    for person in people:
        yield person


def create_people():
    for person in load_people():
        try:
            created_person = PersonInteractor.create(**person)
            LOGGER.debug(created_person)

        except Exception as error:
            LOGGER.error(error)


if __name__ == "__main__":
    create_people()
