HistoPlot
===============

.. contents:: Table of Contents
   :depth: 2
   :local:

nother feature of the library is the ability to generate histogram plots of the results of the experiments. The following code snippet demonstrates how to generate a histogram plot of the results of the experiments:

.. code-block:: python
    
    from SAES.plots.HistoPlot import HistoPlot

    # Load the data and metrics from the CSV files
    data = "swarmIntelligence.csv"
    metrics = "multiobjectiveMetrics.csv"

    # Show the boxplot instead of saving it on disk
    boxplot = HistoPlot(experimentData, metrics, "HV")
    boxplot.show_instance("ZDT1")

The above code snippet generates a boxplot for the experimental results of the selected problem "ZDT1" and the selected metric "HV." The plot is not saved in disk and it is just displayed because we are using the `show()` function. The boxplot should look something similar to this:

.. image:: histoplot.png
   :alt: NHV boxplot
   :width: 100%
   :align: center
