from abc import ABCMeta
from typing import Any, List, Optional

from desafio.clients.orm import LocalSession, Session
from desafio.domain.repositories import IEntityRepository
from desafio.domain.repositories._models._base import Base
from desafio.domain.repositories._models.exceptions import ModelNotFound


class ModelRepository(ABCMeta, IEntityRepository):
    model: Base

    @classmethod
    def get_one(cls, session: Session = None, *args, **kwargs) -> Optional[Any]:
        with LocalSession(session) as session:
            model = session.query(cls.model).filter_by(**kwargs).first()

            if not model:
                return None

            entity = cls.entity.from_orm(model)
        return entity

    @classmethod
    def get_many(cls, session: Session = None, *args, **kwargs) -> List[Any]:
        with LocalSession(session) as session:
            query = session.query(cls.model)
            for key, value in kwargs.items():
                model_attribute = getattr(cls.model, key)
                if isinstance(value, (list, tuple, set)):
                    query = query.filter(model_attribute.in_(value))
                else:
                    query = query.filter(model_attribute == value)

            models = query.all()
            if not models:
                return []
            entities = [cls.entity.from_orm(model) for model in models]

        return entities

    @classmethod
    def create(cls, entity: Any, session: Session = None) -> Any:
        with LocalSession(session) as session:
            model = cls.model(**entity.dict())
            session.add(model)
            session.commit()
            return cls.entity.from_orm(model)

    @classmethod
    def update(cls, entity: Any, session: Session = None) -> Any:
        with LocalSession(session) as session:
            model = cls.get_entity_model(entity=entity, session=session)

            if not model:
                raise ModelNotFound

            entity_dict = entity.dict(exclude_unset=True)
            for field, value in entity_dict.items():
                setattr(model, field, value)

            session.add(model)
            session.commit()

            return cls.entity.from_orm(model)

    @classmethod
    def get_entity_model(cls, entity: Any, session: Session = None) -> Optional[Base]:
        with LocalSession(session) as session:

            entity_id = getattr(entity, "id")
            if entity_id:
                return session.query(cls.model).filter_by(id=entity_id).first()

            entity_uuid = getattr(entity, "uuid")
            if entity_uuid:
                return session.query(cls.model).filter_by(uuid=entity_uuid).first()

            return None
