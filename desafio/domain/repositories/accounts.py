from typing import Any

from sqlalchemy.exc import IntegrityError

from desafio.domain.exceptions.accounts import PersonNotFound, DuplicatedPerson
from desafio.domain.interactors._entities import (
    Account as AccountEntity,
    Person as PersonEntity,
)
from desafio.domain.repositories._models import ModelRepository, Session
from desafio.domain.repositories._models.accounts import (
    Account as AccountModel,
    Person as PersonModel,
)


class AccountRepository(ModelRepository):
    model = AccountModel
    entity = AccountEntity

    @classmethod
    def create(cls, entity: Any, session: Session = None) -> Any:
        try:
            return super().create(entity=entity, session=session)
        except IntegrityError as error:
            if "accounts_person_id_fkey" in error.args[0]:
                raise PersonNotFound(id=entity.person_id)

            raise error


class PersonRepository(ModelRepository):
    model = PersonModel
    entity = PersonEntity

    @classmethod
    def create(cls, entity: Any, session: Session = None) -> Any:
        try:
            return super().create(entity=entity, session=session)
        except IntegrityError:
            raise DuplicatedPerson(cpf=entity.cpf)
