# SAES: Stochastic Algorithm Evaluation Suite
![UMA CV 2025](https://github.com/rorro6787/rorro6787/blob/main/Images/benchmark-817347020.png "Khaos Investigation Group Logo")

`SAES` is a Python library designed to analyse and compare the performance of stochastic algorithms (e.g. metaheuristics and machine learning techniques) on multiple problems. 

The current version of the tool (V0.1) allows you to:  
1. **Process data from CSV files** containing experiment results.  
2. **Perform advanced statistical studies**, such as Friedman tests or post hoc analysis.  
3. **Automatically generate LaTeX reports** with clear, professional tables.  
4. **Create boxplot graphs** to effectively visualize comparisons between algorithms.  

This tool is aimed at researchers and developers interested in algorithm benchmarking studies for artificial intelligence, optimization, machine learning, and more.

## 📖 Context
A stochastic algorithm is an algorithm that incorporates randomness as part of its logic. This randomness leads to variability in outcomes even when applied to the same problem with the same initial conditions. Stochastic algorithms are widely used in various fields, including optimization, machine learning, and simulation, due to their ability to explore larger solution spaces and avoid local optima. Analyzing and comparing stochastic algorithms pose challenges due to their inherent randomness due to the fact that single run does not provide a complete picture of its performance; instead, multiple runs are necessary to capture the distribution of possible outcomes. This variability necessitates a statistical-based methodology based on descriptive (mean, median, standard deviation, ...) and inferential (hypothesis testing) statistics and visualization.

SAES assumes that the results of comparative study between a number of algorithms is provided in a CSV file with this scheme:

- **Algorithm** (string):  Algorithm name.
- **Instance** (string): Instance name. 
- **MetricName** (string): Name of the quality metric used to evaluate the algorithm performace on the instance. 
- **ExecutionId** (integer): Unique identifier for each algorithm run .
- **MetricValue** (double): Value of the metric corresponding to the run. 

### Example of file content

| Algorithm | Problem     | MetricName    | ExecutionId | MetricValue         |
|-----------|-------------|---------------|-------------|---------------------|
| SVM       | Iris        | Accuracy      | 0           | 0.985               |
| SVM       | Iris        | Accuracy      | 1           | 0.973               |
| ...       | ...         | ...           | ...         | ...                 |


## 🛠 Requirements

- **Python**: 3.X.X

## 📦 Installation

Run the following commands to clone and configure the repository in your local machine:
```sh
git clone https://github.com/rorro6787/algorithm-benchmark-toolkit.git
cd algorithm-benchmark-toolkit
```

## 🤝 Contributors

- [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/rorro6787) **Emilio Rodrigo Carreira Villalta**
- [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/ajnebro) **Antonio Jesús Nebro**


