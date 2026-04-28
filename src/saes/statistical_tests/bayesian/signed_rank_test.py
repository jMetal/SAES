"""Bayesian signed-rank test for pairwise algorithm comparison."""

from __future__ import annotations

import numpy as np
import pandas as pd

from saes.exceptions import ConfigurationError, StatisticalTestError
from saes.logger import get_logger
from saes.statistical_tests.base import BaseBayesianTest, BayesianTestResult
from saes.statistical_tests.registry import TestName, register_test

logger = get_logger(__name__)

_VALID_PRIOR_PLACES = ("left", "rope", "right")


@register_test(TestName.BAYESIAN_SIGNED_RANK)
class BayesianSignedRankTest(BaseBayesianTest):
    """Bayesian signed-rank test for pairwise algorithm comparison.

    Extends the Bayesian sign test by incorporating the magnitude of
    differences (not just their sign).  Uses a weighted Dirichlet process
    over the pairwise sums of differences.

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
        prior_strength: float = 1.0,
        prior_place: str = "rope",
        sample_size: int = 1000,
        seed: int | None = None,
    ) -> BayesianTestResult:
        """Execute the Bayesian signed-rank test.

        Args:
            data: DataFrame or array with exactly 2 columns (algorithms).
            rope_limits: ``(lower, upper)`` bounds of practical equivalence.
            prior_strength: Strength of the Dirichlet prior (must be > 0).
            prior_place: Pseudo-observation placement (``"left"``,
                ``"rope"``, or ``"right"``).
            sample_size: Number of Monte Carlo samples.
            seed: Random seed for reproducibility.

        Returns:
            A :class:`BayesianTestResult` with posterior probabilities
            and the raw samples.
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

        logger.debug(
            "Running Bayesian signed-rank test: n=%d, sample_size=%d",
            n,
            sample_size,
        )

        # Compute differences with pseudo-observation z_0
        z = sample1 - sample2
        z0_values = {
            "left": -float("inf"),
            "rope": 0.0,
            "right": float("inf"),
        }
        z0 = z0_values[prior_place]
        z_full = np.concatenate(([z0], z))

        # Monte Carlo sampling via weighted Dirichlet process
        samples = np.zeros((sample_size, 3))
        for mc in range(sample_size):
            # Draw weights from Dirichlet(prior_strength, 1, 1, ..., 1)
            dir_alpha = np.ones(n + 1)
            dir_alpha[0] = prior_strength
            w = rng.dirichlet(dir_alpha)

            # Compute posterior mass for each region
            for i in range(n + 1):
                for j in range(i, n + 1):
                    pairwise_sum = z_full[i] + z_full[j]
                    weight = 2.0 * w[i] * w[j] if i != j else w[i] * w[j]

                    if pairwise_sum < 2 * rope_limits[0]:
                        samples[mc, 0] += weight
                    elif pairwise_sum > 2 * rope_limits[1]:
                        samples[mc, 2] += weight
                    else:
                        samples[mc, 1] += weight

        # Compute posterior probabilities
        winner_id = np.argmax(samples, axis=1)
        win_left = int(np.sum(winner_id == 0))
        win_right = int(np.sum(winner_id == 2))
        win_rope = sample_size - win_left - win_right

        probabilities = np.array([win_left, win_rope, win_right]) / float(sample_size)

        logger.debug(
            "Bayesian signed-rank: P(left)=%.3f, P(rope)=%.3f, P(right)=%.3f",
            probabilities[0],
            probabilities[1],
            probabilities[2],
        )

        return BayesianTestResult(
            probabilities=probabilities,
            samples=samples,
            test_name="Bayesian Signed Rank Test",
        )
