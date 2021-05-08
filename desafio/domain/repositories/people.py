from typing import Any

from desafio.domain.exceptions.accounts import DuplicatedPerson
from desafio.domain.interactors._entities import Person as PersonEntity
from desafio.domain.repositories._models import ModelRepository, Session
from desafio.domain.repositories._models.accounts import Person as PersonModel
from desafio.domain.repositories._models.exceptions import DuplicatedModel


class PersonRepository(ModelRepository):
    model = PersonModel
    entity = PersonEntity

    @classmethod
    def create(cls, entity: Any, session: Session = None) -> Any:
        try:
            return super().create(entity=entity, session=session)
        except DuplicatedModel:
            raise DuplicatedPerson(cpf=entity.cpf)
