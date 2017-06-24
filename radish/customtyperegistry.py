# -*- coding: utf-8 -*-

"""
    This module provides the Argument-Expression Registry
"""

from singleton import singleton

from .exceptions import RadishError

from parse_type import TypeBuilder


@singleton()
class CustomTypeRegistry(object):
    """
        Registry for all custom argument expressions
    """
    def __init__(self):
        self.custom_types = {}

    def register(self, name, func):
        """
        Registers a custom type
        """
        if name in self.custom_types:
            raise RadishError("Cannot register custom type with name {0} because it already exists".format(name))

        self.custom_types[name] = func


def custom_type(name, pattern):
    """
    Decorator for custom type pattern
    """
    def _decorator(func):
        """
        Actual decorator
        """
        func.pattern = pattern
        CustomTypeRegistry().register(name, func)

        return func
    return _decorator


def register_custom_type(**kwargs):
    """
    Register the given custom types
    """
    for name, func in kwargs.items():
        CustomTypeRegistry().register(name, func)


@custom_type("MathExpression", r"[0-9 +\-*/%.e]+")
def math_expression_type(text):
    """
    Custom Type which expects a valid math expression

    :param str text: the text which was matched as math expression

    :returns: calculated float number from the math expression
    :rtype: float
    """
    return float(eval(text))


@custom_type('QuotedString', r'"(?:[^"\\]|\\.)*"')
def quoted_string_type(text):
    """
    Custom type to parse a quoted string.

    Double quotes (") have to be escaped with a
    backslash within the double quotes.
    """
    return text[1:-1]
