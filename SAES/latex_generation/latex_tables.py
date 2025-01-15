from SAES.statistical_tests.non_parametrical import wilcoxon_test
from SAES.statistical_tests.non_parametrical import friedman_test
import pandas as pd

def median_table(title: str, df_og: pd.DataFrame, df1: pd.DataFrame, df2: pd.DataFrame) -> str:
    """
    Generates a LaTeX table with performance statistics for algorithms across different instances.

    Args:
        title (str): 
            The title for the table.
        
        df_og (pd.DataFrame): 
            Original DataFrame containing the algorithms and instances.
        
        df1 (pd.DataFrame): 
            DataFrame with median values for each algorithm and instance.
        
        df2 (pd.DataFrame): 
            DataFrame with standard deviation values for each algorithm and instance.

    Returns:
        str: LaTeX formatted table as a string.
    """

    # Extract the list of algorithms and instances from the DataFrame
    algorithms = df_og["Algorithm"].unique().tolist()
    instances = df_og["Instance"].unique().tolist()

    # Initialize the LaTeX document with the table structure and formatting
    latex_doc = """
    \\begin{table}[H]
    \\caption{EP. """ + title + """}
    \\vspace{1mm}
    \\centering
    \\begin{scriptsize}
    \\begin{tabular}{l|""" + """c|""" * (len(algorithms)-1) + """c}
    \\hline
    & """ + " & ".join(algorithms) + " \\\\ \\hline\n"

    # Loop through each instance to generate rows of the table
    for instance in instances:
        # Start the row with the instance name
        row_data = f"{instance} & "

        # Obtain the median and standard deviation for each algorithm for the current instance
        median = df1.loc[instance]
        std_dev = df2.loc[instance]

        # Normalize the median by standard deviation
        df_global = median/std_dev

        # Algorithm with the highest and second highest normalized value
        max_idx = df_global.idxmax()
        second_idx = df_global.drop(max_idx).idxmax()

        # Iterate over each algorithm to compute Wilcoxon test and populate the table
        for algorithm in algorithms:
            # Format the median and standard deviation values for the LaTeX table
            score1 = median[algorithm]
            score2 = std_dev[algorithm]

            # Apply conditional formatting for the highest and second highest algorithms
            if algorithm == max_idx:
                row_data += f"\\cellcolor{{gray95}}${score1:.2f}_{{ {score2:.2f} }}$ & "
            elif algorithm == second_idx:
                row_data += f"\\cellcolor{{gray25}}${score1:.2f}_{{ {score2:.2f} }}$ & "
            else:
                row_data += f"${score1:.2f}_{{ {score2:.2f} }}$ & "

        # Add the formatted row to the LaTeX document
        latex_doc += row_data.rstrip(" & ") + " \\\\ \n"
    
    # Close the table structure
    latex_doc += """
    \\hline
    \\end{tabular}
    \\end{scriptsize}
    \\vspace{2mm}
    \\small
    """
        
    latex_doc += """
    \\end{table}
    """

    # Return the final LaTeX code for the table
    return latex_doc

