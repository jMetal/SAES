"""Registry for statistical tests — enables pluggable extensibility."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal, TypeVar, cast, overload

from saes.exceptions import ConfigurationError
from saes.statistical_tests.base import (
    BaseBayesianTest,
    BaseOmnibusTest,
    BasePairwiseTest,
)


class TestName(StrEnum):
    """Available statistical tests."""

    __test__ = False

    # Omnibus tests
    FRIEDMAN = "friedman"
    FRIEDMAN_ALIGNED = "friedman_aligned"
    QUADE = "quade"
    ANOVA = "anova"

    # Pairwise tests
    WILCOXON = "wilcoxon"
    T_TEST = "t_test"

    # Bayesian tests
    BAYESIAN_SIGN = "bayesian_sign"
    BAYESIAN_SIGNED_RANK = "bayesian_signed_rank"


# Global registry mapping lowercase names to test classes
_REGISTRY: dict[str, type] = {}


def register_test(name: str | TestName) -> Any:
    """Decorator to register a test class by name.

    Usage::

        @register_test(TestName.FRIEDMAN)
        class FriedmanTest(BaseOmnibusTest): ...

    Args:
        name: Case-insensitive identifier or :class:`TestName`.

    Returns:
        Decorator function.
    """

    def decorator(cls: type) -> type:
        _REGISTRY[str(name).lower()] = cls
        return cls

    return decorator


T = TypeVar("T", BaseOmnibusTest, BasePairwiseTest, BaseBayesianTest)


@overload
def get_test(
    name: Literal[TestName.FRIEDMAN, TestName.FRIEDMAN_ALIGNED, TestName.QUADE, TestName.ANOVA],
    *args: Any,
    **kwargs: Any,
) -> BaseOmnibusTest: ...


@overload
def get_test(
    name: Literal[TestName.WILCOXON, TestName.T_TEST],
    *args: Any,
    **kwargs: Any,
) -> BasePairwiseTest: ...


@overload
def get_test(
    name: Literal[TestName.BAYESIAN_SIGN, TestName.BAYESIAN_SIGNED_RANK],
    *args: Any,
    **kwargs: Any,
) -> BaseBayesianTest: ...


@overload
def get_test(
    name: str | TestName,
    *args: Any,
    **kwargs: Any,
) -> BaseOmnibusTest | BasePairwiseTest | BaseBayesianTest: ...


def get_test(
    name: str | TestName, *args: Any, **kwargs: Any
) -> BaseOmnibusTest | BasePairwiseTest | BaseBayesianTest:
    """Instantiate a statistical test by its registered name.

    Args:
        name: Case-insensitive name or :class:`TestName`.
        *args: Positional arguments forwarded to the test constructor.
        **kwargs: Keyword arguments forwarded to the test constructor.

    Returns:
        An instance of the requested test.

    Raises:
        ConfigurationError: If the name is not registered.
    """

    key = str(name).lower()
    if key not in _REGISTRY:
        import importlib

        module_map = {
            "anova": "saes.statistical_tests.omnibus.anova",
            "friedman": "saes.statistical_tests.omnibus.friedman",
            "friedman_aligned": "saes.statistical_tests.omnibus.friedman_aligned",
            "quade": "saes.statistical_tests.omnibus.quade",
            "t_test": "saes.statistical_tests.pairwise.t_test",
            "wilcoxon": "saes.statistical_tests.pairwise.wilcoxon",
            "bayesian_sign": "saes.statistical_tests.bayesian.sign_test",
            "bayesian_signed_rank": "saes.statistical_tests.bayesian.signed_rank_test",
        }
        if key in module_map:
            importlib.import_module(module_map[key])

    if key not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY.keys()))
        msg = f"Unknown test '{name}'. Available: {available}"
        raise ConfigurationError(msg)
    return cast(
        BaseOmnibusTest | BasePairwiseTest | BaseBayesianTest, _REGISTRY[key](*args, **kwargs)
    )
