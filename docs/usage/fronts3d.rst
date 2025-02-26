Fronts 3D
=========

.. contents:: Table of Contents
   :depth: 2
   :local:

If your data allows it, you can visualize the Pareto fronts in 3D. The following code snippet demonstrates how to generate a 3D plot of the results of the experiments:

.. code-block:: python
    
    from SAES.multiobjective.pareto_front import Front3D

    # Load the data and metrics from the CSV files
    fronts_path = "fronts"
    references_path = "references"

    # Show the boxplot instead of saving it on disk
    front = Front3D(fronts_path, references_path, metric)
    boxplot = Boxplot(experimentData, metrics, "NHV")
    front.show("WFG9", median=True)

The above code snippet generates a boxplot for the experimental results of the selected problem "WFG9" and the selected metric "NHV." The plot is not saved in disk and it is just displayed because we are using the `show()` function. The boxplot should look something similar to this:

.. image:: front3d.png
   :alt: NHV boxplot
   :width: 100%
   :align: center
