Example boxplot
===============

.. contents:: Table of Contents
   :depth: 2
   :local:

Single Boxplot 
--------------

The first feauture of the library is the ability to generate boxplots of the results of the experiments. The following code snippet demonstrates how to generate a boxplot of the results of the experiments:

.. code-block:: python

    import pandas as pd
    from SAES.plots.boxplot import boxplot_csv_metric

    # Load the data and metrics from the CSV files
    data = pd.read_csv('data.csv')
    metrics = pd.read_csv('metrics.csv')

    # Choose the metric to generate the boxplot
    metric = 'NHV'

    boxplot_csv_metric(data, metrics, metric)

or 

.. code-block:: python

    from SAES.plots.boxplot import boxplot_csv_metric

    # Path to the CSV file containing the benchmarking data.
    data = 'data.csv'
    metrics = 'metrics.csv'

    # Choose the metric to generate the boxplot
    metric = 'NHV'
    
    boxplot_csv_metric(data, metrics, metric)

The above code snippet generates boxplots for the experimental results of all problems based on the selected metric "NHV." The boxplots are saved as PNG files in the current working directory, and each of them will look similar to this:

.. image:: WFG9.png
   :alt: NHV boxplot
   :width: 100%
   :align: center

Full Boxplot generation
-----------------------

If you prefer the library to generate all the boxplots for all the metrics in the data, you can use the following code snippet:

.. code-block:: python

    import pandas as pd
    from SAES.plots.boxplot import boxplots_csv

    # Load the data and metrics from the CSV files
    data = pd.read_csv('data.csv')
    metrics = pd.read_csv('metrics.csv')
    
    boxplots_csv(data, metrics)

or

.. code-block:: python

    from SAES.plots.boxplot import boxplots_csv

    # Path to the CSV file containing the benchmarking data.
    data = "data.csv"
    metrics = "metrics.csv"
    
    boxplots_csv(data, metrics)

The boxplots are saved as PNG files in the current working directory in a folder called "boxplots". For each different metric, all its boxplots will be saved in a subfolder with the name of the metric.