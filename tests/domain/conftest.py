from datetime import datetime
from decimal import Decimal

import pytest

from desafio.domain.interactors._entities import Account, Person


@pytest.fixture()
def person():
    return Person(
        id=1,
        name="Fulano Cicrano",
        cpf="06021547314",
    )


@pytest.fixture()
def account(person):
    return Account(
        id=1,
        balance=Decimal("123.45"),
        created_at=datetime.utcnow(),
        person_id=person.id,
    )
