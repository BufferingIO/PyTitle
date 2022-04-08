class SrtError(Exception):
    """Base class for all exceptions in this module."""


class ShiftError(SrtError):
    """Raised when SrtSubtitle.shift() fails."""


class NegativeTimestampError(SrtError):
    """Raised when a negative timestamp is encountered."""


class SrtSaveError(SrtError):
    """Raised when SrtSubtitle.save() fails."""
