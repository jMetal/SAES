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
- ``-fr``: Generate the Pareto Fronts for the paper.

**Optional Arguments**
----------------------

- ``-pf``: Path to the Pareto Fronts CSV file. Required for ``-fr``.
- ``-r``: Path to the Pareto Fronts references CSV file. Required for ``-fr``.
- ``-m``: Specify the metric to be used to generate the results. Applicable to all features.
- ``-i``: Specify the instance to be used for generating the results. Only applicable to ``-bp`` and ``-fr``.
- ``-s``: Specify the type of LaTeX report to generate. Only applicable to ``-ls``.
  - Options: ``mean_median``, ``friedman``, ``wilcoxon``, ``wilcoxon_pivot``.
- ``-op``: Specify the output path for the generated files. Applicable to all features.
- ``-g``: Generate all boxplots for a specific metric in grid format. Only applicable to ``-bp``.
- ``-d``: Choose the number of dimensions for the Pareto Fronts. Only applicable to ``-fr``.

**Examples**
------------

1. **Generate a LaTeX Skeleton**

.. code-block:: bash

    python -m SAES -ls -ds="dataset.csv" -ms="metrics.csv" -m="accuracy" -s="friedman" -op="./output/"

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

4. **Generate Pareto Fronts**

   a. **For a Specific Metric and Instance in 2D:**

   .. code-block:: bash

       python -m SAES -fr -ds="dataset.csv" -ms="metrics.csv" -pf="pareto.csv" -r="references.csv" -m="accuracy" -i="instance_1" -d="2" -op="./output/"

   b. **For a Specific Metric and Instance in 3D:**

   .. code-block:: bash

       python -m SAES -fr -ds="dataset.csv" -ms="metrics.csv" -pf="pareto.csv" -r="references.csv" -m="accuracy" -i="instance_1" -d="3" -op="./output/"

   c. **For Higher-Dimensional Pareto Fronts:**

   .. code-block:: bash

       python -m SAES -fr -ds="dataset.csv" -ms="metrics.csv" -pf="pareto.csv" -r="references.csv" -m="accuracy" -i="instance_1" -d="4" -op="./output/"

5. **Generate All Outputs**

.. code-block:: bash

    python -m SAES -all -ds="dataset.csv" -ms="metrics.csv" -op="./output/"

This will generate all plots (boxplots, critical distance plots, Pareto fronts) and LaTeX reports for all metrics in the dataset.

**Error Handling**
------------------

- If you specify ``-i`` without ``-m``, an error will occur:

  .. code-block:: bash

      error: The argument '-i/--instance' requires '-m/--metric' to be specified.

- If you specify ``-fr`` without ``-pf`` or ``-r``, an error will occur:

  .. code-block:: bash

      error: The argument '-fr' requires '-pf' and '-r' to be specified.

- Ensure that the dataset, metrics, and Pareto Fronts file paths are valid and accessible.

**Notes**
---------

- The CLI interface is case-sensitive.
- Output files will be saved to the directory specified with ``-op``. If no directory is provided, the current working directory will be used by default.

