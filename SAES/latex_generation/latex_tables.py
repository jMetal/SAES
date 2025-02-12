from SAES.statistical_tests.non_parametrical import wilcoxon_test
from SAES.statistical_tests.non_parametrical import friedman_test
from SAES.utils.csv_processor import process_csv_metrics
from SAES.utils.statistical_checks import check_normality
from SAES.statistical_tests.non_parametrical import friedman_test
from SAES.statistical_tests.non_parametrical import wilcoxon_test
import pandas as pd
from abc import ABC, abstractmethod

from SAES.logger import get_logger
logger = get_logger(__name__)

class Table(ABC):
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str):
        self.data, self.maximize = process_csv_metrics(data, metrics, metric)
        self.metric = metric
        self.normal = check_normality(self.data)
        self.algorithms = self.data['Algorithm'].unique()
        self.instances = self.data['Instance'].unique()

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

    @abstractmethod
    def compute_table(self):
        pass

    @abstractmethod
    def print_latex(self):
        pass

class MeanMedianTable(Table):
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str):
        super().__init__(data, metrics, metric)

    def compute_table(self):
        self.compute_base_table()

class FriedmanTable(Table):
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str):
        super().__init__(data, metrics, metric)

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

            friedman_results = friedman_test(friedman_table, self.maximize)
            self.table.loc[instance, 'Friedman'] = "+"
            if friedman_results["Results"]["p-value"] < 0.05:
                self.table.loc[instance, 'Friedman'] = "+"
            else:
                self.table.loc[instance, 'Friedman'] = "="

    def print_latex(self):
        pass

class WilcoxonPivot(Table):
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str):
        super().__init__(data, metrics, metric)

    def compute_table(self):
        if self.normal:
            logger.warning('Wilcoxon test is only applicable for non normal data. The test will be skipped.')
            return
        
        self.compute_base_table()

        self.table = self.mean_median.copy().map(lambda x: ({x}, 'X'))
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
                wilcoxon_result = wilcoxon_test(wilconxon_table, self.maximize)
                self.table.loc[instance, algorithm] = (self.table.loc[instance, algorithm][0], wilcoxon_result)

    def print_latex(self):
        pass



if __name__ == "__main__":
    data = '/home/khaosdev/SAES/notebooks/swarmIntelligence.csv'
    metrics = '/home/khaosdev/SAES/notebooks/multiobjectiveMetrics.csv'
    metric = 'EP'
    table = WilcoxonPivot(data, metrics, metric)
    table.compute_table()
    print(table.table)