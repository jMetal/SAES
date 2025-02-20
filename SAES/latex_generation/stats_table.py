from SAES.utils.dataframe_processor import process_dataframe_metric
from SAES.statistical_tests.non_parametrical import friedman
from SAES.statistical_tests.non_parametrical import wilcoxon
from SAES.utils.dataframe_processor import check_normality
from SAES.logger import get_logger

from abc import ABC, abstractmethod
import pandas as pd
import os

logger = get_logger(__name__)

def _highlight_max(table: pd.DataFrame):
    is_max = table[:-1] == table[:-1].max() 
    return ['background-color: green' if v else '' for v in is_max] + ['']

def _highlight_min(table: pd.DataFrame):
    is_min = table[:-1] == table[:-1].min() 
    return ['background-color: green' if v else '' for v in is_min] + ['']

class Table(ABC):
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str, normal: bool = False):
        self.data, self.maximize = process_dataframe_metric(data, metrics, metric)
        self.metric = metric
        self.normality = check_normality(self.data)
        self.normal = normal
        self.algorithms = self.data['Algorithm'].unique()
        self.instances = self.data['Instance'].unique()

        self.mean_median = None
        self.std_iqr = None
        self.table = None
        self.latex_doc = None

    def compute_base_table(self):
        if self.normal:
            grouped = self.data.groupby(['Instance', 'Algorithm'])['MetricValue'].agg(['mean', 'std'])
            self.mean_median, self.std_iqr = grouped['mean'], grouped['std']
        else:
            grouped = self.data.groupby(['Instance', 'Algorithm'])['MetricValue'].agg(
                median='median', Q1=lambda x: x.quantile(0.25), Q3=lambda x: x.quantile(0.75)
            )
            self.mean_median, self.std_iqr = grouped['median'], grouped['Q3'] - grouped['Q1']

        self.mean_median = self.mean_median.unstack()
        self.std_iqr = self.std_iqr.unstack()

        self.mean_median = self.mean_median[self.algorithms].reindex(self.instances)
        self.std_iqr = self.std_iqr[self.algorithms].reindex(self.instances)

        self.mean_median.index.name, self.mean_median.columns.name = None, None
        self.std_iqr.index.name, self.std_iqr.columns.name = None, None
    
    def save(self, output_path: str, sideways: bool = False):
        # Create the LaTeX table
        self.create_latex_table(sideways=sideways)
        os.makedirs(output_path, exist_ok=True)

        # Save the LaTeX table to a file
        with open(f"{output_path}/{self.__str__()}_{self.metric}.tex", "w") as f:
            f.write(self.latex_doc)

        logger.info(f"{self.__repr__()} table saved to {output_path}")

    def create_latex_table(self, sideways: bool = False):
        self.compute_table()

        self.latex_doc = """
        \\documentclass{article}
        \\title{Algorithms Comparison}
        \\usepackage{colortbl}
        \\usepackage{float}
        \\usepackage{rotating}
        \\usepackage[table*]{xcolor}
        \\usepackage{tabularx}
        \\usepackage{siunitx}
        \\sisetup{output-exponent-marker=\\text{e}}
        \\xdefinecolor{gray95}{gray}{0.65}
        \\xdefinecolor{gray25}{gray}{0.8}
        \\author{YourName}
        \\begin{document}
        \\maketitle
        \\section{Tables}"""
        
        self.latex_doc += "\\begin{sidewaystable}" if sideways else "\\begin{table}[H]"

        # Step 2: Append the provided body content to the LaTeX document
        self._latex_header()
        self._create_latex_table()
        self._latex_footer(sideways)

        # Step 3: Close the LaTeX document structure
        self.latex_doc += """
        \\end{document}
        """

    @abstractmethod
    def show():
        pass

    @abstractmethod
    def _latex_header(self):
        pass

    def _latex_footer(self, sideways: bool):
        self.latex_doc += """
        \\hline
        \\end{tabular}
        \\end{scriptsize}
        """ 
        
        self.latex_doc += "\\end{sidewaystable}" if sideways else "\\end{table}"

    @abstractmethod
    def _create_latex_table(self):
        pass

    @abstractmethod
    def compute_table(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

class MeanMedian(Table):
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str, normal: bool = False):
        super().__init__(data, metrics, metric, normal=normal)

    def compute_table(self):
        self.compute_base_table()
        self.table = self.mean_median.copy()

    def show(self):
        pass
    
    def _create_latex_table(self):
        # Loop over instances and format the row data
        for instance in self.instances:
            row_data = f"{instance} & "
            median = self.mean_median.loc[instance]
            std_dev = self.std_iqr.loc[instance]
            
            # Compute df_global and find the max and second idx
            df_global = median / std_dev
            max_idx = df_global.idxmax()
            second_idx = df_global.drop(max_idx).idxmax()

            # Loop over algorithms and format the row data
            for algorithm in self.algorithms:
                score1 = median[algorithm]
                score2 = std_dev[algorithm]

                # Create the formatted string based on conditions
                if algorithm == max_idx:
                    row_data += f"\\cellcolor{{gray95}}${score1:.2e}_{{ {score2:.2e} }}$ & "
                elif algorithm == second_idx:
                    row_data += f"\\cellcolor{{gray25}}${score1:.2e}_{{ {score2:.2e} }}$ & "
                else:
                    row_data += f"${score1:.2e}_{{ {score2:.2e} }}$ & "

            self.latex_doc += row_data.rstrip(" & ") + " \\\\ \n"

    def _latex_header(self):
        self.latex_doc += """
        \\
        \\caption{""" + self.metric + """.  """ + str(self.__repr__()) + """}
        \\vspace{1mm}
        \\centering
        \\begin{scriptsize}
        \\begin{tabular}{l|""" + """c|""" * (len(self.algorithms) - 1) + """c}
        \\hline
        & """ + " & ".join(self.algorithms) + " \\\\ \\hline\n"

    def __str__(self):
        return "MeanMedian"
        
    def __repr__(self):
        if self.normal:
            return "Mean and Standard Deviation Table"
        else:
            return "Median and Interquartile Range Table"

