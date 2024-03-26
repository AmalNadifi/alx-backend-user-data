#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        This function creates a user object and saves it to the database

        Args:
            email (str): User's email address.
            hashed_password (str): User's hashed password.

        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        This function retrieves a user whose attributes match
        the attributes provided as arguments.

        Args:
            kwargs (dict): A dictionary of attributes to match the user.

        Returns:
            User: The matching user if found.

        Raises:
            InvalidRequestError: If an invalid attribute is provided.
            NoResultFound: If no user is found with the provided attributes.
        """
        all_users = self._session.query(User)
        for attr_name, attr_value in kwargs.items():
            if attr_name not in User.__dict__:
                raise InvalidRequestError
            for user in all_users:
                if getattr(user, attr_name) == attr_value:
                    return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        This method updates a 'user' attributes

        Args:
            user_id(int): the user id
            kwargs(dict) : a dictionnary of the user's attributes

        Returns:
            None
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
