from csv_processor import process_csv
import pandas as pd
import os

def create_table(title: str, df1: pd.DataFrame, df2: pd.DataFrame, algorithms: list) -> str:
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

    # Iterate through each row of df1 and df2 to compare their values
    for (idx1, row1), (_, row2) in zip(df1.iterrows(), df2.iterrows()):
        # Create a DataFrame to manage the median and standard deviation together
        data = pd.DataFrame({'median': row1, 'std_dev': row2})

        # Sort primarily by median (descending) and secondarily by std_dev (ascending)
        sorted_data = data.sort_values(by=['median', 'std_dev'], ascending=[False, True])

        # Extract the top two indices
        max_idx, second_idx = sorted_data.index[0], sorted_data.index[1]
    
        # Build the row data for the LaTeX table
        row_data = f"{idx1} & "
        for (index1, score1), (_, score2) in zip(row1.items(), row2.items()):
            # Format and highlight the maximum and second highest values
            if index1 == max_idx:
                row_data += f"\\cellcolor{{gray95}}${score1:.2f}_{{ {score2:.2f} }}$ & "
            elif index1 == second_idx:
                row_data += f"\\cellcolor{{gray25}}${score1:.2f}_{{ {score2:.2f} }}$ & "
            else:
                row_data += f"${score1:.2f}_{{ {score2:.2f} }}$ & "

        # Append the formatted row to the LaTeX document
        latex_doc += row_data.rstrip(" & ") + " \\\\ \n"

    # Close the table structure in the LaTeX document
    latex_doc += """
    \\hline
    \\end{tabularx}
    \\end{scriptsize}
    \\end{table}
    """

    # Return the generated LaTeX code for the table
    return latex_doc

def create_table_latex(csv_path: str) -> None:
    """
    Generates a LaTeX document comparing various algorithms based on statistical metrics 
    (median, standard deviation, interquartile range, and mean) extracted from a CSV file.

    This function processes the provided CSV file to compute the median/meana and standard deviation, 
    for each algorithm. It then generates a LaTeX document that includes tables displaying these statistics 
    for the algorithms.

    The LaTeX document is saved as "outputs/tables.tex".

    Parameters:
    ----------
    csv_path : str
        Path to the CSV file containing the algorithm data. The file should have algorithms as columns 
        and corresponding data values as rows.

    Returns:
    -------
    None
        The function does not return anything. It generates a LaTeX document and saves it to a file.
    
    Notes:
    -----
    - The `process_csv` function is assumed to process the CSV data and return DataFrames containing 
      the necessary statistics (median, standard deviation and mean).
    - The `create_table` function is assumed to be responsible for formatting the DataFrame into LaTeX-compatible 
      tables for inclusion in the document.

    Example:
    --------
    latex_document("data/comparison.csv")
    """

    # Step 1: Process the CSV data to compute mean/median and standard deviation (std)
    df1, df2, name = process_csv(csv_path, extra=True)

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
    
    # Step 4: Add tables to the document using the dataframe
    latex_doc += create_table(name + " and Standard Deviation", df1, df2, algorithms) 

    # Step 5: Close the LaTeX document structure
    latex_doc += """
    \\end{document}
    """

    # Step 6: Save the LaTeX document to a file
    if not os.path.exists("outputs/tables"):
        os.makedirs("outputs/tables")
    with open(f"outputs/tables/{name}&std_table.tex", "w") as f:
        f.write(latex_doc)
