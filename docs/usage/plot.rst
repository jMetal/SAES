Example Boxplot
===============

.. contents:: Table of Contents
   :depth: 2
   :local:

The first feauture of the library is the ability to generate boxplots of the results of the experiments. The following code snippet demonstrates how to generate a boxplot of the results of the experiments:

.. code-block:: python

    import pandas as pd
    from SAES.plots.boxplot import boxplot_instance_metric

    # Load the data and metrics from the CSV files
    data = pd.read_csv('swarmIntelligence.csv')
    metrics = pd.read_csv('metrics.csv')

    # Choose the metric to generate the boxplot
    metric = 'NHV'

    # Name of the instance to generate the boxplot
    instance_name = 'WFG9'

    # Show the boxplot instead of saving it on disk
    boxplot_instance_metric(data, metrics, metric, instance_name, show=True)

or 

.. code-block:: python

    from SAES.plots.boxplot import boxplot_instance_metric

    # Path to the CSV file containing the benchmarking data.
    data = 'swarmIntelligence.csv'
    metrics = 'metrics.csv'

    # Choose the metric to generate the boxplot
    metric = 'NHV'

    # Name of the instance to generate the boxplot
    instance_name = 'WFG9'
    
    # Show the boxplot instead of saving it on disk
    boxplot_instance_metric(data, metrics, metric, instance_name, show=True)

The above code snippet generates a boxplot for the experimental results of the selected problem "WFG9" and the selected metric "NHV." The is not saved in disk and it is just displayed because of the "show" flag value used. The boxplot should look something similar to this:

.. image:: WFG9.png
   :alt: NHV boxplot
   :width: 100%
   :align: center
