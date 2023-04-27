import getpass
import os
from typing import Optional

TOKEN_ENV_VAR = "CIRCLE_CI_API_TOKEN"


_circle_ci_api_token: Optional[str] = None


def get_api_token() -> str:
    """Get API token from user input or environment variable."""
    global _circle_ci_api_token
    if _circle_ci_api_token is not None:
        return _circle_ci_api_token

    token = os.environ.get(TOKEN_ENV_VAR)
    if token is None:
        token = getpass.getpass(f"Enter API token (or set {TOKEN_ENV_VAR}): ")

    _circle_ci_api_token = token
    return token
