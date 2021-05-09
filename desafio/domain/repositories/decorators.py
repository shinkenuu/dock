from functools import wraps

from desafio.domain.repositories._models import LocalSession
from desafio.logger import get_logger

LOGGER = get_logger()


def with_lock(table: str):  # noqa
    def decorator(func):
        @wraps(func)
        def wrap_func(cls, *args, **kwargs):
            with LocalSession() as session:
                session.begin_nested()
                session.execute(f"LOCK TABLE {table};")

                try:
                    kwargs["session"] = session
                    return func(cls, *args, **kwargs)

                except Exception as error:
                    LOGGER.error(error)
                    session.rollback()

                    raise error

        return wrap_func

    return decorator
