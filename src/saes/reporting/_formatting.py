"""Shared LaTeX formatting utilities."""

from __future__ import annotations


def latex_document_header() -> str:
    """Return the LaTeX document preamble."""
    return """
        \\documentclass{article}
        \\title{Algorithms Comparison}
        \\usepackage{colortbl}
        \\usepackage{float}
        \\usepackage{rotating}
        \\usepackage[table*]{xcolor}
        \\usepackage{tabularx}
        \\usepackage{siunitx}
        \\sisetup{output-exponent-marker=\\text{e}}
        \\xdefinecolor{gray95}{gray}{0.65}
        \\xdefinecolor{gray25}{gray}{0.8}
        \\author{YourName}
        \\begin{document}
        \\maketitle
        \\section{Tables}"""


def latex_document_footer() -> str:
    """Return the LaTeX document closing."""
    return """
        \\end{document}
        """


def format_cell(value: float, dispersion: float, *, is_best: bool, is_second: bool) -> str:
    """Format a single LaTeX table cell with optional highlighting."""
    cell = f"${value:.2e}_{{ {dispersion:.2e} }}$"
    if is_best:
        return f"\\cellcolor{{gray95}}{cell}"
    if is_second:
        return f"\\cellcolor{{gray25}}{cell}"
    return cell
