from SAES.utils.csv_processor import process_csv
from SAES.utils.csv_processor import process_csv_metrics
from SAES.utils.csv_processor import process_dataframe_basic
from SAES.utils.csv_processor import process_dataframe_extended

from SAES.latex_generation.latex_tables import median_table
from SAES.latex_generation.latex_tables import friedman_table
from SAES.latex_generation.latex_tables import wilcoxon_pivot_table
from SAES.latex_generation.latex_tables import wilcoxon_table

import pandas as pd
import os

from SAES.latex_generation.__init__ import TableTypes

from SAES.logger import get_logger
logger = get_logger(__name__)

def __latex_document_builder(body: str, output_path: str) -> None:
    """
    Generates a LaTeX document for comparison tables and saves it to the specified path.

    Args:
        body (str): 
            The LaTeX content to be included within the `\\section{Tables}` environment.
        
        output_path (str): 
            The file path where the LaTeX document will be saved, including the file name.

    Returns:
        None: The function saves the LaTeX document to disk.
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
    with open(output_path+".tex", "w") as f:
        f.write(latex_doc)

def __create_tables_latex(df_m: pd.DataFrame, metric: str, maximize: bool, output_dir: str) -> None:
    """
    Generates and saves LaTeX tables based on the provided metric and CSV data.

    This function processes the input dataframe to compute aggregate values, standard deviations, and 
    statistical test results, then creates and saves LaTeX tables for various analyses, including: base table with aggregation and standard deviation; Friedman test table; Wilcoxon pivot table and Wilcoxon test (1vs1).

    Args:
        csv (pd.DataFrame): 
            DataFrame containing the data to be processed.

        metric (str):
            The metric to analyze (e.g., "accuracy", "precision").

        maximize (bool): 
            If True, indicates that higher metric values are better, influencing the Friedman test.
        
        output_dir (str):
            The path to the directory where the LaTeX tables will be saved.

    Returns:
        None: The function saves the LaTeX tables to disk.
    """

    # Process the input DataFrame to calculate aggregate values and standard deviations
    df_agg, df_std, aggregation_type, _ = process_dataframe_extended(df_m, metric)
    df_og, _ = process_dataframe_basic(df_m, metric)

    # Generate LaTeX tables for the given metric
    median = median_table(f"{aggregation_type} and Standard Deviation ({metric})", df_og, df_agg, df_std)
    friedman = friedman_table(f"{aggregation_type} and Standard Deviation - Friedman Test ({metric})", df_og, df_agg, df_std, maximize)
    wilcoxon_pivot = wilcoxon_pivot_table(f"{aggregation_type} and Standard Deviation - Wilcoxon Pivot ({metric})", df_og, df_agg, df_std)
    wilcoxon = wilcoxon_table(f"Wilcoxon Test 1vs1 ({metric})", df_og)

    # Save the LaTeX tables to disk
    __latex_document_builder(median, os.path.join(output_dir, "median"))
    __latex_document_builder(friedman, os.path.join(output_dir, "friedman"))
    __latex_document_builder(wilcoxon_pivot, os.path.join(output_dir, "wilcoxon_pivot"))
    __latex_document_builder(wilcoxon, os.path.join(output_dir, "wilcoxon"))

def latex_selected(data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str, selected: str) -> str:
    """
    Generates LaTeX tables for the specified metric and selected analysis.

    Args:
        data (str | pd.DataFrame): 
            The input data in CSV file path or DataFrame format.
        
        metrics (str | pd.DataFrame): 
            The metrics in CSV file path or DataFrame format.
        
        metric (str):
            The metric to analyze (e.g., "accuracy", "precision").
        
        selected (str):
            The selected analysis to perform -> ("median", "friedman", "wilcoxon_pivot", "wilcoxon").
    
    Returns:
        str: The path to the directory containing the generated tables.

    Example:
        >>> from SAES.latex_generation.latex_skeleton import latex_selected
        >>> 
        >>> # Data source
        >>> experimentData = "swarmIntelligence.csv"
        >>> 
        >>> # Metrics source
        >>> metrics = "metrics.csv"
        >>> 
        >>> # Metric to analyze
        >>> metric = "HV"
        >>> 
        >>> # Selected analysis
        >>> selected = "wilcoxon_pivot"
        >>> 
        >>> # Save the latex reports on disk
        >>> output_dir = latex_selected(data, metrics, metric)
        >>> print(output_dir)
        LaTeX wilcoxon_pivot document for metric HV saved to {output_dir}
        {output_dir}
    """

    # Create the output directory for the tables
    output_dir = os.path.join(os.getcwd(), "outputs", "latex", metric)

    # Process the input data and metrics
    df_m, maximize = process_csv_metrics(data, metrics, metric)
    df_agg, df_std, aggregation_type, _ = process_dataframe_extended(df_m, metric)
    df_og, _ = process_dataframe_basic(df_m, metric)

    if selected == TableTypes.MEDIAN.value:
        body = median_table(f"{aggregation_type} and Standard Deviation ({metric})", df_og, df_agg, df_std)
    elif selected == TableTypes.FRIEDMAN.value:
        body = friedman_table(f"{aggregation_type} and Standard Deviation - Friedman Test ({metric})", df_og, df_agg, df_std, maximize)
    elif selected == TableTypes.WILCOXON_PIVOT.value:
        body = wilcoxon_pivot_table(f"{aggregation_type} and Standard Deviation - Wilcoxon Pivot ({metric})", df_og, df_agg, df_std)
    elif selected == TableTypes.WILCOXON_PIVOT.value:
        body = wilcoxon_table(f"Wilcoxon Test 1vs1 ({metric})", df_og)
    else:
        raise ValueError("Invalid selected analysis. Please choose one of the following: 'median', 'friedman', 'wilcoxon_pivot', 'wilcoxon'.")

    # Save the LaTeX tables to disk
    __latex_document_builder(body, os.path.join(output_dir, selected))
    logger.info(f"LaTeX {selected} document for metric {metric} saved to {output_dir}")
    return os.path.join(output_dir, selected+".tex")

def latex(data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str) -> str:
    """
    Processes the input data and metrics, and generates all the LaTeX reports on disk for a specific metric.

    Args:
        data (str | pd.DataFrame): 
            The input data in CSV file path or DataFrame format.
        
        metrics (str | pd.DataFrame): 
            The metrics in CSV file path or DataFrame format.
        
        metric (str):
            The metric to analyze (e.g., "accuracy", "precision").

    Returns:
        str: The path to the directory containing the generated tables.

    Example:
        >>> from SAES.latex_generation.latex_skeleton import latex
        >>> 
        >>> # Data source
        >>> experimentData = "swarmIntelligence.csv"
        >>> 
        >>> # Metrics source
        >>> metrics = "metrics.csv"
        >>> 
        >>> # Metric to analyze
        >>> metric = "HV"
        >>> 
        >>> # Save the latex reports on disk
        >>> output_dir = latex(data, metrics, metric)
        >>> print(output_dir)
        LaTeX document for metric HV saved to {output_dir}
        {output_dir}
    """

    # Process the input data and metrics
    df_m, maximize = process_csv_metrics(data, metrics, metric)

    # Create the output directory for the tables
    output_dir = os.path.join(os.getcwd(), "outputs", "latex", metric)

    # Generate LaTeX tables for the current metric
    __create_tables_latex(df_m, metric, maximize, output_dir)

    # Log the successful generation of the LaTeX tables
    logger.info(f"LaTeX document for metric {metric} saved to {output_dir}")
    return output_dir

def latex_all_metrics(data: str | pd.DataFrame, metrics: str | pd.DataFrame) -> str:
    """
    Processes the input data and metrics, and generates all the LaTeX reports for each metric.

    Args:
        data (str | pd.DataFrame): 
            The input data in CSV file path or DataFrame format.
        
        metrics (str | pd.DataFrame): 
            The metrics in CSV file path or DataFrame format.

    Returns:
        str: The path to the directory containing the generated tables.

    Example:
        >>> from SAES.latex_generation.latex_skeleton import latex_all_metrics
        >>> 
        >>> # Data source
        >>> experimentData = "swarmIntelligence.csv"
        >>> 
        >>> # Metrics source
        >>> metrics = "metrics.csv"
        >>> 
        >>> # Save the latex reports on disk
        >>> output_dir = latex_all_metrics(data, metrics)
        >>> print(output_dir)
        LaTeX document for metric HV saved to {output_dir}
        {output_dir}
    """

    # Process the input data and metrics
    data = process_csv(data, metrics)

    # Create the output directory for the tables
    output_dir = os.path.join(os.getcwd(), "outputs", "latex")

    # Process the input data and metrics
    for metric, (df_m, maximize) in data.items():
        # Create the output directory for the current metric
        output_path = os.path.join(output_dir, metric)

        # Generate LaTeX tables for the current metric
        __create_tables_latex(df_m, metric, maximize, output_path)
        logger.info(f"LaTeX document for metric {metric} saved to {output_path}")

    return output_dir
