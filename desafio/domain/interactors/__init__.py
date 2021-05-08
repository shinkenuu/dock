from abc import ABCMeta, abstractmethod


class IInteractorCreate(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError()
