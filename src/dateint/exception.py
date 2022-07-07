"""Module for custom exceptions."""


class FormatError(Exception):
    """Custom Exception for format errors."""


class FloatFormatError(Exception):
    """Custom Exception for format error when a float has a non-zero decimal part."""
