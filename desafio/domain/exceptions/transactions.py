from decimal import Decimal


class InactiveAccount(Exception):
    def __init__(self, account_id):
        error_message = f"Account {account_id} is inactive"
        super().__init__(error_message)


class InsufficientFund(Exception):
    def __init__(self, account_id: int, value: Decimal):
        error_message = (
            f"Insufficient funds for account {account_id} with value {value}"
        )
        super().__init__(error_message)


class DailyWithdrawalLimitReached(Exception):
    def __init__(self, account_id: int, value: Decimal):
        error_message = f"Daily withdrawal limit reached for account {account_id} with value {value}"
        super().__init__(error_message)
