from datetime import datetime
from decimal import Decimal
from typing import List

from desafio.domain.exceptions.transactions import (
    DailyWithdrawalLimitReached,
    InactiveAccount,
    InsufficientFund,
)
from desafio.domain.interactors import IInteractorFindMany
from desafio.domain.interactors.accounts import AccountInteractor
from desafio.domain.interactors._entities import Account, Transaction
from desafio.domain.repositories.transactions import TransactionRepository
from desafio.domain.repositories.decorators import with_lock
from desafio.logger import get_logger

LOGGER = get_logger()


class TransactionInteractor(IInteractorFindMany):
    entity = Transaction
    repository = TransactionRepository

    account_interactor = AccountInteractor

    @classmethod
    def find_many(cls, *args, **kwargs) -> List[dict]:
        LOGGER.info("Looking for transactions with %s", kwargs)
        found_transactions = cls.repository.get_many(*args, **kwargs)
        LOGGER.info("Found %s transactions with id %s", len(found_transactions), kwargs)
        return [transaction.dict() for transaction in found_transactions]

    @classmethod
    @with_lock("transactions")
    def deposit(cls, account_id: int, value: Decimal, *args, **kwargs) -> dict:
        if value <= 0:
            raise ValueError("Deposit value must be positive")

        account = cls._find_active_account_entity(account_id, *args, **kwargs)

        created_transaction = cls._commit_transaction(account, value, *args, **kwargs)

        return created_transaction.dict()

    @classmethod
    @with_lock("transactions")
    def withdrawal(cls, account_id: int, value: Decimal, *args, **kwargs) -> dict:
        if value >= 0:
            raise ValueError("Withdrawal value must be negative")

        account = cls._find_active_account_entity(account_id, *args, **kwargs)

        cls._check_sufficient_funds_to_withdraw(account.id, account.balance, value)
        cls._check_withdrawal_daily_limit(
            account.id, account.max_daily_withdrawal, value, *args, **kwargs
        )

        created_transaction = cls._commit_transaction(account, value, *args, **kwargs)

        return created_transaction.dict()

    @classmethod
    def _find_active_account_entity(cls, account_id: int, *args, **kwargs):
        account_dict = cls.account_interactor.find_one(id=account_id, *args, **kwargs)

        if not account_dict["is_active"]:
            raise InactiveAccount(account_id=account_dict["id"])

        return Account(**account_dict)

    @classmethod
    def _commit_transaction(
        cls, account: Account, value: Decimal, *args, **kwargs
    ) -> Transaction:
        """
        Persist transaction value and modify account's balance accordingly
        :param account: Account the transaction is action at
        :param value: Transaction value
        :param args:
        :param kwargs: atomic session
        :return: persisted transaction entity
        """
        account.balance += value
        transaction = cls.entity(
            value=value,
            account_id=account.id,
            processed_at=datetime.utcnow(),
            account=account,
        )

        LOGGER.info("Creating transaction for account %s", account.id)
        created_transaction = cls.repository.create(transaction, *args, **kwargs)
        LOGGER.info("Created transaction with id %s", created_transaction.id)

        return created_transaction

    # ######################  WITHDRAWAL  ###################### #

    @staticmethod
    def _check_sufficient_funds_to_withdraw(
        account_id: int,
        account_balance: Decimal,
        value: Decimal,
    ):
        if account_balance + value < 0:
            raise InsufficientFund(account_id=account_id, value=value)

    @classmethod
    def _check_withdrawal_daily_limit(
        cls,
        account_id: int,
        max_daily_withdrawal: Decimal,
        value: Decimal,
        *args,
        **kwargs
    ):
        if max_daily_withdrawal is None:
            return

        today_total_withdrawal = cls._sum_today_total_withdrawal(
            account_id, *args, **kwargs
        )
        if max_daily_withdrawal + (today_total_withdrawal + value) < 0:
            raise DailyWithdrawalLimitReached(account_id, value=value)

    @classmethod
    def _sum_today_total_withdrawal(cls, account_id: int, *args, **kwargs):
        kwargs["account_id"] = account_id
        today_withdrawals = cls.repository.get_today_withdrawals(*args, **kwargs)

        today_total_withdrawal = sum(
            [withdrawal.value for withdrawal in today_withdrawals]
        )

        return today_total_withdrawal
