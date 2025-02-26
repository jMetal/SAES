LaTeX Report
======================

Another feauture of the library is the ability to generate LaTeX reports of the results of the experiments using different statistical tests. The following code snippet demonstrates how to generate LaTex reports from the results of the experiments for the chosen metric:

.. code-block:: python

    from SAES.latex_generation.stats_table import MeanMedian
    from SAES.latex_generation.stats_table import Friedman
    from SAES.latex_generation.stats_table import WilcoxonPivot
    from SAES.latex_generation.stats_table import Wilcoxon

    # Parameters for the analysis
    data = "swarmIntelligence.csv"
    metrics = "multiobjectiveMetrics.csv"
    metric = "HV"
    output_path = "./output/"

    # Create the LaTeX tables
    mean_median = MeanMedian(experimentData, metrics, metric)
    friedman = Friedman(experimentData, metrics, metric)
    wilcoxon_pivot = WilcoxonPivot(experimentData, metrics, metric)
    wilcoxon = Wilcoxon(experimentData, metrics, metric)

    # Save the LaTeX tables on disk
    mean_median.save(output_path)
    friedman.save(output_path)
    wilcoxon_pivot.save(output_path)
    wilcoxon.save(output_path)

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
