#!/usr/bin/env python3
""" This module is a definition of a _hash_password function """
import bcrypt
from uuid import uuid4
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    This function hashes a password string and returns it in bytes form
    Args:
        password (str): password in string format
    """
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    This function generates a uuid and returns its str representation
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """This is the initialization method"""
        self._db = DB()

    def register_user(self, email, password):
        """
        This method is to register the user

        Args:
            email (str): new user's email address
            password (str): new user's password
        Return:
            if no user with given email exists, return newly created user
            else raise ValueError
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        This function validates a user's login credentials

        Args:
            email (str): user's email address
            password (str): user's password
        Return:
            True if credentials are correct, else return False
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        passwd = password.encode("utf-8")
        return bcrypt.checkpw(passwd, user_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
        This function creates a session_id for an existing user
        and update the user's session_id attribute

        Args:
            email (str): user's email address
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id