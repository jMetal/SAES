import pandas as pd
from scipy.stats import shapiro

def check_normality(data: pd.DataFrame) -> bool:
    """
    Check the normality of grouped data in a DataFrame using the Shapiro-Wilk test.
    
    This function groups the input data by the "Algorithm" and "Problem" columns, 
    and tests the normality of the "Mark" column within each group. It returns `False` 
    if any group fails the normality test, and `True` otherwise.
    
    :param data: pd.DataFrame
        The input DataFrame containing the data to be tested for normality.
        Must include columns "Algorithm", "Problem", and "Mark".
        
    :return: bool
        `True` if all groups pass the Shapiro-Wilk test for normality, 
        `False` if any group fails.
    """

    # Group the data by Algorithm and Problem
    grouped_data = data.groupby(["Algorithm", "Problem"])

    # Perform the Shapiro-Wilk test for normality for each group
    for _, group in grouped_data:
        marks = group["Mark"]
        if marks.max() == marks.min() or len(marks) < 3: 
            # Identical values imply non-normal distribution
            p_value = 0
        else:
            _, p_value = shapiro(marks)
            
        # If any group fails the normality test
        if p_value <= 0.05:
            print("Found groups with non-normal data.")
            return False
        
    # If all groups pass the normality test
    print("All groups have normal data.")
    return True
