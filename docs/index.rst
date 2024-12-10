.. algorithm_benchmark_toolkit documentation master file, created by
   sphinx-quickstart on Thu Nov 28 10:42:21 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SAES
===========================

This is the documentation for the `SAES` python library, which is a Python library designed to analyze and compare the performance of different algorithms across multiple problems automatically. The tool allows you to: 

1. **Process data from CSV files** containing experiment results.  
2. **Perform advanced statistical studies**, such as Friedman tests or post hoc analysis.  
3. **Automatically generate LaTeX reports** with clear, professional tables.  
4. **Create boxplot graphs** to effectively visualize comparisons between algorithms.  

This tool is aimed at researchers and developers interested in algorithm benchmarking studies for artificial intelligence, optimization, machine learning, and more.

Installation
============

To install the project, you need to clone the repository and install the required dependencies. You will need to have Python 3.8 or higher installed on your system. Before installing the project, we recommend creating a virtual environment to avoid conflicts with other Python projects:

.. code-block:: bash

   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Once you have activated the virtual environment, you can install the project dependencies using the following command:

.. code-block:: bash

   pip install SAES

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   configure/configuration
   API/api
   usage/usage

