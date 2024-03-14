#!/usr/bin/env python3
"""
The following module Ddefines a filter_datum function to obfuscate sensitive
data in log messages, along with supporting classes and functions for logging
and database access.
"""
from typing import List
import re
import logging
import os
import mysql.connector


# Sensitive fields to be redacted
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    
    Args:
        fields (list): List of strings indicating fields to obfuscate.
        redaction (str): String representing the redacted content.
        message (str): The log line to obfuscate.
        separator (str): The character separating the fields.
        
    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(field + '=.*?' + separator,
                         field + '=' + redaction + separator, message)
    return message
