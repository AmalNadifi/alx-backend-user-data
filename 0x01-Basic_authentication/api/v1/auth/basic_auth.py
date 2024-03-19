#!/usr/bin/env python3
"""
Definition of class BasicAuth
"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """This method decodes a Base-64-encoded str"""
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except base64.binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ This method extracts the user email and password
        from Base64 decoded value
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
