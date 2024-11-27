from csv_processor import process_csv_extended
from csv_processor import process_csv_basic
from stats import wilcoxon_test
import pandas as pd
import os

def create_base_table(title: str, df1: pd.DataFrame, df2: pd.DataFrame, algorithms: list) -> str:
    """
    Generates a LaTeX table that compares two dataframes `df1` and `df2` based on the performance scores
    of different algorithms, with specific formatting to highlight the highest and second-highest scores.

    The function assumes that `df1` and `df2` are pandas DataFrames with the same structure, where:
    - The rows represent the entities being compared (e.g., algorithms or methods).
    - The columns represent different algorithms, and the values are performance scores (e.g., accuracy, error, etc.).

    The LaTeX table will:
    - Display the comparison of scores for each algorithm.
    - Highlight the maximum score with a light gray background and the second-highest score with a darker gray background.
    - Include the algorithm names as column headers.
    - Format the values of `df1` and `df2` in a specific LaTeX math format.

    Args:
    - df1 (pandas.DataFrame): The first dataframe containing performance scores for the algorithms.
    - df2 (pandas.DataFrame): The second dataframe containing performance scores for the algorithms.
    - algorithms (list of str): A list of algorithm names to be used as column headers in the LaTeX table.

    Returns:
    - str: A string containing the LaTeX code for the table.
    """

    # Initialize the LaTeX table with basic structure, including the table header
    latex_doc = """
    \\begin{table}[H]
    \\caption{EP. """ + title + """}
    \\vspace{1mm}
    \\centering
    \\begin{scriptsize}
    \\begin{tabularx}{\\textwidth}{l""" + "X"*len(algorithms) + """}
    \\hline
    & \\centering\\arraybackslash """ + " & \\centering\\arraybackslash ".join(algorithms) + " \\\\ \\hline\n"

    # Iterate through each row of df1 and df2, representing different problems or comparisons
    for (idx1, row1), (_, row2) in zip(df1.iterrows(), df2.iterrows()):
        # Combine the median and standard deviation values from df1 and df2 into a single DataFrame for sorting
        data = pd.DataFrame({title: row1, 'std_dev': row2})

        # Sort data by median score (descending) and by standard deviation (ascending) to identify best scores
        sorted_data = data.sort_values(by=[title, 'std_dev'], ascending=[False, True])

        # Extract the indices of the highest and second-highest scores based on the sorting
        max_idx, second_idx = sorted_data.index[0], sorted_data.index[1]
    
        # Initialize the row of LaTeX table content with the problem name
        row_data = f"{idx1} & "

        # Loop through each algorithm's score pair (from df1 and df2) to populate the table
        for (index1, score1), (_, score2) in zip(row1.items(), row2.items()):
            # Format and highlight the maximum and second highest values with gray background
            if index1 == max_idx:
                row_data += f"\\cellcolor{{gray95}}${score1:.2f}_{{ {score2:.2f} }}$ & "
            elif index1 == second_idx:
                row_data += f"\\cellcolor{{gray25}}${score1:.2f}_{{ {score2:.2f} }}$ & "
            else:
                row_data += f"${score1:.2f}_{{ {score2:.2f} }}$ & "

        # Remove the last unnecessary "&" and append the row to the LaTeX document
        latex_doc += row_data.rstrip(" & ") + " \\\\ \n"

    # Close the table structure in the LaTeX document
    latex_doc += """
    \\hline
    \\end{tabularx}
    \\end{scriptsize}
    \\end{table}
    """

    # Return the final LaTeX code for the table
    return latex_doc

