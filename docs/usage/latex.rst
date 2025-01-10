Example LaTeX document
======================

Single LaTeX report 
-------------------

Another feauture of the library is the ability to generate LaTeX reports of the results of the experiments using different statistical tests. The following code snippet demonstrates how to generate LaTex reports from the results of the experiments for the chosen metric:

.. code-block:: python

    import pandas as pd
    from SAES.latex_generation.latex_skeleton import create_tables_latex_metric

    # Load the data and metrics from the CSV files
    data = pd.read_csv('data.csv')
    metrics = pd.read_csv('metrics.csv')

    # Choose the metric to generate the boxplot
    metric = 'NHV'

    create_tables_latex_metric(data, metric, metric)

or

.. code-block:: python

    from SAES.latex_generation.latex_skeleton import create_tables_latex_metric

    # Path to the CSV file containing the benchmarking data.
    data = 'data.csv'
    metrics = 'metrics.csv'

    # Choose the metric to generate the boxplot
    metric = 'NHV'
    
    create_tables_latex_metrics(data, metric, metric)

The above code snippet generates all the LaTeX reports of the results of the experiments as for the selected metric. The report can be saved as a PDF file in the current working directory and it will looks something like this:

+------------------------+------------------------+
| .. image:: latex1.png  | .. image:: latex2.png  |
|    :width: 600px       |    :width: 600px       |
|    :alt: Image 1       |    :alt: Image 2       |
|                        |                        |
+------------------------+------------------------+
| .. image:: latex3.png  | .. image:: latex4.png  |
|    :width: 600px       |    :width: 600px       |
|    :alt: Image 3       |    :alt: Image 4       |
|                        |                        |
+------------------------+------------------------+

Full LaTeX report generation
----------------------------

If you prefer the library to generate all the LaTeX reports for all the metrics in the data, you can use the following code snippet:

.. code-block:: python

    import pandas as pd
    from SAES.latex_generation.latex_skeleton import create_tables_latex

    # Load the data and metrics from the CSV files
    data = pd.read_csv('data.csv')
    metrics = pd.read_csv('metrics.csv')

    create_tables_latex(data, metrics)

or

.. code-block:: python

    from SAES.latex_generation.latex_skeleton import create_tables_latex

    # Path to the CSV file containing the benchmarking data.
    data = 'data.csv'
    metrics = 'metrics.csv'
    
    create_tables_latex(data, metrics)

The reports are saved as .tex files in the current working directory in a folder called "tables". For each different metric, all its reports will be saved in a subfolder with the name of the metric.