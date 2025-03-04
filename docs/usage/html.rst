HTML Module 
=====================
`SAES` has also the capability to generate HTML reports for the results of the experiments. The HTML reports are generated for a specific metric and depending
and you can choose whether to add the fronts (in 2D, 3D, or higher dimensions) or not. The following code snippet demonstrates how to generate a critical distance diagram of the results of the experiments for a selected metric:

.. code-block:: python

    # from SAES.html.html_generator import notebook_no_fronts
    # from SAES.html.html_generator import notebook_fronts2D
    from SAES.html.html_generator import notebook_fronts3D 
    # from SAES.html.html_generator import notebook_frontsND

    # Load the data and metrics from the CSV files
    data = "swarmIntelligence.csv"
    metrics = "multiobjectiveMetrics.csv"
    metric = "HV"
    fronts = "fronts.csv"
    references = "references.csv"
    # dimensions = 3
    output_path = os.getcwd()

    # Save the HTML report on disk instead of displaying it
    notebook_fronts3D(data, metrics, metric, fronts, references, output_path)

The above code snippet generates the HTML report for the experimental results of all problems based on the selected metric "NHV." The HTML report is saved as a HTML file in the seletec directory.
