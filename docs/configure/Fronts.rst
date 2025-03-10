Front Files
===========

The `Saes` library provides a multiobjective module designed for data from multiobjective optimization studies. The data
are composed of the best and median Pareto front approximations found by a set of algorithms when solving a set of problems.
The files containing these data must be stored in a folder tree following this structura:

.. code-block::

    📂 fronts_folder  
    ├── 📂 algorithm-1/            
    │   ├── 📂 instance-1
    |   |    ├── BEST_metric-1_FUN.csv
    |   |    ├── MEDIAN_metric-1_FUN.csv
    |   |    .
    |   |    .
    |   |    ├── BEST_metric-k_FUN.csv
    |   |    ├── MEDIAN_metric-k_FUN.csv
    │   ├── 📂 instance-2
    |   .
    |   .
    |   └── 📂 instance-m
    ├── 📂 algorithm-2/             
    .
    .
    ├── 📂 algorithm-n/               

Structure Details
-----------------

- Each **algorithm** has its own directory inside ``fronts_folder``.  
- Within each algorithm’s folder, **instances** are stored as subdirectories.  
- Each instance contains multiple CSV files representing Pareto fronts, following the format:  
  
  - ``BEST_metric-x_FUN.csv``: The file with the best Pareto front approximation based on metric `x`.
  - ``MEDIAN_metric-x_FUN.csv``: The file with the median Pareto front approximation based on metric `x`.