def create_wilconxon_table(title: str, df_og: pd.DataFrame, df1: pd.DataFrame, df2: pd.DataFrame, algorithms: list) -> str:
    """
    Generates a LaTeX table comparing the performance scores of different algorithms based on two dataframes `df1` and `df2`.
    The table highlights the highest and second-highest scores with different background colors, and includes statistical results
    from a Wilcoxon signed-rank test for pairwise comparisons.

    Args:
    - title (str): The title for the LaTeX table.
    - df_og (pandas.DataFrame): The original dataframe containing the performance scores of algorithms.
    - df1 (pandas.DataFrame): The first dataframe containing performance scores (e.g., for algorithm A).
    - df2 (pandas.DataFrame): The second dataframe containing performance scores (e.g., for algorithm B).
    - algorithms (list of str): A list of algorithm names to be used as column headers in the LaTeX table.

    Returns:
    - str: The LaTeX code for the formatted table.

    This function assumes that:
    - `df1` and `df2` have the same structure, with rows representing the problems/algorithms and columns representing performance metrics.
    - `df_og` contains information necessary for calculating Wilcoxon signed-rank test results between pairs of algorithms.
    """

    # Initialize the LaTeX document with the table structure and formatting
    latex_doc = """
    \\begin{table}[H]
    \\caption{EP. """ + title + """}
    \\vspace{1mm}
    \\centering
    \\begin{scriptsize}
    \\begin{tabularx}{\\textwidth}{l""" + "X"*len(algorithms) + """}
    \\hline
    & \\centering\\arraybackslash """ + " & \\centering\\arraybackslash ".join(algorithms) + " \\\\ \\hline\n"

    # Identify the pivot algorithm, which is the algorithm to compare others against
    pivot_algorithm = df_og.iloc[-1]["Algorithm"]
    
    # Iterate through each row of df1 and df2, representing different problems or comparisons
    for (idx1, row1), (_, row2) in zip(df1.iterrows(), df2.iterrows()):
        # Combine the median and standard deviation values from df1 and df2 into a single DataFrame for sorting
        data = pd.DataFrame({title: row1, 'std_dev': row2})
        # Problem name or identifier
        problem_wilconxon = idx1
    
        # Sort data by median score (descending) and by standard deviation (ascending) to identify best scores
        sorted_data = data.sort_values(by=[title, 'std_dev'], ascending=[False, True])

        # Extract the indices of the highest and second-highest scores based on the sorting
        max_idx, second_idx = sorted_data.index[0], sorted_data.index[1]
    
        # Initialize the row of LaTeX table content with the problem name
        row_data = f"{idx1} & "

        # Loop through each algorithm's score pair (from df1 and df2) to populate the table
        for (index1, score1), (_, score2) in zip(row1.items(), row2.items()):
            # Initialize the result of the Wilcoxon test (empty initially)
            wilconson_result = ""  

            # Skip the pivot algorithm itself, which is not compared with itself
            if not index1 == pivot_algorithm:
                # Filter the original dataframe for the relevant pair of algorithms and the current problem
                algorithms_wilconxon = [pivot_algorithm, index1]
                dg_og_filtered = df_og[(df_og["Algorithm"].isin(algorithms_wilconxon)) & (df_og["Problem"] == problem_wilconxon)]
                df_wilconxon = dg_og_filtered.pivot(index="Id", columns="Algorithm", values="MetricValue").reset_index()
                df_wilconxon = df_wilconxon.drop(columns="Id")
                df_wilconxon.columns = ["Algorithm A", "Algorithm B"]

                # Perform the Wilcoxon signed-rank test and store the result
                try:
                    wilconson_result = wilcoxon_test(df_wilconxon)
                except:
                    print("Wilconson test failed: your dataset either does not contain enough data or the variaty of the data is too low.")
                    return ""
            
            # Format and highlight the maximum and second highest values with gray background
            if index1 == max_idx:
                row_data += f"\\cellcolor{{gray95}}${wilconson_result} {score1:.2f}_{{ {score2:.2f} }}$ & "
            elif index1 == second_idx:
                row_data += f"\\cellcolor{{gray25}}${wilconson_result} {score1:.2f}_{{ {score2:.2f} }}$ & "
            else:
                row_data += f"${wilconson_result} {score1:.2f}_{{ {score2:.2f} }}$ & "

        # Remove the last unnecessary "&" and append the row to the LaTeX document
        latex_doc += row_data.rstrip(" & ") + " \\\\ \n"

    # Close the table structure in the LaTeX document
    latex_doc += """
    \\hline
    \\end{tabularx}
    \\end{scriptsize}
    \\end{table}
    """

    # Return the final LaTeX code for the table
    return latex_doc

def create_tables_latex(csv_path: str) -> None:
    """
    Generates a LaTeX document that compares various algorithms based on statistical metrics 
    (median, standard deviation, interquartile range, and mean) derived from a CSV file.

    This function processes the provided CSV file to compute statistical measures (mean, median, 
    standard deviation, and interquartile range) for each algorithm. It then constructs a LaTeX document 
    that includes tables displaying these statistics for the algorithms in a structured format.

    The LaTeX document is saved to the file "outputs/tables.tex".

    Parameters:
    ----------
    csv_path : str
        The path to the CSV file containing the algorithm data. The file should have algorithms as 
        columns and their corresponding data values as rows.

    Returns:
    -------
    None
        This function does not return anything. It generates a LaTeX document and saves it to the 
        specified location.

    Notes:
    -----
    - The `process_csv_extended` function processes the CSV data and returns DataFrames with necessary 
      statistics (median, mean, and standard deviation).
    - The `create_base_table` and `create_wilconxon_table` functions are assumed to format the DataFrames 
      into LaTeX-compatible tables for inclusion in the document.
    
    Example:
    --------
    create_tables_latex("data/comparison.csv")
    """

    # Step 1: Process the CSV data to compute mean/median and standard deviation (std)
    df1, df2, name = process_csv_extended(csv_path, extra=True)
    df_og = process_csv_basic(csv_path)

    # Step 2: Extract the list of algorithms from the columns of the mean/median dataframe
    algorithms = df1.columns.tolist()

    # Step 3: Initialize the LaTeX document content
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
    
    # Step 4: Add tables to the document using the different dataframes
    latex_doc += create_base_table(name + " and Standard Deviation", df1, df2, algorithms) 
    latex_doc += create_wilconxon_table(name + " and Standard Deviation (Wilconxon)", df_og, df1, df2, algorithms)

    # Step 5: Close the LaTeX document structure
    latex_doc += """
    \\end{document}
    """

    # Step 6: Save the LaTeX document to a file
    if not os.path.exists("outputs/tables"):
        os.makedirs("outputs/tables")
    with open(f"outputs/tables/{name}&std_table.tex", "w") as f:
        f.write(latex_doc)
