from SAES.plots import generate_boxplots_from_csv
from SAES.latex_generator import create_tables_latex_metrics
import subprocess
from pathlib import Path

if __name__ == '__main__':
    # Example usage
    data = "data.csv"
    metrics = "metrics.csv"

    # Generate boxplots for the data
    generate_boxplots_from_csv(data, metrics)
    
    # Create LaTeX tables for the data
    create_tables_latex_metrics(data, metrics)
    
    # Compile the LaTeX tables to PDF (only works if pdflatex is installed)
    subprocess.run(['pdflatex', Path("outputs") / "tables" / "Median&std_table_Java.tex"])
    subprocess.run(['pdflatex', Path("outputs") / "tables" / "Median&std_table_Python.tex"])