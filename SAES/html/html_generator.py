import papermill as pm
import subprocess, os

notebooks = f"{os.path.dirname(os.path.abspath(__file__))}/notebooks"

def notebook_no_fronts(data: str,
                       metrics: str, 
                       metric: str,
                       output_path: str) -> None:
    """
    This function creates a notebook that shows the statistical analysis of the data.

    Args:
        data (str):
            The path to the data file.
        
        metrics (str):
            The path to the metrics file.
        
        metric (str):
            The metric to analyze.

        output_path (str):
            The path to save the html.
    
    Returns:
        None

    Example:
        >>> from SAES.html.html_generator import notebook_no_fronts
        >>> import os
        >>> 
        >>> data = "data.csv"
        >>> metrics = "metrics.csv"
        >>> metric = "HV"
        >>> output_path = os.getcwd()
        >>> notebook_no_fronts(data, metrics, metric, output_path)
    """

    # Execute the notebook
    pm.execute_notebook(f"{notebooks}/multiobjective_optimization.ipynb", f"{output_path}/no_fronts.ipynb", 
                        parameters=dict(data=data, 
                                        metrics=metrics, 
                                        metric=metric)
    )

    # Define and execute the command 
    command = ['python', '-m', 'nbconvert', '--to', 'html', '--no-input', f"{output_path}/no_fronts.ipynb"]
    subprocess.run(command, check=True)
    os.remove(f"{output_path}/no_fronts.ipynb")

def notebook_fronts2D(data: str, 
                      metrics: str, 
                      metric: str, 
                      fronts: str, 
                      references: str,
                      output_path: str) -> None:
    """
    This function creates a notebook that shows the statistical analysis of the data.

    Args:
        data (str):
            The path to the data file.
        
        metrics (str):
            The path to the metrics file.
        
        metric (str):
            The metric to analyze.
        
        fronts (str):
            The path to the fronts file.
        
        references (str):
            The path to the references file.

        output_path (str):
            The path to save the html.
    
    Returns:
        None

    Example:
        >>> from SAES.html.html_generator import notebook_fronts2D
        >>> import os
        >>> 
        >>> data = "data.csv"
        >>> metrics = "metrics.csv"
        >>> metric = "HV"
        >>> fronts = "fronts"
        >>> references = "references"
        >>> output_path = os.getcwd()
        >>> notebook_fronts2D(data, metrics, metric, fronts, references, output_path)
    """

    # Execute the notebook
    pm.execute_notebook(f"{notebooks}/multiobjective_fronts2D.ipynb", f"{output_path}/fronts2D.ipynb", 
                        parameters=dict(data=data, 
                                        metrics=metrics, 
                                        metric=metric, 
                                        fronts=fronts, 
                                        references=references)
    )

    # Define and execute the command 
    command = ['python', '-m', 'nbconvert', '--to', 'html', '--no-input', f"{output_path}/fronts2D.ipynb"]
    subprocess.run(command, check=True)
    os.remove(f"{output_path}/fronts2D.ipynb")

def notebook_fronts3D(data: str, 
                      metrics: str, 
                      metric: str, 
                      fronts: str, 
                      references: str,
                      output_path: str) -> None:
    """
    This function creates a notebook that shows the statistical analysis of the data.

    Args:
        data (str):
            The path to the data file.
        
        metrics (str):
            The path to the metrics file.
        
        metric (str):
            The metric to analyze.
        
        fronts (str):
            The path to the fronts file.
        
        references (str):
            The path to the references file.

        output_path (str):
            The path to save the html.
    
    Returns:
        None

    Example:
        >>> from SAES.html.html_generator import notebook_fronts3D
        >>> import os
        >>> 
        >>> data = "data.csv"
        >>> metrics = "metrics.csv"
        >>> metric = "HV"
        >>> fronts = "fronts"
        >>> references = "references"
        >>> output_path = os.getcwd()
        >>> notebook_fronts3D(data, metrics, metric, fronts, references, output_path)
    """

    # Execute the notebook
    pm.execute_notebook(f"{notebooks}/multiobjective_fronts3D.ipynb", f"{output_path}/fronts3D.ipynb", 
                        parameters=dict(data=data, 
                                        metrics=metrics, 
                                        metric=metric, 
                                        fronts=fronts, 
                                        references=references)
    )

    # Define and execute the command 
    command = ['python', '-m', 'nbconvert', '--to', 'html', '--no-input', f"{output_path}/fronts3D.ipynb"]
    subprocess.run(command, check=True)
    os.remove(f"{output_path}/fronts3D.ipynb")

def notebook_frontsND(data: str, 
                      metrics: str, 
                      metric: str, 
                      fronts: str, 
                      references: str,
                      dimensions: int,
                      output_path: str) -> None:
    """
    This function creates a notebook that shows the statistical analysis of the data.

    Args:
        data (str):
            The path to the data file.
        
        metrics (str):
            The path to the metrics file.
        
        metric (str):
            The metric to analyze.
        
        fronts (str):
            The path to the fronts file.
        
        references (str):
            The path to the references file.
        
        dimensions (int):
            The number of dimensions

        output_path (str):
            The path to save the html.
    
    Returns:
        None

    Example:
        >>> from SAES.html.html_generator import notebook_frontsND
        >>> import os
        >>> 
        >>> data = "data.csv"
        >>> metrics = "metrics.csv"
        >>> metric = "HV"
        >>> fronts = "fronts"
        >>> references = "references"
        >>> dimensions = 3
        >>> output_path = os.getcwd()
        >>> notebook_frontsND(data, metrics, metric, fronts, references, dimensions, output_path)
    """

    # Execute the notebook
    pm.execute_notebook(f"{notebooks}/multiobjective_frontsND.ipynb", f"{output_path}/frontsND.ipynb", 
                        parameters=dict(data=data, 
                                        metrics=metrics, 
                                        metric=metric, 
                                        fronts=fronts, 
                                        references=references,
                                        dimensions=dimensions)
    )

    # Define and execute the command 
    command = ['python', '-m', 'nbconvert', '--to', 'html', '--no-input', f"{output_path}/frontsND.ipynb"]
    subprocess.run(command, check=True)
    os.remove(f"{output_path}/frontsND.ipynb")

def notebook_bayesian(data: str, 
                      metrics: str, 
                      metric: str, 
                      pivot: str,
                      output_path: str) -> None:
    """
    This function creates a notebook that shows the statistical analysis of the data.

    Args:
        data (str):
            The path to the data file.
        
        metrics (str):
            The path to the metrics file.
        
        metric (str):
            The metric to analyze.
        
        pivot (str):
            The pivot algorithm to analyze.

        output_path (str):
            The path to save the html.
    
    Returns:
        None

    Example:
        >>> from SAES.html.html_generator import notebook_bayesian
        >>> import os
        >>> 
        >>> data = "data.csv"
        >>> metrics = "metrics.csv"
        >>> metric = "HV"
        >>> pivot = "NSGAII"
        >>> output_path = os.getcwd()
        >>> notebook_bayesian(data, metrics, metric, pivot, output_path)
    """

    # Execute the notebook
    pm.execute_notebook(f"{notebooks}/bayesian_posterior.ipynb", f"{output_path}/bayesian.ipynb", 
                        parameters=dict(data=data, 
                                        metrics=metrics, 
                                        metric=metric, 
                                        pivot=pivot)
    )

    # Define and execute the command 
    command = ['python', '-m', 'nbconvert', '--to', 'html', '--no-input', f"{output_path}/bayesian.ipynb"]
    subprocess.run(command, check=True)
    os.remove(f"{output_path}/bayesian.ipynb")
    