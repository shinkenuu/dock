from datetime import datetime

import pytest

from desafio.domain.interactors.accounts import PersonInteractor
from desafio.domain.interactors._entities import Person


@pytest.mark.parametrize(
    "create_kwargs, repository_return",
    [
        (
            {
                "name": "Jão das Névi",
                "cpf": "060.215.473-14",
                "birth_date": None,
            },
            Person(id=1, name="Jão das Névi", cpf="06021547314"),
        ),
        (
            {
                "name": "Zé da Quitanda",
                "cpf": "62660388202",
                "birth_date": datetime(1994, 2, 23),
            },
            Person(
                id=1,
                name="Zé da Quitanda",
                cpf="62660388202",
                birth_date=datetime(1994, 2, 23),
            ),
        ),
    ],
)
def test_return(mocker, create_kwargs, repository_return):
    # ARRANGE
    PersonInteractor.repository = mocker.Mock()
    PersonInteractor.repository.create.return_value = repository_return

    expected_return = repository_return.dict()

    # ACT
    actual_return = PersonInteractor.create(**create_kwargs)

    # ASSERT
    assert actual_return == expected_return


def test_calls_repository_create_with_entity(mocker, person):
    # ARRANGE
    PersonInteractor.repository = mocker.Mock()
    PersonInteractor.repository.create.return_value = person

    # ACT
    PersonInteractor.create(
        name=person.name,
        cpf=person.cpf,
        birth_date=person.birth_date,
    )

    # ASSERT
    PersonInteractor.repository.create.assert_called_once_with(person)


@pytest.mark.parametrize(
    "invalid_cpf",
    [
        "123.345.567-42",
        "",
        None,
    ],
)
def test_raises_value_error_at_invalid_cpf(invalid_cpf):
    # ACT / ASSERT
    with pytest.raises(ValueError):
        PersonInteractor.create(
            name="Sauron",
            cpf=invalid_cpf,
        )
