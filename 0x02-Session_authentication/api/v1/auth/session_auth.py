#!/usr/bin/env python3
"""
Definition of class SessionAuth
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """This is the class of SessionAuth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ This method creates a session Id for user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ This method returns a user id based on a session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
