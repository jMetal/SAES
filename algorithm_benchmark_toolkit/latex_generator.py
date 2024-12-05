from algorithm_benchmark_toolkit.csv_processor import process_csv_extended
from algorithm_benchmark_toolkit.csv_processor import process_csv_basic
from algorithm_benchmark_toolkit.stats import wilcoxon_test
from algorithm_benchmark_toolkit.stats import friedman_test
import pandas as pd
import os

def __create_base_table(title: str, df1: pd.DataFrame, df2: pd.DataFrame) -> str:
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
    \\begin{tabular}{l|""" + """c|""" * (len(algorithms)-1) + """c}
    \\hline
    & """ + " & ".join(names) + " \\\\ \\hline\n"

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
    \\end{tabular}
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

def __create_friedman_table(title: str, df_og: pd.DataFrame, df1: pd.DataFrame, df2: pd.DataFrame, maximize: bool) -> str:
    """
    Generates a LaTeX formatted table for presenting the results of a Friedman test along with 
    the performance scores of different algorithms for various problems. The table includes 
    median values, standard deviations, and Wilcoxon test results.

    Parameters:
    ----------
    title : str
        The title of the table, typically a description of the experiments or dataset.
    
    df_og : pd.DataFrame
        A DataFrame containing the original data with columns 'Algorithm', 'Problem', 
        and 'MetricValue'. This is used for performing the Friedman test on the data.
        
    df1 : pd.DataFrame
        A DataFrame containing the median values of performance scores for the algorithms, 
        where each row represents a different problem, and the columns correspond to different algorithms.
    
    df2 : pd.DataFrame
        A DataFrame containing the standard deviations for each algorithm's performance 
        scores, where each row corresponds to a different problem, and the columns 
        correspond to the same algorithms.
    maximize : bool
        A boolean indicating whether the metric should be maximized (True) or minimized (False).

    Returns:
    -------
    str
        A LaTeX string representing the formatted table that can be used in a LaTeX document.
        The table displays the performance scores for each algorithm, the Wilcoxon test results, 
        and highlights the best and second-best algorithms in each row.

    Notes:
    -----
    - The LaTeX table generated will display the median scores from `df1` along with the corresponding 
      standard deviations from `df2` for each algorithm.
    - The table also includes a result of a Friedman test to check if there are significant differences 
      between the algorithms for each problem.
    - Algorithms are displayed with labels "Algorithm A", "Algorithm B", etc.
    - For each problem, the best and second-best scores are highlighted with different shades of gray.
    - If the Friedman test shows significant differences (p-value < 0.05), a "+" symbol is added in the 
      table. Otherwise, an "=" symbol is used.
    - This function assumes that the `friedman_test()` function is defined elsewhere in the code and 
      performs the statistical test on the given data.

    Example:
    --------
    title = "Comparison of Algorithms"
    df_og = pd.DataFrame({
        'Algorithm': ['A', 'B', 'C'],
        'Problem': ['Problem 1', 'Problem 1', 'Problem 1'],
        'MetricValue': [0.85, 0.87, 0.90]
    })
    df1 = pd.DataFrame({
        'A': [0.85, 0.88],
        'B': [0.87, 0.89],
        'C': [0.90, 0.91]
    }, index=['Problem 1', 'Problem 2'])
    df2 = pd.DataFrame({
        'A': [0.03, 0.04],
        'B': [0.02, 0.03],
        'C': [0.01, 0.02]
    }, index=['Problem 1', 'Problem 2'])

    latex_table = create_friedman_table(title, df_og, df1, df2)
    print(latex_table)
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
    \\begin{tabular}{l|""" + """c|""" * (len(algorithms)) + """c}
    \\hline
    & """ + " & ".join(names) + " & FT \\\\ \\hline\n"
    
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
            # Format and highlight the maximum and second highest values with gray background
            if index1 == max_idx:
                row_data += f"\\cellcolor{{gray95}}${score1:.2f}_{{ {score2:.2f} }} $ & "
            elif index1 == second_idx:
                row_data += f"\\cellcolor{{gray25}}${score1:.2f}_{{ {score2:.2f} }} $ & "
            else:
                row_data += f"${score1:.2f}_{{ {score2:.2f} }} $ & "

            # Perform the Friedman test for the last algorithm in the list
            if index1 == algorithms[-1]:
                # Filter the original dataframe for the relevant algorithms and the current problem
                algorithms_friedman = algorithms
                dg_og_filtered = df_og[(df_og["Algorithm"].isin(algorithms_friedman)) & (df_og["Problem"] == problem_wilconxon)]
                df_friedman = dg_og_filtered.pivot(index="Id", columns="Algorithm", values="MetricValue").reset_index()
                df_friedman = df_friedman.drop(columns="Id")
                df_friedman.columns = names

                # Perform the Friedman test and store the result
                try:
                    df_friedman_result = friedman_test(df_friedman, maximize)
                    if df_friedman_result["Results"]["p-value"] < 0.05:
                        row_data += "+ & "
                    else:
                        row_data += "= & "
                except:
                    print("Friedman test failed: your dataset either does not contain enough data or the variaty of the data is too low.")
                    return ""

        # Remove the last unnecessary "&" and append the row to the LaTeX document
        latex_doc += row_data.rstrip(" & ") + " \\\\ \n"

    # Close the table structure in the LaTeX document
    latex_doc += """
    \\hline
    \\end{tabular}
    \\end{scriptsize}
    \\vspace{2mm}
    \\small
    \\begin{itemize}
    """

    # Add each algorithm with its respective change
    for name, algorithm in zip(names, algorithms):
        latex_doc += f"\\item \\texttt{{{name}}} : {algorithm}\n"

    latex_doc += f"\\item \\texttt{{+ implies that the difference between the algorithms for the problem in the select row is significant}}\n"
        
    latex_doc += """
    \\end{itemize}
    \\end{table}
    """

    # Return the final LaTeX code for the table
    return latex_doc

def __create_wilconxon_table(title: str, df_og: pd.DataFrame) -> str:
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
    \\begin{tabular}{l|""" + """c|""" * (len(algorithms)-2) + """c}
    \\hline
    & """ + " & ".join(names[1:]) + " \\\\ \\hline\n"

    # Generate comparisons and populate table
    compared_pairs = set()

    for algorithm1, name in zip(algorithms, names):
        if algorithm1 == algorithms[-1]:
            continue
        latex_doc += name + " & "
        for algorithm2 in algorithms:
            if algorithm2 == algorithms[0]:
                continue
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
                        latex_doc += " ="
                    else:
                        winner = og_columns[0] if wilconson_result == "+" else og_columns[1]
                        latex_doc += " +" if algorithm1 == winner else " -"
            latex_doc += "} & "
        latex_doc = latex_doc.rstrip(" & ") + " \\\\\n" 

    # Close the table structure in the LaTeX document
    latex_doc += """
    \\hline
    \\end{tabular}
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

def __create_wilconxon_pivot_table(title: str, df_og: pd.DataFrame, df1: pd.DataFrame, df2: pd.DataFrame) -> str:
    """
    Generates a LaTeX table comparing the performance scores of different algorithms using two dataframes (`df1` and `df2`)
    and performs statistical comparisons via the Wilcoxon signed-rank test.

    Args:
    - title (str): The title for the LaTeX table.
    - df_og (pandas.DataFrame): The original dataframe with metadata and performance scores, needed for statistical comparisons.
    - df1 (pandas.DataFrame): Dataframe containing median performance scores for each algorithm across problems.
    - df2 (pandas.DataFrame): Dataframe containing standard deviations associated with the scores in `df1`.

    Returns:
    - str: The LaTeX code for a formatted table.

    Functionality:
    - The table compares algorithms based on their scores, highlighting the best and second-best performance for each problem.
    - Performs pairwise Wilcoxon signed-rank tests between algorithms and a pivot algorithm (identified as the last row in `df_og`).
    - Statistical results are displayed alongside the performance scores.
    - Highlights:
        - The highest score in a row is shaded light gray (`gray95`).
        - The second-highest score in a row is shaded darker gray (`gray25`).
    - Displays a summary of Wilcoxon test outcomes (`+`, `-`, `=`) in the table footer.

    Notes:
    - Assumes `df1` and `df2` have the same structure (rows for problems, columns for algorithms).
    - Assumes `df_og` contains sufficient metadata for filtering relevant data for Wilcoxon tests.
    - Handles potential issues with the Wilcoxon test gracefully, including low-variability or insufficient data.

    Example:
    ```
    title = "Performance Comparison"
    df_og = pd.DataFrame(...)  # Original data with metadata and scores
    df1 = pd.DataFrame(...)    # Median scores
    df2 = pd.DataFrame(...)    # Standard deviations
    latex_table = create_wilconxon_pivot_table(title, df_og, df1, df2)
    print(latex_table)
    ```

    Raises:
    - Prints an error message if the Wilcoxon test fails due to insufficient or low-variability data.
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
    \\begin{tabular}{l|""" + """c|""" * (len(algorithms)-1) + """c}
    \\hline
    & """ + " & ".join(names) + " \\\\ \\hline\n"

    # Initialize a dictionary to keep track of Wilcoxon test results for each algorithm
    ranks = {name: [0, 0, 0] for name in names[:-1]}

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
                    algorithm_name = names[algorithms.index(index1)]
                    if wilconson_result == "+":
                        ranks[algorithm_name][0] += 1
                    elif wilconson_result == "-":
                        ranks[algorithm_name][1] += 1
                    else:
                        ranks[algorithm_name][2] += 1
                except:
                    print("Wilconson test failed: your dataset either does not contain enough data or the variaty of the data is too low.")
                    return ""
            
            # Format and highlight the maximum and second highest values with gray background
            if index1 == max_idx:
                row_data += f"\\cellcolor{{gray95}}${score1:.2f}_{{ {score2:.2f} }} {wilconson_result} $ & "
            elif index1 == second_idx:
                row_data += f"\\cellcolor{{gray25}}${score1:.2f}_{{ {score2:.2f} }} {wilconson_result} $ & "
            else:
                row_data += f"${score1:.2f}_{{ {score2:.2f} }} {wilconson_result} $ & "

        # Remove the last unnecessary "&" and append the row to the LaTeX document
        latex_doc += row_data.rstrip(" & ") + " \\\\ \n"

    # Add summary statistics to the footer of the table
    latex_doc += """\\hline + / - / ="""
    for name, rank in ranks.items():
        latex_doc += f" & \\textbf{rank[0]} / \\textbf{rank[1]} / \\textbf{rank[2]}"
    
    # Close the table structure in the LaTeX document
    latex_doc += """
    \\\\
    \\hline
    \\end{tabular}
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

