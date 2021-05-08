from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional


class IEntityRepository(metaclass=ABCMeta):
    entity: Any = None

    @classmethod
    @abstractmethod
    def get_one(cls, *args, **kwargs) -> Optional[Any]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_many(cls, *args, **kwargs) -> List[Any]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(cls, entity: Any) -> Any:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, entity: Any) -> Any:
        raise NotImplementedError
