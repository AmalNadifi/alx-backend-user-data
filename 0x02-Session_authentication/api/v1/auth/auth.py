#!/usr/bin/env python3
""" Module for api authentication"""
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """Class for managing API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """This method checks if authentication is required for a given path.

        Args:
            path (str): The path to check for authentication requirement.
            excluded_paths (List[str]): Paths excluded from authentication

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if '*' in excluded_path:
                # Extract the part of the excluded path before the wildcard *
                prefix, _ = excluded_path.split('*', 1)
                if path.startswith(prefix):
                    return False
            elif path.startswith(excluded_path.rstrip('/')):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """This method gets the authorization header from the request.

        Args:
            request (Request): The Flask request object.

        Returns:
            str: The authorization header value if present, otherwise None.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """This method gets the current authenticated user.

        Args:
            request (Request): The Flask request object.

        Returns:
            TypeVar('User'): Current authenticated user object if available
                            otherwise None.
        """
        return None

    def session_cookie(self, request=None):
        """ This method returns a cookie value from a request
        Args:
            request (Request): The Flask request object.
        Returns:
            str: The value of the cookie named SESSION_NAME if present,
            otherwise None.
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
