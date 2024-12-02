from csv_processor import process_csv_extended
from csv_processor import process_csv_basic
from stats import wilcoxon_test
import pandas as pd
import os

def create_base_table(title: str, df1: pd.DataFrame, df2: pd.DataFrame) -> str:
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
    - title (str): The title for the LaTeX table.
    - df1 (pandas.DataFrame): The first dataframe containing performance scores for the algorithms.
    - df2 (pandas.DataFrame): The second dataframe containing performance scores for the algorithms.

    Returns:
    - str: A string containing the LaTeX code for the table.
    """

    # Extract the list of algorithms from the columns of the DataFrame
    algorithms = df1.columns.tolist()

    # Define display names for algorithms
    names = [f"Algorithm {chr(65 + i)}" for i in range(len(algorithms))]

    # Initialize the LaTeX table with basic structure, including the table header
    latex_doc = """
    \\begin{table}[H]
    \\caption{EP. """ + title + """}
    \\vspace{1mm}
    \\centering
    \\begin{scriptsize}
    \\begin{tabularx}{\\textwidth}{l|""" + """>{ \\centering\\arraybackslash }X|""" * (len(algorithms)-1) + """>{ \\centering\\arraybackslash }X}
    \\hline
    & \\centering\\arraybackslash """ + " & \\centering\\arraybackslash ".join(names) + " \\\\ \\hline\n"

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
    \\vspace{2mm}
    \\small
    \\begin{itemize}
    """

    # Add each algorithm with its respective change
    for name, algorithm in zip(names, algorithms):
        latex_doc += f"\\item \\texttt{{{name}}} : {algorithm}\n"
        
    latex_doc += """
    \\end{itemize}
    \\end{table}
    """

    # Return the final LaTeX code for the table
    return latex_doc

def create_wilconxon_table(title: str, df_og: pd.DataFrame) -> str:
    """
    Creates a LaTeX table for Wilcoxon test results between algorithms (each one against each other one in pairs).

    Args:
        title (str): Title of the table.
        df_og (pd.DataFrame): DataFrame containing columns 'Algorithm', 'Problem', and 'MetricValue'.

    Returns:
        str: LaTeX-formatted table string.
    """ 

    # Extract the list of algorithms and problems from the columns of the DataFrame
    algorithms = df_og["Algorithm"].unique().tolist()
    problems = df_og["Problem"].unique().tolist()

    # Define display names for algorithms
    names = [f"Algorithm {chr(65 + i)}" for i in range(len(algorithms))]

    # Initialize the LaTeX table with basic structure, including the table header
    latex_doc = """
    \\begin{table}[H]
    \\caption{EP. """ + title + """}
    \\vspace{1mm}
    \\centering
    \\begin{scriptsize}
    \\begin{tabularx}{\\textwidth}{l""" + """>{ \\centering\\arraybackslash }X""" * (len(algorithms)-1) + """>{ \\centering\\arraybackslash }X}
    \\hline
    & \\centering\\arraybackslash """ + " & \\centering\\arraybackslash ".join(names) + " \\\\ \\hline\n"

    # Generate comparisons and populate table
    compared_pairs = set()

    for algorithm1, name in zip(algorithms, names):
        latex_doc += name + " & "
        for algorithm2 in algorithms:
            # Skip self-comparison
            if algorithm1 == algorithm2:
                latex_doc += " & "
                continue
            latex_doc += "\\texttt{"
            pair = tuple(sorted([algorithm1, algorithm2]))
            # Only perform comparison if the pair has not been processed and are different
            if pair not in compared_pairs:
                # Mark the pair as processed
                compared_pairs.add(pair)  
                for problem in problems:
                    # Filter the original dataframe for the relevant pair of algorithms and the current problem
                    algorithms_wilconxon = [algorithm1, algorithm2]
                    dg_og_filtered = df_og[(df_og["Algorithm"].isin(algorithms_wilconxon)) & (df_og["Problem"] == problem)]
                    df_wilconxon = dg_og_filtered.pivot(index="Id", columns="Algorithm", values="MetricValue").reset_index()
                    df_wilconxon = df_wilconxon.drop(columns="Id")
                    og_columns = df_wilconxon.columns.tolist()
                    df_wilconxon.columns = ["Algorithm A", "Algorithm B"]

                    # Perform the Wilcoxon signed-rank test and store the result
                    wilconson_result = wilcoxon_test(df_wilconxon)
                    if wilconson_result == "=":
                        latex_doc += "="
                    else:
                        winner = og_columns[0] if wilconson_result == "+" else og_columns[1]
                        latex_doc += "+" if algorithm1 == winner else "-"
            latex_doc += "} & "
        latex_doc = latex_doc.rstrip(" & ") + " \\\\\n" 

    # Close the table structure in the LaTeX document
    latex_doc += """
    \\hline
    \\end{tabularx}
    \\end{scriptsize}
    \\vspace{2mm}
    \\small
    \\begin{itemize}
    """

    # Add each algorithm with its respective change
    for name, algorithm in zip(names, algorithms):
        latex_doc += f"\\item \\texttt{{{name}}} : {algorithm}\n"

    latex_doc += f"\\item \\texttt{{Problems (in order)}} : {problems}\n"
    latex_doc += f"\\item \\texttt{{Algorithm (row) vs Algorithm (column) = + implies Algorithm (row) better than Algorithm (column)}}\n"

    latex_doc += """
    \\end{itemize}
    \\end{table}
    """

    # Return the final LaTeX code for the table
    return latex_doc