class Friedman(Table):
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str, normal: bool = False):
        super().__init__(data, metrics, metric, normal=normal)

    def compute_table(self):
        if self.normal:
            logger.warning('Friedman test is only applicable for non normal data. The test will be skipped.')
            return

        self.compute_base_table()

        self.table = self.mean_median.copy()
        for instance in self.instances:
            data = self.data[self.data['Instance'] == instance]
            friedman_table = data.pivot(index='ExecutionId', 
            columns='Algorithm', values='MetricValue').reset_index().drop(columns='ExecutionId')

            friedman_results = friedman(friedman_table, self.maximize)
            self.table.loc[instance, 'Friedman'] = "+"
            if friedman_results["Results"]["p-value"] < 0.05:
                self.table.loc[instance, 'Friedman'] = "+"
            else:
                self.table.loc[instance, 'Friedman'] = "="

    def show(self):
        self.compute_table()
        if self.maximize:
            styled_df = self.table.style.apply(_highlight_max, axis=1)
        else:
            styled_df = self.table.style.apply(_highlight_min, axis=1)

        styled_df.format({col: "{:.4e}" for col in self.table.select_dtypes(include=["number"]).columns})

        return styled_df
    
    def _create_latex_table(self):
        # Loop over instances and format the row data
        for instance in self.instances:
            row_data = f"{instance} & "
            median = self.mean_median.loc[instance]
            std_dev = self.std_iqr.loc[instance]
            
            # Compute df_global and find the max and second idx
            df_global = median / std_dev
            max_idx = df_global.idxmax()
            second_idx = df_global.drop(max_idx).idxmax()

            # Loop over algorithms and format the row data
            for algorithm in self.algorithms:
                score1 = median[algorithm]
                score2 = std_dev[algorithm]

                # Create the formatted string based on conditions
                if algorithm == max_idx:
                    row_data += f"\\cellcolor{{gray95}}$\\SI{{{score1:.2e}}}{{}}_{{ \\SI{{{score2:.2e}}}{{}} }}$ & "
                elif algorithm == second_idx:
                    row_data += f"\\cellcolor{{gray25}}$\\SI{{{score1:.2e}}}{{}}_{{ \\SI{{{score2:.2e}}}{{}} }}$ & "
                else:
                    row_data += f"$\\SI{{{score1:.2e}}}{{}}_{{ \\SI{{{score2:.2e}}}{{}} }}$ & "

                # Add the Friedman result to the last column
                if algorithm == self.algorithms[-1]:
                    row_data += f"{self.table.loc[instance, 'Friedman']} & "

            self.latex_doc += row_data.rstrip(" & ") + " \\\\ \n"

    def _latex_header(self):
        self.latex_doc += """
        \\caption{""" + self.metric + """.  """ + str(self.__repr__()) + f" (+ implies that the difference between the algorithms for the instance in the select row is significant)\n" + """}
        \\vspace{1mm}
        \\centering
        \\begin{scriptsize}
        \\begin{tabular}{l|""" + """c|""" * (len(self.algorithms)) + """c}
        \\hline
        & """ + " & ".join(self.algorithms) + " & FT \\\\ \\hline\n"

    def __str__(self):
        return "Friedman"
        
    def __repr__(self):
        if self.normal:
            return "Mean and Standard Deviation Friedman Table"
        else:
            return "Median and Interquartile Range Friedman Table"

