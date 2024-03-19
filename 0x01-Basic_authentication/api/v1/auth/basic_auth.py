#!/usr/bin/env python3
"""
Definition of class BasicAuth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ This is the class of BasicAuth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        This method extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header value.

        Returns:
            str: The Base64 part of the Authorization header if valid,
            otherwise None.
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split("Basic ")[1].strip()
