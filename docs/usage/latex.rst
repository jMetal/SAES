Example LaTeX Report
======================

Another feauture of the library is the ability to generate LaTeX reports of the results of the experiments using different statistical tests. The following code snippet demonstrates how to generate LaTex reports from the results of the experiments for the chosen metric:

.. code-block:: python

    import pandas as pd
    from SAES.latex_generation.latex_skeleton import create_latex

    # Load the data and metrics from the CSV files
    data = pd.read_csv('swarmIntelligence.csv')
    metrics = pd.read_csv('metrics.csv')

    # Choose the metric to generate the boxplot
    metric = 'NHV'

    # Save the latex reports on disk
    output_dir = create_latex(data, metric, metric)

or

.. code-block:: python

    from SAES.latex_generation.latex_skeleton import create_latex

    # Path to the CSV file containing the benchmarking data.
    data = 'swarmIntelligence.csv'
    metrics = 'metrics.csv'

    # Choose the metric to generate the boxplot
    metric = 'NHV'
    
    # Save the latex reports on disk
    output_dir = create_latex(data, metrics, metric)

The above code snippet generates all the 4 LaTeX reports of the results of the experiments as for the selected metric. The reports can be saved as a PDF file in the current working directory and it will look something like this:

+-------------------------+--------------------------------+
| .. image:: median.png   | .. image:: friedman.png        | 
|    :width: 600px        |    :width: 600px               |
|    :alt: Image 1        |    :alt: Image 2               |
|                         |                                |
+-------------------------+--------------------------------+
| .. image:: wilcoxon.png | .. image:: wilcoxon_pivot.png  |
|    :width: 600px        |    :width: 600px               |
|    :alt: Image 3        |    :alt: Image 4               |
|                         |                                |
+-------------------------+--------------------------------+
