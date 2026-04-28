"""Bayesian sign test for pairwise algorithm comparison."""

from __future__ import annotations

import numpy as np
import pandas as pd

from saes.exceptions import ConfigurationError, StatisticalTestError
from saes.logger import get_logger
from saes.statistical_tests.base import BaseBayesianTest, BayesianTestResult
from saes.statistical_tests.registry import TestName, register_test

logger = get_logger(__name__)

_VALID_PRIOR_PLACES = ("left", "rope", "right")


@register_test(TestName.BAYESIAN_SIGN)
class BayesianSignTest(BaseBayesianTest):
    """Bayesian sign test for pairwise algorithm comparison.

    Computes the posterior probability that one algorithm is better,
    equivalent (within the ROPE), or worse than another, using a
    Dirichlet-Multinomial model.

    Reference:
        Benavoli, A. et al. (2017). *Time for a change: a tutorial for
        comparing multiple classifiers through Bayesian analysis.*
        JMLR 18(1), 2653–2688.  https://arxiv.org/pdf/1606.04316
    """

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
        """Execute the Bayesian sign test.

        Args:
            data: DataFrame or array with exactly 2 columns (algorithms).
            rope_limits: ``(lower, upper)`` bounds of practical equivalence.
            prior_strength: Strength of the Dirichlet prior (must be > 0).
            prior_place: Pseudo-observation placement (``"left"``,
                ``"rope"``, or ``"right"``).
            sample_size: Number of Dirichlet posterior samples.
            seed: Random seed for reproducibility.

        Returns:
            A :class:`BayesianTestResult` with posterior probabilities
            ``[P(left), P(rope), P(right)]`` and the raw Dirichlet samples.

        Raises:
            ConfigurationError: If ``prior_strength <= 0`` or
                ``prior_place`` is invalid.
            StatisticalTestError: If the data does not have exactly 2 columns.
        """
        if prior_strength <= 0:
            msg = "prior_strength must be a positive float."
            raise ConfigurationError(msg)

        if prior_place not in _VALID_PRIOR_PLACES:
            msg = f"prior_place must be one of {_VALID_PRIOR_PLACES}, got '{prior_place}'."
            raise ConfigurationError(msg)

        values = data.values if isinstance(data, pd.DataFrame) else data

        if values.shape[1] != 2:
            msg = f"Expected 2 columns, got {values.shape[1]}."
            raise StatisticalTestError(msg)

        sample1, sample2 = values[:, 0], values[:, 1]
        n = values.shape[0]

        rng = np.random.default_rng(seed)

        logger.debug("Running Bayesian sign test: n=%d, sample_size=%d", n, sample_size)

        # Compute pairwise differences
        z = sample1 - sample2

        n_right = int(np.sum(z > rope_limits[1]))
        n_left = int(np.sum(z < rope_limits[0]))
        n_equiv = n - n_right - n_left

        # Dirichlet parameters
        alpha = np.array([n_left, n_equiv, n_right], dtype=float) + 1e-6
        alpha[_VALID_PRIOR_PLACES.index(prior_place)] += prior_strength

        # Sample from Dirichlet posterior
        samples = rng.dirichlet(alpha, sample_size)

        # Compute posterior probabilities from argmax
        winner_id = np.argmax(samples, axis=1)
        win_left = int(np.sum(winner_id == 0))
        win_right = int(np.sum(winner_id == 2))
        win_rope = sample_size - win_left - win_right

        probabilities = np.array([win_left, win_rope, win_right]) / float(sample_size)

        logger.debug(
            "Bayesian sign test: P(left)=%.3f, P(rope)=%.3f, P(right)=%.3f",
            probabilities[0],
            probabilities[1],
            probabilities[2],
        )

        return BayesianTestResult(
            probabilities=probabilities,
            samples=samples,
            test_name="Bayesian Sign Test",
        )
