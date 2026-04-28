"""Registry for reporting tables — enables pluggable extensibility."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from saes.exceptions import ConfigurationError


class TableName(StrEnum):
    """Available reporting table types."""

    MEAN_MEDIAN = "mean_median"
    FRIEDMAN = "friedman"
    FRIEDMAN_P_VALUES = "friedman_p_values"
    ANOVA = "anova"
    WILCOXON = "wilcoxon"
    WILCOXON_PIVOT = "wilcoxon_pivot"
    T_TEST = "t_test"
    T_TEST_PIVOT = "t_test_pivot"


# Global registry mapping lowercase names to table classes
_REGISTRY: dict[str, type] = {}


def register_table(name: str | TableName) -> Any:
    """Decorator to register a table class by name.

    Usage::

        @register_table(TableName.MEAN_MEDIAN)
        class MeanMedianTable(BaseTable): ...

    Args:
        name: Case-insensitive identifier or :class:`TableName`.

    Returns:
        Decorator function.
    """

    def decorator(cls: type) -> type:
        _REGISTRY[str(name).lower()] = cls
        return cls

    return decorator


def get_table(name: str | TableName, *args: Any, **kwargs: Any) -> Any:
    """Instantiate a table by its registered name.

    Args:
        name: Case-insensitive name or :class:`TableName`.
        *args: Positional arguments forwarded to the table constructor.
        **kwargs: Keyword arguments forwarded to the table constructor.

    Returns:
        An instance of the requested table.

    Raises:
        ConfigurationError: If the name is not registered.
    """

    key = str(name).lower()
    if key not in _REGISTRY:
        import importlib

        module_map = {
            "mean_median": "saes.reporting.tables.mean_median",
            "friedman": "saes.reporting.tables.friedman",
            "friedman_p_values": "saes.reporting.tables.friedman",
            "anova": "saes.reporting.tables.anova",
            "wilcoxon": "saes.reporting.tables.wilcoxon",
            "wilcoxon_pivot": "saes.reporting.tables.wilcoxon",
            "t_test": "saes.reporting.tables.t_test",
            "t_test_pivot": "saes.reporting.tables.t_test",
        }
        if key in module_map:
            importlib.import_module(module_map[key])

    if key not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY.keys()))
        msg = f"Unknown table '{name}'. Available: {available}"
        raise ConfigurationError(msg)
    return _REGISTRY[key](*args, **kwargs)