def __create_tables_latex(csv: pd.DataFrame, metric: str, maximize: bool) -> None:
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
    metric : str
        The metric to be used for comparison (e.g., accuracy, error rate, F1 score).
    maximize : bool
        A boolean indicating whether the metric should be maximized (True) or minimized (False).

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
    df1, df2, name = process_csv_extended(csv, metric, extra=True)
    df_og = process_csv_basic(csv, metric)

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
    latex_doc += __create_base_table(f"{name} and Standard Deviation ({metric})", df1, df2) 
    latex_doc += __create_friedman_table(f"{name} and Standard Deviation - Friedman Test ({metric})", df_og, df1, df2, maximize)
    latex_doc += __create_wilconxon_pivot_table(f"{name} and Standard Deviation - Wilconxon Pivot ({metric})", df_og, df1, df2)
    latex_doc += __create_wilconxon_table(f"Wilconxon Test 1vs1 ({metric})", df_og)

    # Step 4: Close the LaTeX document structure
    latex_doc += """
    \\end{document}
    """

    # Step 5: Save the LaTeX document to a file
    if not os.path.exists("outputs/tables"):
        os.makedirs("outputs/tables")
    with open(f"outputs/tables/{name}&std_table_{metric}.tex", "w") as f:
        f.write(latex_doc)

