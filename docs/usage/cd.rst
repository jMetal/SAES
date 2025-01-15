Example Critical Distance Graph
=================================

The last feauture of the library is the ability to generate critical distance graphs of the results of the experiments. The following code snippet demonstrates how to generate a critical distance diagram of the results of the experiments for a selected metric:

.. code-block:: python

    import pandas as pd
    from SAES.plots.critical_distance_plot import CDplot_metric

    # Load the data and metrics from the CSV files
    data = pd.read_csv('data.csv')
    metrics = pd.read_csv('metrics.csv')

    # Choose the metric to generate the boxplot
    metric = 'NHV'

    # Save the critical distance plot on disk instead of displaying it
    output_dir = CDplot_metric(data, metrics, metric, show=False)

or

.. code-block:: python

    from SAES.plots.critical_distance_plot import CDplot_metric

    # Path to the CSV file containing the benchmarking data.
    data = 'data.csv'
    metrics = 'metrics.csv'

    # Choose the metric to generate the boxplot
    metric = 'NHV'
    
    # Save the critical distance plot on disk instead of displaying it
    output_dir = CDplot_metric(data, metrics, metric, show=False)

The above code snippet generates a critical distance diagram for the experimental results of all problems based on the selected metric "NHV." The critical distance diagram is saved as a PNG file in the current working directory because of the "show" flag value selected, and it will look similar to this:

.. image:: NHV_cd_plot.png
   :alt: CD diagram
   :width: 100%
   :align: center
