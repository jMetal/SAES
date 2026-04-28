"""Abstract base classes for all statistical tests in SAES."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class StatisticalTestResult:
    """Immutable result from a statistical test.

    Attributes:
        statistic: The test statistic value.
        p_value: The p-value associated with the test statistic.
        test_name: Human-readable name of the test.
        metadata: Optional additional data (e.g., ranks, intermediate values).
    """

    statistic: float
    p_value: float
    test_name: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_significant(self) -> bool:
        """Whether the result is significant at α = 0.05."""
        return self.p_value < 0.05

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to a pandas DataFrame for display compatibility."""
        return pd.DataFrame(
            data=np.array([self.statistic, self.p_value]),
            index=[f"{self.test_name} stat", "p-value"],
            columns=["Results"],
        )


@dataclass(frozen=True)
class PairwiseTestResult:
    """Result from a pairwise (two-algorithm) comparison test.

    Attributes:
        verdict: One of ``"+"``, ``"-"``, or ``"="`` indicating which
            algorithm is statistically better.
        p_value: The p-value from the test.
        test_name: Human-readable name of the test.
    """

    verdict: str
    p_value: float
    test_name: str


@dataclass(frozen=True)
class BayesianTestResult:
    """Result from a Bayesian comparison test.

    Attributes:
        probabilities: Array of shape ``(3,)`` with posterior probabilities
            ``[P(left wins), P(rope/equivalent), P(right wins)]``.
        samples: Array of shape ``(sample_size, 3)`` with Dirichlet samples.
        test_name: Human-readable name of the test.
    """

    probabilities: np.ndarray
    samples: np.ndarray
    test_name: str


class BaseOmnibusTest(ABC):
    """Abstract base for multi-algorithm comparison tests.

    Omnibus tests (Friedman, Quade, ANOVA) determine whether there are
    statistically significant differences among *k ≥ 2* algorithms.
    """

    @abstractmethod
    def run(self, data: pd.DataFrame, *, maximize: bool) -> StatisticalTestResult:
        """Execute the omnibus test.

        Args:
            data: DataFrame where each column is an algorithm and each row
                is a problem instance.  Shape ``(n_instances, k_algorithms)``.
            maximize: If ``True``, higher values are better.

        Returns:
            A :class:`StatisticalTestResult` with the test statistic and p-value.

        Raises:
            StatisticalTestError: If the data is malformed.
        """


class BasePairwiseTest(ABC):
    """Abstract base for two-algorithm comparison tests.

    Pairwise tests (Wilcoxon, T-test) compare exactly two algorithms and
    return a verdict: ``"+"``, ``"-"``, or ``"="``.
    """

    @abstractmethod
    def run(
        self,
        data: pd.DataFrame,
        *,
        maximize: bool,
        alpha: float = 0.05,
    ) -> PairwiseTestResult:
        """Execute the pairwise test.

        Args:
            data: DataFrame with exactly two columns (one per algorithm)
                and one row per instance.
            maximize: If ``True``, higher values are better.
            alpha: Significance level.

        Returns:
            A :class:`PairwiseTestResult` with verdict and p-value.
        """


class BaseBayesianTest(ABC):
    """Abstract base for Bayesian comparison tests.

    Bayesian tests compute posterior probabilities over three hypotheses:
    algorithm A wins, equivalence (ROPE), or algorithm B wins.
    """

    @abstractmethod
    def run(
        self,
        data: pd.DataFrame,
        *,
        rope_limits: tuple[float, float] = (-0.01, 0.01),
        prior_strength: float = 0.5,
        prior_place: str = "rope",
        sample_size: int = 5000,
        seed: int | None = None,
    ) -> BayesianTestResult:
        """Execute the Bayesian test.

        Args:
            data: DataFrame with exactly two columns (one per algorithm).
            rope_limits: Region of practical equivalence ``(lower, upper)``.
            prior_strength: Strength of the Dirichlet prior.
            prior_place: Where to place the pseudo-observation
                (``"left"``, ``"rope"``, or ``"right"``).
            sample_size: Number of posterior samples.
            seed: Random seed for reproducibility.

        Returns:
            A :class:`BayesianTestResult` with probabilities and samples.
        """
