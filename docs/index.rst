.. algorithm_benchmark_toolkit documentation master file, created by
   sphinx-quickstart on Thu Nov 28 10:42:21 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SAES
===========================

.. image:: SAES.png
   :alt: CD diagram
   :width: 100%
   :align: center

This is the documentation for the `SAES` python library, which is a Python library designed to analyze and compare the performance of different algorithms across multiple problems automatically. The tool allows you to: 

1. **Seamless CSV data processing**  

   - Import and preprocess experiment results effortlessly.  
   - Handle datasets of varying sizes with ease.  

2. **Statistical analysis**  

   - **Parametric tests**:

     - Normality test
   - **Non-parametric tests**:  

     - Friedman test  
     - Wilcoxon signed-rank test  
   - **Post hoc analysis**:  
   
     - Nemenyi test (critical distance)

3. **Report generation** 

   - Automated LaTeX **Median table** report
   - Automated LaTeX **Median table with Friedman test** report
   - Automated LaTeX **Median table with Wilcoxon pairwise test (pivot-based)** report
   - Automated LaTeX **Pairwise Wilcoxon test table (1-to-1 comparison)** report 

4. **Visualization**  

   - **Boxplot graphs** for algorithm comparison.  
   - **Critical distance plots** for statistical significance.  

This tool is aimed at researchers and developers interested in algorithm benchmarking studies for artificial intelligence, optimization, machine learning, and more.

Context
=======

A stochastic algorithm is an algorithm that incorporates randomness as part of its logic. This randomness leads to variability in outcomes even when applied to the same problem with the same initial conditions. Stochastic algorithms are widely used in various fields, including optimization, machine learning, and simulation, due to their ability to explore larger solution spaces and avoid local optima. Analyzing and comparing stochastic algorithms pose challenges due to their inherent randomness due to the fact that single run does not provide a complete picture of its performance; instead, multiple runs are necessary to capture the distribution of possible outcomes. This variability necessitates a statistical-based methodology based on descriptive (mean, median, standard deviation, ...) and inferential (hypothesis testing) statistics and visualization.

Installation
============

To install the project, you need to clone the repository and install the required dependencies. You will need to have Python 3.10 or higher installed on your system. Before installing the project, we recommend creating a virtual environment to avoid conflicts with other Python projects:

.. code-block:: bash

   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

.. warning:: 
   This project is currently in **BETA VERSION** and still has work in progress. We recommend using it with caution and reporting any issues you encounter to ensure the project's stability and reliability.

Once you have activated the virtual environment, you can install the project and its dependencies using the following command:

.. code-block:: bash

   pip install SAES

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   configure/configuration
   API/api
   usage/usage

