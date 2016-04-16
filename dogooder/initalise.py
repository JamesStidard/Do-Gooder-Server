import os
import logging

from utilise.password_helper import PasswordHelper as PWH

from dogooder.utils.config import CONFIG
from dogooder.control import Control
from dogooder.utils.orm_utils import drop_all, create_all
from dogooder.model import *


def main():
    logging.info("db: %s", CONFIG.DB_URL)

    control = Control(CONFIG.DB_URL)
    with control.session as session:
        drop_all(session)

        create_all(Base, control._engine)

        user = User(
            username='test',
            _email='test@test.com',
            email_confirmed=True,
            _password=PWH.create_password('password'),
        )
        session.add(user)


if __name__ == "__main__":
    main()
