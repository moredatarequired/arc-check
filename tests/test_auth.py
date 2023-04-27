import getpass
from unittest.mock import patch

from arc_check import auth


def test_get_api_token_from_input(monkeypatch):
    auth._circle_ci_api_token = None
    monkeypatch.delenv("CIRCLE_CI_API_TOKEN", raising=False)

    api_token = "some strings are better than others 👾"
    with patch.object(getpass, "getpass", return_value=api_token) as mock_getpass:
        token = auth.get_api_token()
        assert token == api_token
        mock_getpass.assert_called_once()


def test_get_api_token_from_env(monkeypatch):
    auth._circle_ci_api_token = None
    api_token = "this **could** be an api t0kn"
    monkeypatch.setenv("CIRCLE_CI_API_TOKEN", api_token)

    token = auth.get_api_token()
    assert token == api_token


def test_get_api_token_from_cache(monkeypatch):
    auth._circle_ci_api_token = None
    api_token = "some circle ci api t-o-k-e-n"
    monkeypatch.setenv("CIRCLE_CI_API_TOKEN", api_token)

    token = auth.get_api_token()
    assert token == api_token

    # Should be cached; test by removing the environment variable.
    monkeypatch.delenv("CIRCLE_CI_API_TOKEN", raising=False)

    token = auth.get_api_token()
    assert token == api_token
