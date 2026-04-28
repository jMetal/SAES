"""Registry for visualization plots — enables pluggable extensibility."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from saes.exceptions import ConfigurationError


class PlotName(StrEnum):
    """Available plot types."""

    BOXPLOT = "boxplot"
    VIOLIN = "violin"
    HISTOGRAM = "histogram"
    CD_PLOT = "cd_plot"
    POSTERIOR = "posterior"
    FRONT_2D = "front_2d"
    FRONT_3D = "front_3d"
    FRONT_ND = "front_nd"


# Global registry mapping lowercase names to plot classes
_REGISTRY: dict[str, type] = {}


def register_plot(name: str | PlotName) -> Any:
    """Decorator to register a plot class by name.

    Usage::

        @register_plot(PlotName.BOXPLOT)
        class Boxplot(BasePlot): ...

    Args:
        name: Case-insensitive identifier or :class:`PlotName`.

    Returns:
        Decorator function.
    """

    def decorator(cls: type) -> type:
        _REGISTRY[str(name).lower()] = cls
        return cls

    return decorator


def get_plot(name: str | PlotName, *args: Any, **kwargs: Any) -> Any:
    """Instantiate a plot by its registered name.

    Args:
        name: Case-insensitive name or :class:`PlotName`.
        *args: Positional arguments forwarded to the plot constructor.
        **kwargs: Keyword arguments forwarded to the plot constructor.

    Returns:
        An instance of the requested plot.

    Raises:
        ConfigurationError: If the name is not registered.
    """

    key = str(name).lower()
    if key not in _REGISTRY:
        import importlib

        module_map = {
            "boxplot": "saes.visualization.plots.boxplot",
            "cd_plot": "saes.visualization.plots.cd_plot",
            "histogram": "saes.visualization.plots.histogram",
            "posterior": "saes.visualization.plots.posterior",
            "violin": "saes.visualization.plots.violin",
            "front_2d": "saes.pareto.front_2d",
            "front_3d": "saes.pareto.front_3d",
            "front_nd": "saes.pareto.front_nd",
        }
        if key in module_map:
            importlib.import_module(module_map[key])

    if key not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY.keys()))
        msg = f"Unknown plot '{name}'. Available: {available}"
        raise ConfigurationError(msg)
    return _REGISTRY[key](*args, **kwargs)
