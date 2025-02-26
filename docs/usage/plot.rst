Boxplot
===============

.. contents:: Table of Contents
   :depth: 2
   :local:

The first feauture of the library is the ability to generate boxplots of the results of the experiments. The following code snippet demonstrates how to generate a boxplot of the results of the experiments:

.. code-block:: python
    
    from SAES.plots.boxplot import Boxplot

    # Load the data and metrics from the CSV files
    data = "swarmIntelligence.csv"
    metrics = "multiobjectiveMetrics.csv"

    # Show the boxplot instead of saving it on disk
    boxplot = Boxplot(experimentData, metrics, "NHV")
    boxplot.show_instance("WFG9")

The above code snippet generates a boxplot for the experimental results of the selected problem "WFG9" and the selected metric "NHV." The plot is not saved in disk and it is just displayed because we are using the `show()` function. The boxplot should look something similar to this:

.. image:: WFG9.png
   :alt: NHV boxplot
   :width: 100%
   :align: center
