from csv_processor import process_csv

def create_table(title, df1, df2, algorithms) -> str:
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
    \\label{table: EP_IQR_Median}
    \\centering
    \\begin{scriptsize}
    \\begin{tabularx}{\\textwidth}{l""" + "X"*len(algorithms) + """}
    \\hline
    & \\centering\\arraybackslash """ + " & \\centering\\arraybackslash ".join(algorithms) + " \\\\ \\hline\n"

    # Iterate through each row of df1 and df2 to compare their values
    for (idx1, row1), (_, row2) in zip(df1.iterrows(), df2.iterrows()):
        # Sort row1 to find the maximum and second maximum values
        row1_sorted = row1.sort_values(ascending=False)

        # Determine which columns should be highlighted (max and second max values)
        if row1_sorted.iloc[0] == row1_sorted.iloc[1]:
            if row2[row1_sorted.index[0]] > row2[row1_sorted.index[1]]:
                max_idx, second_idx = row1_sorted.index[0], row1_sorted.index[1]
            else:
                max_idx, second_idx = row1_sorted.index[1], row1_sorted.index[0]
        else:
            max_idx, second_idx = row1_sorted.index[0], row1_sorted.index[1]

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

    This function processes the provided CSV file to compute the median, standard deviation, 
    interquartile range (IQR), and mean for each algorithm. It then generates a LaTeX document 
    that includes tables displaying these statistics for the algorithms, using the following structure:
    - Median and Standard Deviation
    - Median and Interquartile Range
    - Mean and Standard Deviation
    - Mean and Interquartile Range

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
      the necessary statistics (median, standard deviation, IQR, and mean).
    - The `create_table` function is assumed to be responsible for formatting the DataFrame into LaTeX-compatible 
      tables for inclusion in the document.

    Example:
    --------
    latex_document("data/comparison.csv")
    """

    # Step 1: Process the CSV data to compute median, standard deviation (std), and interquartile range (IQR)
    df_median, df_std, df_iqr = process_csv(csv_path, median=True, extra=True)

    # Step 2: Process the CSV data again to compute the mean (without std or IQR)
    df_mean = process_csv(csv_path, median=False, extra=False)[0]

    # Step 3: Extract the list of algorithms from the columns of the median dataframe
    algorithms = df_median.columns.tolist()

    # Step 4: Initialize the LaTeX document content
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
    
    # Step 5: Add tables to the document using different dataframes (median, std, mean, IQR)
    latex_doc += create_table("Median and Standard Deviation", df_median, df_std, algorithms) # Median table with std
    latex_doc += create_table("Median and Interquartile Range", df_median, df_iqr, algorithms) # Median table with IQR
    latex_doc += create_table("Mean and Standard Deviation", df_mean, df_std, algorithms) # Mean table with std
    latex_doc += create_table("Mean and Interquartile Range", df_mean, df_iqr, algorithms) # Mean table with IQR

    # Step 6: Close the LaTeX document structure
    latex_doc += """
    \\end{document}
    """

    # Step 7: Save the LaTeX document to a file
    with open("outputs/tables.tex", "w") as f:
        f.write(latex_doc)
    
# Load CSV data into a pandas DataFrame
file_path = "CSVs/data.csv"

# Check the shape
create_table_latex(file_path)