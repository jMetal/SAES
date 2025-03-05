Fronts ND
=========

.. contents:: Table of Contents
   :depth: 2
   :local:

If you are working with data that surpases the 3D dimension (or is exactly 3D), you can visualize the Pareto fronts in ND (Take into account that you need to procide as a parameter the number of objectives). The following code snippet demonstrates how to generate a ND plot of the results of the experiments:

.. code-block:: python
    
    from SAES.multiobjective.pareto_front import FrontND

    # Load the data and metrics from the CSV files
    fronts_path = "fronts"
    references_path = "references"

    # Show the boxplot instead of saving it on disk
    front = FrontND(fronts_path, references_path, metric, dimensions=3)
    boxplot = Boxplot(experimentData, metrics, "NHV")
    front.show("WFG9", median=True)

The above code snippet generates a boxplot for the experimental results of the selected problem "WFG9" and the selected metric "NHV." The plot is not saved in disk and it is just displayed because we are using the `show()` function. The boxplot should look something similar to this:

.. image:: frontnd.png
   :alt: NHV boxplot
   :width: 100%
   :align: center

   