def create_wilconxon_pivot_table(title: str, df_og: pd.DataFrame, df1: pd.DataFrame, df2: pd.DataFrame) -> str:
    """
    Generates a LaTeX table comparing the performance scores of different algorithms based on two dataframes `df1` and `df2`.
    The table highlights the highest and second-highest scores with different background colors and includes statistical results
    from a Wilcoxon signed-rank test for pairwise comparisons.

    Args:
    - title (str): The title for the LaTeX table.
    - df_og (pandas.DataFrame): The original dataframe containing the performance scores of algorithms and metadata needed 
      for statistical comparisons.
    - df1 (pandas.DataFrame): The first dataframe containing performance scores (e.g., medians) for each algorithm.
    - df2 (pandas.DataFrame): The second dataframe containing associated metrics (e.g., standard deviations).
    
    Returns:
    - str: The LaTeX code for the formatted table.

    Notes:
    - The Wilcoxon signed-rank test is performed between each algorithm and a pivot algorithm.
    - The pivot algorithm is identified as the algorithm listed in the last row of `df_og`.
    - Results from the Wilcoxon test are displayed alongside the performance scores in the table.
    - Highlights:
      - The highest score in a row is shaded with a light gray (`gray95`).
      - The second-highest score in a row is shaded with a darker gray (`gray25`).
    - The function assumes that:
      - `df1` and `df2` have the same structure, with rows representing problems and columns representing algorithms.
      - `df_og` contains metadata needed to filter relevant data for each pairwise comparison and perform the Wilcoxon test.

    Raises:
    - An exception is printed if the Wilcoxon test fails due to insufficient or low-variability data.

    Example:
    ```
    title = "Performance Comparison"
    df_og = pd.DataFrame(...)  # Original data with metadata and scores
    df1 = pd.DataFrame(...)    # Median scores
    df2 = pd.DataFrame(...)    # Standard deviations
    latex_table = create_last_wilconxon_table(title, df_og, df1, df2)
    print(latex_table)
    ```
    """
    
    # Extract the list of algorithms from the columns of the DataFrame
    algorithms = df1.columns.tolist()

    # Define display names for algorithms
    names = [f"Algorithm {chr(65 + i)}" for i in range(len(algorithms))]

    # Initialize the LaTeX document with the table structure and formatting
    latex_doc = """
    \\begin{table}[H]
    \\caption{EP. """ + title + """}
    \\vspace{1mm}
    \\centering
    \\begin{scriptsize}
    \\begin{tabularx}{\\textwidth}{l|""" + """>{ \\centering\\arraybackslash }X|""" * (len(algorithms)-1) + """>{ \\centering\\arraybackslash }X}
    \\hline
    & \\centering\\arraybackslash """ + " & \\centering\\arraybackslash ".join(names) + " \\\\ \\hline\n"

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
    \\vspace{2mm}
    \\small
    \\begin{itemize}
    """

    # Add each algorithm with its respective change
    for name, algorithm in zip(names, algorithms):
        latex_doc += f"\\item \\texttt{{{name}}} : {algorithm}\n"

    latex_doc += f"\\item \\texttt{{+ implies that the pivot algorithm (last column) was worse than the selected}}\n"

    latex_doc += """
    \\end{itemize}
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

    # Step 2: Initialize the LaTeX document content
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
    
    # Step 3: Add tables to the document using the different dataframes
    latex_doc += create_base_table(name + " and Standard Deviation", df1, df2) 
    latex_doc += create_wilconxon_pivot_table(name + " and Standard Deviation (Wilconxon Pivot)", df_og, df1, df2)
    latex_doc += create_wilconxon_table("Wilconxon Test 1vs1", df_og)

    # Step 4: Close the LaTeX document structure
    latex_doc += """
    \\end{document}
    """

    # Step 5: Save the LaTeX document to a file
    if not os.path.exists("outputs/tables"):
        os.makedirs("outputs/tables")
    with open(f"outputs/tables/{name}&std_table.tex", "w") as f:
        f.write(latex_doc)
