from SAES.utils.csv_processor import process_csv
from SAES.utils.csv_processor import process_csv_metrics
from SAES.utils.csv_processor import process_dataframe_basic
from SAES.utils.csv_processor import process_dataframe_extended

from SAES.latex_generation.latex_tables import base_table
from SAES.latex_generation.latex_tables import friedman_table
from SAES.latex_generation.latex_tables import wilconxon_pivot_table
from SAES.latex_generation.latex_tables import wilconxon_table

import pandas as pd
import os

from SAES.logger import get_logger
logger = get_logger(__name__)

def latex_document_builder(body: str, output_path: str):
    """
    Generates a LaTeX document for comparison tables and saves it to the specified path.

    Parameters:
        body (str): The LaTeX content to be included within the `\\section{Tables}` environment.
        output_path (str): The file path where the LaTeX document will be saved, including the file name.
    """

    # Step 1: Define the LaTeX document preamble and initial structure
    latex_doc = """
    \\documentclass{article}
    \\title{AlgorithmsComparison}
    \\usepackage{colortbl}
    \\usepackage{float}
    \\usepackage[table*]{xcolor}
    \\usepackage{tabularx}
    \\xdefinecolor{gray95}{gray}{0.65}
    \\xdefinecolor{gray25}{gray}{0.8}
    \\author{YourName}
    \\begin{document}
    \\maketitle
    \\section{Tables}"""

    # Step 2: Append the provided body content to the LaTeX document
    latex_doc += body

    # Step 3: Close the LaTeX document structure
    latex_doc += """
    \\end{document}
    """

    # Step 4: Ensure the output directory exists
    folder_path = os.path.dirname(output_path)
    os.makedirs(folder_path, exist_ok=True)

    # Step 5: Save the LaTeX document to the specified file
    with open(output_path, "w") as f:
        f.write(latex_doc)

    # Step 6: Print confirmation message
    logger.warning(f"LaTeX document saved to {output_path}")

def create_tables_latex(csv: pd.DataFrame, metric: str, maximize: bool) -> None:
    """
    Generates and saves LaTeX tables based on the provided metric and CSV data.

    This function processes the input dataframe to compute aggregate values, standard deviations, and 
    statistical test results, then creates and saves LaTeX tables for various analyses, including:
    - Base table with aggregation and standard deviation
    - Friedman test table
    - Wilcoxon pivot table
    - Wilcoxon test (1vs1)

    Args:
        csv (pd.DataFrame): DataFrame containing the data to be processed.
        metric (str): The metric to analyze (e.g., "accuracy", "precision").
        maximize (bool): If True, indicates that higher metric values are better, influencing the Friedman test.

    Returns:
        None: The function saves the LaTeX tables to disk.
    """

    # Process the input DataFrame to calculate aggregate values and standard deviations
    df_agg, df_std, aggregation_type = process_dataframe_extended(csv, metric)
    df_og = process_dataframe_basic(csv, metric)

    # Generate LaTeX tables for the given metric
    base = base_table(f"{aggregation_type} and Standard Deviation ({metric})", df_og, df_agg, df_std)
    friedman = friedman_table(f"{aggregation_type} and Standard Deviation - Friedman Test ({metric})", df_og, df_agg, df_std, maximize)
    wilconxon_pivot = wilconxon_pivot_table(f"{aggregation_type} and Standard Deviation - Wilconxon Pivot ({metric})", df_og, df_agg, df_std)
    wilconxon = wilconxon_table(f"Wilconxon Test 1vs1 ({metric})", df_og)

    # Save the LaTeX tables to disk
    latex_document_builder(base, os.path.join(os.getcwd(), "outputs", "tables", metric, "base_table_tex"))
    latex_document_builder(friedman, os.path.join(os.getcwd(), "outputs", "tables", metric, "friedman_table_tex"))
    latex_document_builder(wilconxon_pivot, os.path.join(os.getcwd(), "outputs", "tables", metric, "wilconxon_pivot_table_tex"))
    latex_document_builder(wilconxon, os.path.join(os.getcwd(), "outputs", "tables", metric, "wilconxon_table_tex"))

def create_tables_latex_metrics(data: str | pd.DataFrame, metrics: str | pd.DataFrame) -> None:
    """
    Processes the input data and metrics, and generates LaTeX tables for each metric.

    Parameters:
    - data (str | pd.DataFrame): The input data in CSV file path or DataFrame format.
    - metrics (str | pd.DataFrame): The metrics in CSV file path or DataFrame format.

    This function processes the provided data and metrics, and for each metric, it 
    generates a LaTeX table using `create_tables_latex` based on the processed data.
    """

    # Process the input data and metrics
    data = process_csv(data, metrics)

    # Process the input data and metrics
    for metric, (df_m, maximize) in data.items():
        # Generate LaTeX tables for the current metric
        create_tables_latex(df_m, metric, maximize)
        
if __name__ == "__main__":
    data = "/home/khaosdev/algorithm-benchmark-toolkit/notebooks/data.csv"
    metrics = "/home/khaosdev/algorithm-benchmark-toolkit/notebooks/metrics.csv"

    data2 = "/home/khaosdev/algorithm-benchmark-toolkit/examples/data.csv"
    metrics2 = "/home/khaosdev/algorithm-benchmark-toolkit/examples/metrics.csv"
    create_tables_latex_metrics(data2, metrics2)