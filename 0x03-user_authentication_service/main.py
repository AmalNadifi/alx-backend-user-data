#!/usr/bin/env python3
"""
The following module is for testing API endpoints
of the user authentication service.

This module contains:
    functions to test various API endpoints of the user authentication service.
The functions perform:
    API requests using the requests module
    and assert the expected status codes and payloads for each endpoint.

Usage:
    Run this module to test the API endpoints of user authentication service

Example:
    $ python main.py
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    This function tests registering a user with the given email & password.
    Args:
        email: the user's email
        password: the user's password
    """
    resp = requests.post("{}/users".format(BASE_URL),
                        data={'email': email, 'password': password})
    if resp.status_code == 200:
        assert (resp.json() == {"email": email, "message": "user created"})
    else:
        assert (resp.status_code == 400)
        assert (res.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    This function is a test for log in with the given wrong credentials.
    Args:
        email: The email of the user.
        password: The password of the user.
    Returns:
        None
    """
    r = requests.post(f"{BASE_URL}/sessions",
                    data={'email': email, 'password': password})
    assert (r.status_code == 401) 

def log_in(email: str, password: str) -> str:
    """
    This function isi to test for log in with
    the given correct email and password.
    Args:
        email: The email of the user.
        password: The password of the user.
    Returns:
        The session_id of the user.
    """
    resp = requests.post(f"{BASE_URL}/sessions",
                         data={'email': email, 'password': password})
    assert (resp.status_code == 200)
    assert(resp.json() == {"email": email, "message": "logged in"})
    return resp.cookies['session_id']


def profile_unlogged() -> None:
    """
    Test for profile without being logged in with session_id.
    Returns:
        None
    """
    res = requests.get(f"{BASE_URL}/profile")
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    This function is to test for profile with being logged in with session_id.
    Args:
        session_id: The session_id of the user.
    Returns:
        None
    """
    cookies = {'session_id': session_id}
    r = requests.get(f"{BASE_URL}/profile",
                     cookies=cookies)
    assert(r.status_code == 200)


def log_out(session_id: str) -> None:
    """
    This function is to test for log out with the given session_id.
    Args:
        session_id: The session_id of the user.
    Returns:
        None
    """
    cookies = {'session_id': session_id}
    r = requests.delete(f"{BASE_URL}/sessions",
                        cookies=cookies)
    if r.status_code == 302:
        assert(r.url == f"{BASE_URL}/")
    else:
        assert(r.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    This function is to rest for reset password token with the given email.
    Args:
        email: The email of the user.
    Returns:
        The reset_token of the user.
    """
    r = requests.post(f"{BASE_URL}/reset_password",
                      data={'email': email})
    if r.status_code == 200:
        return r.json()['reset_token']
    assert(r.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    This function is to test for update password with the given email,
    reset_token and new_password.
    Args:
        email: The email of the user.
        reset_token: The reset_token of the user.
        new_password: The new password of the user.
    Returns:
        None
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put(f"{BASE_URL}/reset_password",
                     data=data)
    if r.status_code == 200:
        assert(r.json() == {"email": email, "message": "Password updated"})
    else:
        assert(r.status_code == 403)


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