class WilcoxonPivot(Table):
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str, normal: bool = False):
        super().__init__(data, metrics, metric, normal=normal)

    def compute_table(self):
        if self.normal:
            logger.warning('Wilcoxon test is only applicable for non normal data. The test will be skipped.')
            return
        
        self.compute_base_table()

        self.table = self.mean_median.copy().map(lambda x: (x, ''))
        pivot_algorithm = self.algorithms[-1]
        for instance in self.instances:
            data = self.data[self.data['Instance'] == instance]
            data = data.pivot(index='ExecutionId', columns='Algorithm', values='MetricValue').reset_index().drop(columns='ExecutionId')

            for algorithm in self.algorithms:
                if algorithm == pivot_algorithm:
                    continue
                
                wilconxon_table = data[[pivot_algorithm, algorithm]]
                wilconxon_table.index.name, wilconxon_table.columns.name = None, None
                wilconxon_table.columns = ["Algorithm A", "Algorithm B"]
                wilcoxon_result = wilcoxon(wilconxon_table, self.maximize)
                self.table.loc[instance, algorithm] = (self.table.loc[instance, algorithm][0], wilcoxon_result)
    
    def show(self):
        pass

    def _create_latex_table(self):
        ranks = {algorithm: [0, 0, 0] for algorithm in self.algorithms[:-1]}
        # Loop over instances and format the row data
        for instance in self.instances:
            row_data = f"{instance} & "
            median = self.mean_median.loc[instance]
            std_dev = self.std_iqr.loc[instance]
            
            # Compute df_global and find the max and second idx
            df_global = median / std_dev
            max_idx = df_global.idxmax()
            second_idx = df_global.drop(max_idx).idxmax()

            # Loop over algorithms and format the row data
            for algorithm in self.algorithms:
                wilcoxon_result = self.table.loc[instance, algorithm][1]

                # Update the ranks for the Wilcoxon test results
                if algorithm != self.algorithms[-1]:
                    if wilcoxon_result == "+":
                        ranks[algorithm][0] += 1
                    elif wilcoxon_result == "-":
                        ranks[algorithm][1] += 1
                    else:
                        ranks[algorithm][2] += 1

                score1 = median[algorithm]
                score2 = std_dev[algorithm]

                # Create the formatted string based on conditions
                if algorithm == max_idx:
                    row_data += f"\\cellcolor{{gray95}}$\\SI{{{score1:.2e}}}{{}}_{{ \\SI{{{score2:.2e}}}{{}} }} {wilcoxon_result}$ & "
                elif algorithm == second_idx:
                    row_data += f"\\cellcolor{{gray25}}$\\SI{{{score1:.2e}}}{{}}_{{ \\SI{{{score2:.2e}}}{{}} }} {wilcoxon_result}$ & "
                else:
                    row_data += f"$\\SI{{{score1:.2e}}}{{}}_{{ \\SI{{{score2:.2e}}}{{}} }} {wilcoxon_result}$ & "

            self.latex_doc += row_data.rstrip(" & ") + " \\\\ \n"

        # Add the last row with the ranks
        self.latex_doc += """\\hline + / - / ="""
        for _, rank in ranks.items():
            self.latex_doc += f" & \\textbf{rank[0]} / \\textbf{rank[1]} / \\textbf{rank[2]}"

    def _latex_header(self):
        self.latex_doc += """
        \\caption{""" + self.metric + """.  """ + str(self.__repr__()) + (
            f" (+/- implies that the pivot algorithm (last column) is statistically "
            f"worse/better, = indicates that the differences are not significant.)\n") + """}
        \\vspace{1mm}
        \\centering
        \\begin{scriptsize}
        \\begin{tabular}{l|""" + """c|""" * (len(self.algorithms) - 1) + """c}
        \\hline
        & """ + " & ".join(self.algorithms) + " \\\\ \\hline\n"

    def __str__(self):
        return "WilcoxonPivot"
        
    def __repr__(self):
        if self.normal:
            return "Mean and Standard Deviation Wilcoxon Pivot Table"
        else:
            return "Median and Interquartile Range Wilcoxon Pivot Table"

