"""Custom exception hierarchy for the SAES library."""

from __future__ import annotations


class SAESException(Exception):
    """Base exception class for SAES library."""


class DataLoadError(SAESException):
    """Exception raised for errors in loading data or metrics."""


class ConfigurationError(SAESException):
    """Exception raised for invalid configurations or parameters."""


class StatisticalTestError(SAESException):
    """Exception raised for errors during statistical tests."""


class PostHocTestError(SAESException):
    """Exception raised for errors during post-hoc APV procedures."""


class VisualizationError(SAESException):
    """Exception raised for errors during plotting or visualization."""
