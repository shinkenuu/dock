import pytest

from desafio.domain.interactors._entities import Person


@pytest.fixture()
def person():
    return Person(
        name="Fulano Cicrano",
        cpf="06021547314",
    )
