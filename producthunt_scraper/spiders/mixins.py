"""Spiders mixins."""

import json

DEFAULT_PAGE_SCRIPT_DATA_SELECTOR = "script#__NEXT_DATA__::text"


class PageScriptDataMixin:
    """Provide helpers to scrape page script data.

    This include:
        * parse page script data
    """

    def parse_page_script_data(self, response=None, selector=None, **kwargs):
        """Parse page script data.

        Parameters
        ----------
        response (object):
            Valid scrapy response.

        selector (str):
            Valid page script data css selector.

        Returns
        -------
        data (dict):
            Valid page script data as ``dict``.
        """
        # ensure script data selector
        selector = selector or DEFAULT_PAGE_SCRIPT_DATA_SELECTOR

        # parse page script data
        data = response.css(selector)
        data = data.get() or "{}"

        # cast and select data
        data = json.loads(data)
        data = data.get("props", {}).get("apolloState", {})

        return data
