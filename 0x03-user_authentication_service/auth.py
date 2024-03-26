#!/usr/bin/env python3
""" This module is a definition of a _hash_password function """
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import IntegrityError


def _hash_password(password: str) -> bytes:
    """
    This function hashes a password string and returns it in bytes form
    Args:
        password (str): password in string format
    """
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


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
        hashed_password = _hash_password(password)
        try:
            user = self._db.add_user(email, hashed_password)
            return user
        except IntegrityError:
            raise ValueError(f"User {email} already exists")
