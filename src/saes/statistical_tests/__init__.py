"""Statistical testing subpackage for SAES."""

from __future__ import annotations

from saes.statistical_tests.registry import TestName, get_test, register_test

__all__ = ["TestName", "get_test", "register_test"]
