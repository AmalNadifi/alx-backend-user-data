#!/usr/bin/env python3
"""
Define class SessionDButh
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """This is the SessionDBAuth class that persists session data in a DB"""

    def create_session(self, user_id=None):
        """ This method creates a session id for a user id
        Args:
            user_id (str): the user id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
                "user_id": user_id,
                "session_id": session_id
        }
        user = UserSession(**session_dictionary)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ This method returns the user id based on a session id
        Args:
            session_id (str): the session id
        Return:
            user id or None if session_id is None or not str
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """ This method destroys a UserSession instance based on a session id
        from a request cookie"""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
