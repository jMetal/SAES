Example LaTeX document
======================



The last feauture of the library is the ability to generate LaTeX reports of the results of the experiments using different statistical tests. The following code snippet demonstrates how to generate a LaTeX report of the results of the experiments:

.. code-block:: python

    import pandas as pd
    from algorithm_benchmark_toolkit.latex_generator import create_tables_latex_metrics

    # Load the data from the CSV file
    data = pd.read_csv('data.csv')
    
    # Load the metrics from the CSV file
    metric = pd.read_csv('metrics.csv')

    create_tables_latex_metrics(data, metric)

or

.. code-block:: python

    from algorithm_benchmark_toolkit.latex_generator import create_tables_latex_metrics

    # Path to the CSV file containing the benchmarking data.
    data = "data.csv"
    metric = "metrics.csv"
    
    create_tables_latex_metrics(data, metric)

The above code snippet generates as many LaTeX report of the results of the experiments as metrics there are in the "metrics.csv" file. The report can be saved as a PDF file in the current working directory and it will looks something like this:

+------------------------+------------------------+
| .. image:: latex1.png  | .. image:: latex2.png  |
|    :width: 600px       |    :width: 600px       |
|    :alt: Imagen 1      |    :alt: Imagen 2      |
|                        |                        |
+------------------------+------------------------+
