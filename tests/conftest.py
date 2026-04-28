import matplotlib.pyplot as plt
import pytest


@pytest.fixture(autouse=True)
def mock_show(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *args, **kwargs: None)
