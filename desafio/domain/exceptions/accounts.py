class DuplicatedPerson(Exception):
    def __init__(self, cpf: str):
        error_message = f"Duplicated person with cpf {cpf}"
        super().__init__(error_message)
