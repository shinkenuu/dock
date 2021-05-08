from datetime import datetime
from decimal import Decimal

from pycpfcnpj import cpf as pycpf, compatible as cpf_compatible

from desafio.domain.exceptions.accounts import AccountNotFound
from desafio.domain.interactors import (
    IInteractorCreate,
    IInteractorFindOne,
    IInteractorUpdate,
)
from desafio.domain.interactors._entities import Account, Person
from desafio.domain.repositories.accounts import AccountRepository, PersonRepository
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
    def create(
        cls,
        name: str = None,
        cpf: str = None,
        birth_date: datetime = None,
        *args,
        **kwargs,
    ) -> dict:
        clean_cpf = cls.clean_cpf(cpf)
        entity = cls.entity(name=name, cpf=clean_cpf, birth_date=birth_date)

        LOGGER.info("Creating person...")
        persisted_entity = cls.repository.create(entity)
        LOGGER.info("Created person with id %s", persisted_entity.id)

        return persisted_entity.dict()


class AccountInteractor(IInteractorFindOne, IInteractorCreate, IInteractorUpdate):
    entity = Account
    repository = AccountRepository

    @classmethod
    def _find_entity(cls, *args, **kwargs):
        found_entity = cls.repository.get_one(*args, **kwargs)

        if not found_entity:
            raise AccountNotFound(**kwargs)

        return found_entity

    @classmethod
    def find_one(cls, *args, **kwargs) -> dict:
        LOGGER.info("Looking for a account with %s", kwargs)
        found_account = cls._find_entity(*args, **kwargs)
        LOGGER.info("Found account with id %s", found_account.id)
        return found_account.dict()

    @classmethod
    def create(
        cls,
        balance: Decimal = None,
        max_daily_withdrawal: Decimal = None,
        is_active: bool = None,
        person_id: int = None,
        *args,
        **kwargs,
    ) -> dict:
        created_at = datetime.utcnow()
        entity = cls.entity(
            balance=balance,
            max_daily_withdrawal=max_daily_withdrawal,
            is_active=is_active,
            created_at=created_at,
            person_id=person_id,
        )

        LOGGER.info("Creating account...")
        persisted_entity = cls.repository.create(entity)
        LOGGER.info("Created account with id %s", persisted_entity.id)

        return persisted_entity.dict()

    @classmethod
    def update(cls, id: int, is_active: bool = None, *args, **kwargs):
        existing_entity = cls._find_entity(id=id)
        existing_entity.is_active = is_active

        LOGGER.info("Updating account...")
        updated_entity = cls.repository.update(existing_entity)
        LOGGER.info("Updated account with id %s", updated_entity.id)

        return updated_entity.dict()
