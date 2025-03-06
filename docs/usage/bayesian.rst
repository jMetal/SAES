Bayesian Pplot
===============

.. contents:: Table of Contents
   :depth: 2
   :local:

This module provides the functionality to generate a posterior plot for the Bayesian optimization results. The following code snippet demonstrates how to generate a posterior plot of the results of the experiments:

.. code-block:: python
    
    from SAES.plots.Pplot import Pplot

    # Load the data and metrics from the CSV files
    data = "swarmIntelligence.csv"
    metrics = "multiobjectiveMetrics.csv"

    # Show the boxplot instead of saving it on disk
    pplot = Pplot(experimentData, metrics, "NHV")
    boxplot.show("NSGAII", "AutoMOPSORE")

The above code snippet generates a bayesian Pplot comparing experimental results of the `NSGAII` and `AutoMOPSORE` algorithms for the metric `NHV`. The following image shows the generated Pplot:

.. image:: bayesian.png
   :alt: NHV boxplot
   :width: 100%
   :align: center
