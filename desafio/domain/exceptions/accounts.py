class PersonNotFound(Exception):
    def __init__(self, **kwargs):
        error_message = f"Person not found by {kwargs}"
        super().__init__(error_message)


class DuplicatedPerson(Exception):
    def __init__(self, cpf: str):
        error_message = f"Duplicated person with cpf {cpf}"
        super().__init__(error_message)


class AccountNotFound(Exception):
    def __init__(self, **kwargs):
        error_message = f"Account not found by {kwargs}"
        super().__init__(error_message)
