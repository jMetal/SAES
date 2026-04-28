"""Visualization subpackage for SAES."""

from __future__ import annotations

from saes.visualization.registry import PlotName, get_plot, register_plot

__all__ = ["PlotName", "get_plot", "register_plot"]