class Wilcoxon(Table):
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str, normal: bool = False):
        super().__init__(data, metrics, metric, normal=normal)

    def compute_table(self):
        if self.normal:
            logger.warning('Wilcoxon test is only applicable for non normal data. The test will be skipped.')
            return

        self.compute_base_table()

        self.table = pd.DataFrame("", index=self.algorithms[:-1], columns=self.algorithms[1:])

        for i, fila in enumerate(self.algorithms[:-1]):
            for _, columna in enumerate(self.algorithms[i+1:]):
                wilcoxon_result = ""
                for instance in self.instances:
                    data = self.data[self.data['Instance'] == instance]
                    data = data.pivot(index='ExecutionId', columns='Algorithm', values='MetricValue').reset_index().drop(columns='ExecutionId')
                    wilcoxon_table = data[[fila, columna]]
                    wilcoxon_table.index.name, wilcoxon_table.columns.name = None, None
                    wilcoxon_table.columns = ["Algorithm A", "Algorithm B"]
                    wilcoxon_result += wilcoxon(wilcoxon_table, self.maximize)
                
                self.table.at[fila, columna] = wilcoxon_result
    
    def show(self):
        self.compute_table()
        return self.table.style.set_properties(**{'font-size': '20px'})

    def _create_latex_table(self):
        # Generate comparisons and populate table
        compared_pairs = set()

        # Loop over algorithms and format the row data
        for algorithm1 in self.algorithms:
            if algorithm1 == self.algorithms[-1]:
                continue
            self.latex_doc += algorithm1 + " & "

            # Loop over algorithms and format the row data
            for algorithm2 in self.algorithms:
                if algorithm2 == self.algorithms[0]:
                    continue
                if algorithm1 == algorithm2:
                    self.latex_doc += " & "
                    continue

                # Create a pair of algorithms
                pair = tuple(sorted([algorithm1, algorithm2]))
                self.latex_doc += "\\texttt{"
                
                # Check if the pair has already been processed
                if pair not in compared_pairs:
                    # Mark the pair as processed
                    compared_pairs.add(pair)
                    for index, _ in enumerate(self.instances):
                        wilcoxon_results = self.table.loc[algorithm1, algorithm2][index]
                        self.latex_doc += wilcoxon_results
                        
                self.latex_doc += "} & "
            self.latex_doc = self.latex_doc.rstrip(" & ") + " \\\\\n"

    def _latex_header(self):
        header_explanation = (". Each symbol in the cells represents a problem. Symbol +/- indicates that the row/column "
                          "algorithm performs better with statistical confidence;  symbol = implies that "
                          "the differences are not significant.")
        
        self.latex_doc += """
        \\caption{""" + self.metric + """.  """ + str(self.__repr__()) + header_explanation + f" Instances (in order) : {self.instances}\n" + """}
        \\vspace{1mm}
        \\centering
        \\begin{scriptsize}
        \\begin{tabular}{l|""" + """c|""" * (len(self.algorithms) - 2) + """c}
        \\hline
        & """ + " & ".join(self.algorithms[1:]) + " \\\\ \\hline\n"

    def __str__(self):
        return "Wilcoxon"
    
    def __repr__(self):
        return "Wilcoxon Test 1vs1 Table"

if __name__ == "__main__":
    data = '/home/khaosdev/SAES/notebooks/swarmIntelligence.csv'
    metrics = '/home/khaosdev/SAES/notebooks/multiobjectiveMetrics.csv'
    metric = 'IGD+'
    table = Friedman(data, metrics, metric)
    

    table.show()
    
