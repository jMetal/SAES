# SAES: Stochastic Algorithm Evaluation Suite
![SAES](https://raw.githubusercontent.com/jMetal/SAES/main/docs/SAES.png)

[![CI](https://github.com/jMetal/SAES/actions/workflows/test.yml/badge.svg)](https://github.com/jMetal/SAES/actions/workflows/test.yml)
[![PyPI Version](https://img.shields.io/pypi/v/SAES.svg)](https://pypi.org/project/SAES/)
[![PyPI Python version](https://img.shields.io/pypi/pyversions/SAES.svg)](https://pypi.org/project/SAES/)
[![PyPI License](https://img.shields.io/pypi/l/SAES.svg)](https://pypi.org/project/SAES/)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-red)](https://jMetal.github.io/SAES/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/jMetal/SAES)

`SAES` is a Python library designed to analyse and compare the performance of stochastic algorithms (e.g. metaheuristics and some machine learning techniques) on multiple problems. 

The current version of the tool offers the following capabilities:  
1. **Seamless CSV data processing**  
   - Import and preprocess experiment results effortlessly.  
   - Handle datasets of varying sizes with ease.  

2. **Statistical analysis**  
   - **Non-parametric tests**:  
     - Friedman test  
     - Friedman aligned-rank test
     - Quade test
     - Wilcoxon signed-rank test  
   - **Parametric tests**:
     - T-Test
     - Anova
   - **Post hoc analysis**:  
     - Nemenyi test (critical distance)

3. **Report generation**  
   - Automated LaTeX reports with the following types of tables:  
     - Median table  
     - Median table with Friedman test  
     - Median table with Wilcoxon pairwise test (pivot-based)  
     - Pairwise Wilcoxon test table (1-to-1 comparison)  
     - Friedman P-Values table (for multiple friedman test variations)
     - Mean table with Anova test
     - Mean table with T-Test pairewise test (pivot-based)
     - Pairwise T-Test table (1-to-1 comparison)

4. **Visualization**  
   - **Boxplot graphs** for algorithm comparison.  
   - **Critical distance plots** for statistical significance.  
   - **Multiobjetive Pareto Front plots** in the [Multiobjective](https://jMetal.github.io/SAES/configure/multiobjective.html) module.
   - **HTML generation** for intuitive analysis.
   - **Bayesian Posterior Plot** for probabilistic comparison of algorithm performance.
   - **Violin Plot** for algorithm performance distribution.
   - **Histogram Plot** for visualizing the distribution of algorithm performance.

5. **CL Interface**
   - Command Line feature to access the different `SAES` functions 

This tool is aimed at researchers and developers interested in algorithm benchmarking studies for artificial intelligence, optimization, machine learning, and more.

`SAES` is a new project that is in its early stages of development. Feel free to open issues for comments, suggestions and bug reports.

## 📖 Context
A stochastic algorithm is an algorithm that incorporates randomness as part of its logic. This randomness leads to variability in outcomes even when applied to the same problem with the same initial conditions. Stochastic algorithms are widely used in various fields, including optimization, machine learning, and simulation, due to their ability to explore larger solution spaces and avoid local optima. Analyzing and comparing stochastic algorithms pose challenges due to their inherent randomness due to the fact that single run does not provide a complete picture of its performance; instead, multiple runs are necessary to capture the distribution of possible outcomes. This variability necessitates a statistical-based methodology based on descriptive (mean, median, standard deviation, ...) and inferential (hypothesis testing) statistics and visualization.

SAES assumes that the results of comparative study between a number of algorithms is provided in a CSV file with this scheme:

- **Algorithm** (string):  Algorithm name.
- **Instance** (string): Instance name. 
- **MetricName** (string): Name of the quality metric used to evaluate the algorithm performace on the instance. 
- **ExecutionId** (integer): Unique identifier for each algorithm run .
- **MetricValue** (double): Value of the metric corresponding to the run. 

### Example of Data file content

| Algorithm | Instance    | MetricName    | ExecutionId | MetricValue         |
|-----------|-------------|---------------|-------------|---------------------|
| SVM       | Iris        | Accuracy      | 0           | 0.985               |
| SVM       | Iris        | Accuracy      | 1           | 0.973               |
| ...       | ...         | ...           | ...         | ...                 |

You will also need a second file to store the information of the different metrics that you to make study. The file must have the following scheme:

- **MetricName** (string): Name of the quality metric used to evaluate the algorithm performace on the instance.
- **Maximize** (boolean): Boolean value to show whether the metric value in that row must be maximized or minimized.

### Example of Metric file content

| MetricName | Maximize    |
|------------|-------------|
| Accuracy   | True        |
| Loss       | False       |
| ...        | ...         |

## SAES API

The SAES library offers a range of functions categorized into three groups, corresponding to its three main features. The following links provide the SAES [Tutorial](https://github.com/jMetal/SAES/tree/main/notebooks) and the SAES [API](https://jMetal.github.io/SAES/API/api.html) documentation that includes a detailed list of features.

## 🛠 Requirements

- **Python**: >= 3.10

## 📦 Installation
Before installing the project, we recommend creating a virtual environment to avoid conflicts with other Python projects:
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Once you have activated the virtual environment, you can install the project with its dependencies using the following command:
```sh
pip install SAES
```

## 🤝 Contributors

- [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/rorro6787) **Emilio Rodrigo Carreira Villalta**
- [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/ajnebro) **Antonio J. Nebro**