def friedman_table(title: str, df_og: pd.DataFrame, df1: pd.DataFrame, df2: pd.DataFrame, maximize: bool) -> str:
    """
    Generates a LaTeX table with performance statistics for algorithms across instances, including a Friedman test 
    for statistical significance between algorithms.

    Args:
        title (str): 
            The title for the table.
        
        df_og (pd.DataFrame): 
            Original DataFrame containing the algorithms and instances.
        
        df1 (pd.DataFrame): 
            DataFrame with median values for each algorithm and instance.
        
        df2 (pd.DataFrame): 
            DataFrame with standard deviation values for each algorithm and instance.
        
        maximize (bool): 
            Whether to maximize the metric for the Friedman test.

    Returns:
        str: LaTeX formatted table as a string.
    """
    
    # Extract the list of algorithms and instances from the DataFrame
    algorithms = df_og["Algorithm"].unique().tolist()
    instances = df_og["Instance"].unique().tolist()

    # Define display names for algorithms (e.g., Algorithm A, Algorithm B)
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
    & """ + " & ".join(algorithms) + " & FT \\\\ \\hline\n"

    # Loop through each instance to generate rows of the table
    for instance in instances:
        # Start the row with the instance name
        row_data = f"{instance} & "
        instance_friedman = instance

        # Obtain the median and standard deviation for each algorithm for the current instance
        median = df1.loc[instance]
        std_dev = df2.loc[instance]

        # Normalize the median by standard deviation
        df_global = median/std_dev

        # Algorithm with the highest and second highest normalized value
        max_idx = df_global.idxmax()
        second_idx = df_global.drop(max_idx).idxmax()

        # Iterate over each algorithm to compute Friedman test and populate the table
        for algorithm in algorithms:

            # Format the median and standard deviation values for the LaTeX table
            score1 = median[algorithm]
            score2 = std_dev[algorithm]

            # Apply conditional formatting for the highest and second highest algorithms
            if algorithm == max_idx:
                row_data += f"\\cellcolor{{gray95}}${score1:.2f}_{{ {score2:.2f} }}$ & "
            elif algorithm == second_idx:
                row_data += f"\\cellcolor{{gray25}}${score1:.2f}_{{ {score2:.2f} }}$ & "
            else:
                row_data += f"${score1:.2f}_{{ {score2:.2f} }}$ & "

            if algorithm == algorithms[-1]:

                # Perform friedman test between the pivot algorithm and the current algorithm
                algorithms_friedman = algorithms
                dg_og_filtered = df_og[(df_og["Algorithm"].isin(algorithms_friedman)) & (df_og["Instance"] == instance_friedman)]
                df_friedman = dg_og_filtered.pivot(index="ExecutionId", columns="Algorithm", values="MetricValue").reset_index()
                df_friedman = df_friedman.drop(columns="ExecutionId")
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

        # Add the formatted row to the LaTeX document
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
        
    latex_doc += f"\\item \\texttt{{+ implies that the difference between the algorithms for the instance in the select row is significant}}\n"
        
    latex_doc += """
    \\end{itemize}
    \\end{table}
    """

    # Return the final LaTeX code for the table
    return latex_doc

def wilcoxon_table(title: str, df_og: pd.DataFrame) -> str:
    """
    Creates a LaTeX table for Wilcoxon test results between algorithms (each one against each other one in pairs).

    Args:
        title (str): 
            Title of the table.

        df_og (pd.DataFrame):
            DataFrame containing columns 'Algorithm', 'Instance', and 'MetricValue'.

    Returns:
        str: LaTeX-formatted table string.
    """ 

    # Extract the list of algorithms and instances from the columns of the DataFrame
    algorithms = df_og["Algorithm"].unique().tolist()
    instances = df_og["Instance"].unique().tolist()

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
    & """ + " & ".join(algorithms[1:]) + " \\\\ \\hline\n"

    # Generate comparisons and populate table
    compared_pairs = set()

    for algorithm1, _ in zip(algorithms, names):
        if algorithm1 == algorithms[-1]:
            continue
        latex_doc += algorithm1 + " & "
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
                for instance in instances:
                    # Filter the original dataframe for the relevant pair of algorithms and the current instance
                    algorithms_wilcoxon = [algorithm1, algorithm2]
                    dg_og_filtered = df_og[(df_og["Algorithm"].isin(algorithms_wilcoxon)) & (df_og["Instance"] == instance)]
                    df_wilcoxon = dg_og_filtered.pivot(index="ExecutionId", columns="Algorithm", values="MetricValue").reset_index()
                    df_wilcoxon = df_wilcoxon.drop(columns="ExecutionId")
                    og_columns = df_wilcoxon.columns.tolist()
                    df_wilcoxon.columns = ["Algorithm A", "Algorithm B"]

                    # Perform the Wilcoxon signed-rank test and store the result
                    wilconson_result = wilcoxon_test(df_wilcoxon)
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
    \\end{tabular}
    \\end{scriptsize}
    \\vspace{2mm}
    \\small
    \\begin{itemize}
    """

    latex_doc += f"\\item \\texttt{{Instances (in order)}} : {instances}\n"
    latex_doc += f"\\item \\texttt{{Algorithm (row) vs Algorithm (column) = + implies Algorithm (row) better than Algorithm (column)}}\n"

    latex_doc += """
    \\end{itemize}
    \\end{table}
    """

    # Return the final LaTeX code for the table
    return latex_doc

def wilcoxon_pivot_table(title: str, df_og: pd.DataFrame, df1: pd.DataFrame, df2: pd.DataFrame) -> str:
    """
    Generates a LaTeX table comparing the performance of algorithms using the Wilcoxon signed-rank test.
    The table includes the median, standard deviation, and the result of the Wilcoxon test for each algorithm 
    across different instances.

    Args:
        title (str): 
            The title to be displayed in the LaTeX table caption.

        df_og (pd.DataFrame): 
            A DataFrame containing the raw data with columns 'Algorithm', 'Instance', 'ExecutionId', and 'MetricValue'.

        df1 (pd.DataFrame): 
            A DataFrame with the median values of each algorithm for each instance.

        df2 (pd.DataFrame): 
            A DataFrame with the standard deviation values of each algorithm for each instance.

    Returns:
        str: The LaTeX code for the table comparing algorithms' performance.
    """

    # Extract the list of algorithms and instances from the DataFrame
    algorithms = df_og["Algorithm"].unique().tolist()
    instances = df_og["Instance"].unique().tolist()

    # Define display names for algorithms (e.g., Algorithm A, Algorithm B)
    names = [f"Algorithm {chr(65 + i)}" for i in range(len(algorithms))]

    # Initialize a dictionary to store the Wilcoxon test results for each algorithm (ranks)
    ranks = {name: [0, 0, 0] for name in names[:-1]}

    # Identify the pivot algorithm (the last algorithm) to compare others against
    pivot_algorithm = df_og.iloc[-1]["Algorithm"]

    # Initialize the LaTeX document with the table structure and formatting
    latex_doc = """
    \\begin{table}[H]
    \\caption{EP. """ + title + """}
    \\vspace{1mm}
    \\centering
    \\begin{scriptsize}
    \\begin{tabular}{l|""" + """c|""" * (len(algorithms)-1) + """c}
    \\hline
    & """ + " & ".join(algorithms) + " \\\\ \\hline\n"

    # Loop through each instance to generate rows of the table
    for instance in instances:
        # Start the row with the instance name
        row_data = f"{instance} & "
        instance_wilcoxon = instance

        # Obtain the median and standard deviation for each algorithm for the current instance
        median = df1.loc[instance]
        std_dev = df2.loc[instance]

        # Normalize the median by standard deviation
        df_global = median/std_dev

        # Algorithm with the highest and second highest normalized value
        max_idx = df_global.idxmax()
        second_idx = df_global.drop(max_idx).idxmax()

        # Iterate over each algorithm to compute Wilcoxon test and populate the table
        for algorithm in algorithms:
            wilconson_result = ""
            if algorithm != pivot_algorithm:

                # Perform Wilcoxon test between the pivot algorithm and the current algorithm
                algorithms_wilcoxon = [pivot_algorithm, algorithm]
                dg_og_filtered = df_og[(df_og["Algorithm"].isin(algorithms_wilcoxon)) & (df_og["Instance"] == instance_wilcoxon)]
                df_wilcoxon = dg_og_filtered.pivot(index="ExecutionId", columns="Algorithm", values="MetricValue").reset_index()
                df_wilcoxon = df_wilcoxon.drop(columns="ExecutionId")
                df_wilcoxon.columns = ["Algorithm A", "Algorithm B"]
                
                try:
                    # Run the Wilcoxon test (defined outside the function)
                    wilconson_result = wilcoxon_test(df_wilcoxon)
                    algorithm_name = names[algorithms.index(algorithm)]

                    # Update ranks based on Wilcoxon test result
                    if wilconson_result == "+":
                        ranks[algorithm_name][0] += 1
                    elif wilconson_result == "-":
                        ranks[algorithm_name][1] += 1
                    else:
                        ranks[algorithm_name][2] += 1
                
                except:
                    print("Wilconson test failed: your dataset either does not contain enough data or the variaty of the data is too low.")
                    return ""
                
            # Format the median and standard deviation values for the LaTeX table
            score1 = median[algorithm]
            score2 = std_dev[algorithm]

            # Apply conditional formatting for the highest and second highest algorithms
            if algorithm == max_idx:
                row_data += f"\\cellcolor{{gray95}}${score1:.2f}_{{ {score2:.2f} }} {wilconson_result} $ & "
            elif algorithm == second_idx:
                row_data += f"\\cellcolor{{gray25}}${score1:.2f}_{{ {score2:.2f} }} {wilconson_result} $ & "
            else:
                row_data += f"${score1:.2f}_{{ {score2:.2f} }} {wilconson_result} $ & "

        # Add the formatted row to the LaTeX document
        latex_doc += row_data.rstrip(" & ") + " \\\\ \n"

    # Add the summary statistics for the Wilcoxon test results at the footer of the table
    latex_doc += """\\hline + / - / ="""
    for name, rank in ranks.items():
        latex_doc += f" & \\textbf{rank[0]} / \\textbf{rank[1]} / \\textbf{rank[2]}"
    
    # Close the table structure
    latex_doc += """
    \\\\
    \\hline
    \\end{tabular}
    \\end{scriptsize}
    \\vspace{2mm}
    \\small
    \\begin{itemize}
    """

    latex_doc += f"\\item \\texttt{{+ implies that the pivot algorithm (last column) was worse than the selected}}\n"

    latex_doc += """
    \\end{itemize}
    \\end{table}
    """

    # Return the final LaTeX code for the table
    return latex_doc
