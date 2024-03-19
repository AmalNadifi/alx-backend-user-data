#!/usr/bin/env python3
"""
Definition of class BasicAuth
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        This method returns a User instance based on email and password
        """
        if (user_email is None or not isinstance(user_email, str) or
                user_pwd is None or not isinstance(user_pwd, str)):
            return None

        users = User.search({"email": user_email})
        if not users or users == []:
            return None

        for us in users:
            if user.is_valid_password(user_pwd):
                return us

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This method overloads Auth and retrieves User instance for a request
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is not None:
            base64_token = self.extract_base64_authorization_header(auth_header)
            if base64_token is not None:
                decoded = self.decode_base64_authorization_header(base64_token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, password)
        return
