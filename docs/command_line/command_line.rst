SAES CL Feature
==========================

SAES provides a command-line interface (CLI) to facilitate the statistical analysis of empirical studies directly from the terminal. This document outlines the available commands, arguments, and usage examples.

.. contents:: 
   :local:
   :depth: 2

**Usage**
---------

To execute SAES from the command line, use the following structure:

.. code-block:: bash

    python -m SAES [OPTIONS] -ds="<DATASET_PATH>" -ms="<METRICS_PATH>"

**Required Arguments**
----------------------

- ``-ds``: Path to the dataset CSV file.
- ``-ms``: Path to the metrics CSV file.

**Main Options**
----------------

Only one of the following mutually exclusive options can be used at a time:

- ``-ls``: Generate a LaTeX skeleton for the paper.
- ``-bp``: Generate a boxplot for the paper.
- ``-cdp``: Generate a critical distance plot for the paper.
- ``-all``: Generate all plots and reports from the dataset.

**Optional Arguments**
----------------------

- ``-m``: Specify the metric to be used to generate the results. Applicable to all features.
- ``-i``: Specify the instance to be used for generating the results. Only applicable to ``-bp``.
- ``-s``: Specify the type of LaTeX report to generate. Only applicable to ``-ls``.
- ``-op``: Specify the output path for the generated files. Applicable to all features.
- ``-g``: Generate all boxplots for a specific metric in grid format. Only applicable to ``-bp``.

**Examples**
------------

1. **Generate a LaTeX Skeleton**

.. code-block:: bash

    python -m SAES -ls -ds="dataset.csv" -ms="metrics.csv" -m="accuracy" -s="friedman" -op="./output/"

This will generate a detailed LaTeX report for the metric "accuracy" and save it to the specified output directory.

2. **Generate Boxplots**

   a. **For All Instances of a Specific Metric:**

   .. code-block:: bash

       python -m SAES -bp -ds="dataset.csv" -ms="metrics.csv" -m="accuracy" -op="./output/"

   b. **For a Specific Instance and Metric:**

   .. code-block:: bash

       python -m SAES -bp -ds="dataset.csv" -ms="metrics.csv" -m="accuracy" -i="instance_1" -op="./output/"

   c. **In Grid Format:**

   .. code-block:: bash

       python -m SAES -bp -ds="dataset.csv" -ms="metrics.csv" -m="accuracy" -g -op="./output/"

3. **Generate Critical Distance Plots**

   a. **For a Specific Metric:**

   .. code-block:: bash

       python -m SAES -cdp -ds="dataset.csv" -ms="metrics.csv" -m="accuracy" -op="./output/"

   b. **For All Metrics:**

   .. code-block:: bash

       python -m SAES -cdp -ds="dataset.csv" -ms="metrics.csv" -op="./output/"

4. **Generate All Outputs**

.. code-block:: bash

    python -m SAES -all -ds="dataset.csv" -ms="metrics.csv" -op="./output/"

This will generate all plots (boxplots, critical distance plots) and LaTeX reports for all metrics in the dataset.

**Error Handling**
------------------

- If you specify ``-i`` without ``-m``, an error will occur:

  .. code-block:: bash

      error: The argument '-i/--instance' requires '-m/--metric' to be specified.

- Ensure that the dataset and metrics file paths are valid and accessible.

**Notes**
---------

- The CLI interface is case-sensitive.
- Output files will be saved to the directory specified with ``-op``. If no directory is provided, the current working directory will be used by default.
