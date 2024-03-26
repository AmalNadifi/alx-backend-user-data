#!/usr/bin/env python3
""" This module is a definition of a _hash_password function """
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    This function hashes a password string and returns it in bytes form
    Args:
        password (str): password in string format
    """
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())
