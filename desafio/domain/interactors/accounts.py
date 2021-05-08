from pycpfcnpj import cpf as pycpf, compatible as cpf_compatible

from desafio.domain.interactors._entities import Account
from desafio.domain.interactors import IInteractorCreate
from desafio.domain.interactors._entities import Person
from desafio.domain.repositories.people import PersonRepository
from desafio.logger import get_logger

LOGGER = get_logger()


class PersonInteractor(IInteractorCreate):
    entity = Person
    repository = PersonRepository

    @staticmethod
    def clean_cpf(cpf) -> str:
        """
        >>> PersonInteractor.clean_cpf('060.215.473-14')
        '06021547314'
        """
        if not pycpf.validate(cpf):
            raise ValueError("Invalid CPF")

        clean_cpf = cpf_compatible.clear_punctuation(cpf)
        return clean_cpf

    @staticmethod
    def mask_cpf(cpf: str) -> str:
        """
        >>> PersonInteractor.mask_cpf('06021547314')
        '060.215.473-14'
        """
        first_section = cpf[:3]
        second_section = cpf[3:6]
        third_section = cpf[6:9]
        verification_digits = cpf[-2:]

        masked_cpf = (
            f"{first_section}.{second_section}.{third_section}-{verification_digits}"
        )
        return masked_cpf

    @classmethod
    def create(cls, *args, **kwargs) -> dict:
        cpf = kwargs.pop("cpf", None)
        clean_cpf = cls.clean_cpf(cpf)
        kwargs["cpf"] = clean_cpf

        entity = cls.entity(**kwargs)

        LOGGER.info("Creating person...")
        persisted_entity = cls.repository.create(entity)
        LOGGER.info("Created person with id %s", persisted_entity.id)

        return persisted_entity.dict()


class AccountInteractor(IInteractorCreate):
    entity: Account
    repository: None

    @classmethod
    def create(cls, *args, **kwargs) -> dict:
        return {}
