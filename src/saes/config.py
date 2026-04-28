"""Global configuration and styling for the SAES library."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ThemeConfig:
    """Configuration for plot styling and dimensions."""

    # Colors
    primary_color: str = "lightblue"
    secondary_color: str = "lightgreen"
    edge_color: str = "navy"
    grid_color: str = "gray"

    # Fonts
    font_family: str = "sans-serif"
    title_fontsize: int = 12
    label_fontsize: int = 10
    tick_fontsize: int = 10

    # Line widths & markers
    line_width: float = 1.5
    marker_size: float = 6.0
    grid_alpha: float = 0.7

    # Sizes
    single_plot_width: int = 8
    multi_plot_width: int = 30

    # Pareto front specific
    pareto_point_color: str = "blue"
    pareto_point_alpha: float = 0.5
    pareto_reference_color: str = "red"
    pareto_reference_alpha: float = 0.8
    pareto_reference_marker: str = "x"


# Global default theme instance
default_theme = ThemeConfig()
