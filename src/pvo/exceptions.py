"""Exceptions for the PVOutput API client."""


class PVOutputError(Exception):
    """Generic PVOutput exception."""


class PVOutputAuthenticationError(PVOutputError):
    """PVOutput authentication exception."""


class PVOutputConnectionError(PVOutputError):
    """PVOutput connection exception."""


class PVOutputNoDataError(PVOutputError):
    """PVOutput has no data available exception."""


class InvalidSystemIDError(PVOutputError):
    """Invalid system ID exception."""
