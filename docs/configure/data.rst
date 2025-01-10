data.csv
--------
`data.csv` is a CSV file containing the results of the experiments. Each row in the file represents the performance of an algorithm on a specific problem. SAES assumes that the results of comparative study between a number of algorithms is provided in a CSV file with this scheme:

- **Algorithm** (string):  Algorithm name.
- **Instance** (string): Instance name. 
- **MetricName** (string): Name of the quality metric used to evaluate the algorithm performace on the instance. 
- **ExecutionId** (integer): Unique identifier for each algorithm run .
- **MetricValue** (double): Value of the metric corresponding to the run. 

.. csv-table:: 
   :header: "Algorithm", "Instance", "MetricName", "ExecutionId", "MetricValue"

   "Algorithm1", "InstanceA", "Acc", "1", "0.85"
   "Algorithm3", "InstanceA", "Acc", "3", "0.78"
   "Algorithm2", "InstanceA", "Acc", "5", "0.91"
   "Algorithm1", "InstanceA", "Acc", "7", "0.67"
   "...", "...", "...", "...", "..."
   "Algorithm2", "InstanceB", "Loss", "2", "0.12"
   "Algorithm1", "InstanceB", "Loss", "4", "0.23"
   "Algorithm3", "InstanceB", "Loss", "6", "0.15"
   "Algorithm2", "InstanceB", "Loss", "8", "0.34"
    "...", "...", "...", "...", "..."