def create_tables_latex_metrics(data: str | pd.DataFrame, metrics: str | pd.DataFrame) -> None:
    """
    Generates LaTeX tables based on the provided metrics and data.

    This function processes the given metrics and data (either as file paths or Pandas DataFrames),
    and for each metric, filters the data to match the corresponding metric. Then, it generates a LaTeX 
    table for each metric, using the helper function __create_tables_latex().

    Args:
        data (str | pd.DataFrame): The data to be processed. This can either be a string representing
                                    the file path to a CSV file, or a Pandas DataFrame containing the data.
        metrics (str | pd.DataFrame): The metrics to use for generating the LaTeX tables. This can either
                                      be a string representing the file path to a CSV file, or a Pandas DataFrame 
                                      containing the metrics.

    Returns:
        None: This function does not return any value. It generates LaTeX tables as side effects.

    Example:
        # If `data.csv` contains the data and `metrics.csv` contains the metrics:
        create_tables_latex_metrics("data.csv", "metrics.csv")

        # If both `data` and `metrics` are Pandas DataFrames:
        create_tables_latex_metrics(data_df, metrics_df)
    
    Notes:
        The function assumes that the metrics DataFrame has at least two columns: "Metric" and "Maximize".
        The data is filtered based on the "Metric" column, and LaTeX tables are generated accordingly.
        The descending flag in the metrics is used to indicate whether the metric should be maximized.
    """

    # Load the metrics DataFrame, either from a CSV file or as an existing DataFrame
    df_m = pd.read_csv(metrics, delimiter=",") if isinstance(metrics, str) else metrics

    # Load the data DataFrame, either from a CSV file or as an existing DataFrame
    df = pd.read_csv(data, delimiter=",") if isinstance(data, str) else data

    # Iterate through each row in the metrics DataFrame
    for _, row in df_m.iterrows():
        # Extract the metric name and the 'Maximize' flag (whether to maximize the metric)
        metric = row["Metric"]
        descending = row["Maximize"]

        # Filter the data for the rows where the 'Metric' matches the current metric
        df_n = df[df["Metric"] == metric].reset_index()

        # Call the helper function to create a LaTeX table for the current metric
        __create_tables_latex(df_n, metric, descending)

