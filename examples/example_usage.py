from algorithm_benchmark_toolkit.plots import generate_boxplots_from_csv
from algorithm_benchmark_toolkit.latex_generator import create_tables_latex
import subprocess
from pathlib import Path

def boxplot(data: str):
    generate_boxplots_from_csv(data)

def tables_latex(data: str) -> None:
    create_tables_latex(data)
    subprocess.run(['pdflatex', Path("outputs") / "tables" / "Median&std_table.tex"])

if __name__ == '__main__':
    # Example usage
    data = "data.csv"

    # Generate boxplots for the data
    generate_boxplots_from_csv(data)
    
    # Create LaTeX tables for the data
    create_tables_latex(data)
    
    # Compile the LaTeX tables to PDF (only works if pdflatex is installed)
    subprocess.run(['pdflatex', Path("outputs") / "tables" / "Median&std_table.tex"])