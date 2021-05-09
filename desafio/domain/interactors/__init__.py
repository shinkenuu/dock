from abc import ABCMeta, abstractmethod


class IInteractorFindOne(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def find_one(cls, *args, **kwargs):
        raise NotImplementedError()


class IInteractorFindMany(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def find_many(cls, *args, **kwargs):
        raise NotImplementedError()


class IInteractorCreate(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError()


class IInteractorUpdate(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def update(cls, id: int, *args, **kwargs):
        raise NotImplementedError()
