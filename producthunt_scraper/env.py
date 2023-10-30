"""Parse and load environment variables."""

import os

from dotenv import find_dotenv, load_dotenv

__all__ = ["env"]

# find .env and load up the entries as environment variables
load_dotenv(find_dotenv())


def env(key, default=None, cast=None, transform=None):
    """Get, transform and cast environment variable.

    Parameters
    ----------
    key (str):
        Valid environment variable key.

    default (*):
        Default value for variable.

    cast (class):
        Valid class to cast enviroment variable to.

    transform (callable):
        Valid callable to apply on enviroment variable.

    Returns
    -------
    dict (dict):
        Valid dict

    Examples
    --------
    >>> from producthunt_scraper.env import env
    >>> AJAXCRAWL_ENABLED = env("AJAXCRAWL_ENABLED", False, bool)
    >>> AJAXCRAWL_ENABLED == False
    True
    """
    value = os.environ.get(key)
    value = value if value else default

    if value and callable(transform):
        value = transform(value)

    if value and callable(cast):
        value = cast(value)

    return value
