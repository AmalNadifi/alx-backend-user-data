#!/usr/bin/env python3
"""
The following module defines functions for hashing and validating passwords.
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    <this function hashes a password and returns the hashed value.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    <this function checks whether a password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to check.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
