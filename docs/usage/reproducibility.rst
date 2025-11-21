Reproducibility and Seeds
=========================

SAES supports deterministic behavior for reproducible research through random seed control.

Why Reproducibility Matters
---------------------------

When analyzing stochastic algorithms, reproducibility is crucial for:

- **Research validation**: Others can verify your results
- **Debugging**: Consistent results make it easier to identify issues
- **Comparisons**: Fair comparison requires consistent conditions
- **Publication**: Many journals and conferences require reproducible results

Functions with Random Seeds
---------------------------

The following SAES functions support deterministic execution via the ``seed`` parameter:

Bayesian Statistical Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~

Both Bayesian tests support the ``seed`` parameter for reproducibility:

.. code-block:: python

    from SAES.statistical_tests.bayesian import bayesian_sign_test, bayesian_signed_rank_test
    import pandas as pd

    data = pd.DataFrame({
        'Algorithm_A': [0.9, 0.85, 0.95, 0.9, 0.92],
        'Algorithm_B': [0.5, 0.6, 0.55, 0.58, 0.52]
    })

    # Deterministic results with seed
    result1, _ = bayesian_sign_test(data, sample_size=5000, seed=42)
    result2, _ = bayesian_sign_test(data, sample_size=5000, seed=42)
    # result1 and result2 will be identical

    # Same for signed rank test
    result3, _ = bayesian_signed_rank_test(data, sample_size=1000, seed=123)

Histogram Plots
~~~~~~~~~~~~~~

The HistoPlot class supports seeding for consistent jitter when handling identical values:

.. code-block:: python

    from SAES.plots.histoplot import HistoPlot
    import pandas as pd

    data = pd.read_csv("results.csv")
    metrics = pd.read_csv("metrics.csv")

    # Create histoplot with reproducible jitter
    histoplot = HistoPlot(data, metrics, "Accuracy", seed=42)
    histoplot.save_instance("Problem1", "output.png")

Best Practices
-------------

1. **Always use seeds for published research**: Set explicit seeds for all random operations
2. **Document your seeds**: Include seed values in your research papers and code
3. **Use different seeds for different experiments**: Avoid accidentally reusing the same random sequence
4. **Version control**: Include seed values in your version-controlled analysis scripts

Example: Complete Reproducible Workflow
---------------------------------------

.. code-block:: python

    from SAES.statistical_tests.bayesian import bayesian_sign_test, bayesian_signed_rank_test
    from SAES.plots.histoplot import HistoPlot
    import pandas as pd

    # Load data
    data = pd.read_csv("algorithm_results.csv")
    metrics = pd.read_csv("metrics.csv")

    # Reproducible Bayesian analysis
    SEED = 42
    algorithm_a = data[data['Algorithm'] == 'A']['MetricValue']
    algorithm_b = data[data['Algorithm'] == 'B']['MetricValue']
    
    comparison_data = pd.DataFrame({
        'Algorithm_A': algorithm_a.values,
        'Algorithm_B': algorithm_b.values
    })

    # Run Bayesian test with seed
    result, samples = bayesian_sign_test(
        comparison_data, 
        sample_size=5000, 
        seed=SEED
    )

    print(f"P(A < B): {result[0]:.4f}")
    print(f"P(A ≈ B): {result[1]:.4f}")
    print(f"P(A > B): {result[2]:.4f}")

    # Create reproducible visualization
    histoplot = HistoPlot(data, metrics, "Accuracy", seed=SEED)
    histoplot.save_all_instances("comparison.png")

Headless Mode for Automated Workflows
-------------------------------------

SAES can be run in headless mode (without display) for automated pipelines and CI/CD:

.. code-block:: bash

    # Set matplotlib to use non-interactive backend
    export MPLBACKEND=Agg

    # Run SAES commands
    python -m SAES -ls -ds data.csv -ms metrics.csv -m HV -s friedman -op results.tex
    python -m SAES -bp -ds data.csv -ms metrics.csv -m HV -i Problem1 -op boxplot.png
    python -m SAES -cdp -ds data.csv -ms metrics.csv -m HV -op cdplot.png

For Python scripts in headless environments:

.. code-block:: python

    import matplotlib
    matplotlib.use('Agg')  # Must be called before importing pyplot
    
    from SAES.plots.boxplot import Boxplot
    import pandas as pd

    # Your analysis code here
    data = pd.read_csv("results.csv")
    metrics = pd.read_csv("metrics.csv")
    
    boxplot = Boxplot(data, metrics, "Accuracy")
    boxplot.save_instance("Problem1", "output.png")

