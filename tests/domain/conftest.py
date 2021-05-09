from datetime import datetime
from decimal import Decimal

import pytest

from desafio.domain.interactors._entities import Account, Person, Transaction


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
        id=2,
        balance=Decimal("123.45"),
        created_at=datetime.utcnow(),
        person_id=person.id,
    )


@pytest.fixture()
def transaction(account):
    return Transaction(
        id=3,
        value=Decimal("23.45"),
        account_id=account.id,
        processed_at=datetime.utcnow(),
    )
