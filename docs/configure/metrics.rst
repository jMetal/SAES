metrics.csv
-----------
`metrics.csv` is a CSV file containing the configuration for the analysis. Each row in the file represents a metric that will be used to evaluate the algorithms and the Maximize column indicates whether the metric should be maximized or minimized in the statistical analysis. The file must have the following scheme:

- **MetricName** (string): Name of the quality metric used to evaluate the algorithm performace on the instance.
- **Maximize** (boolean): Boolean value to show whether the metric value in that row must be maximized or minimized.

.. csv-table:: 
   :header: "MetricName", "Maximize"

    "Acc", "True"
    "Loss", "False"
