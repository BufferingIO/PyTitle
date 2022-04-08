class SrtError(Exception):
    """Base class for all exceptions in this module."""


class NegativeTimestampError(SrtError):
    """Raised when a negative timestamp is encountered."""


