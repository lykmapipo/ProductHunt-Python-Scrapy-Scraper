"""Spiders mixins."""

import json

DEFAULT_PAGE_SCRIPT_DATA_SELECTOR = "script#__NEXT_DATA__::text"


__all__ = ["PageScriptDataMixin"]


class PageScriptDataMixin:
    """Provide helpers to scrape page script data.

    This include:
        * parse page script data
        * parse references from page script data
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

    def parse_ref_keys(self, key=None, source=None, ref_type="__ref", strict=False):
        """Parse associated/related reference keys from a source.

        Parameters
        ----------
        key (str):
            Valid related data key.

        source (dict):
            Valid portion of page script data as source.

        type (str):
            Valid type of related data. Default to ``__ref``.

        Returns
        -------
        data (set):
            Valid set of keys to referenced data.
        """
        if not key or not source and not isinstance(source, dict):
            return set()

        # parse related/referenced data i.e topics, categories etc.
        for ref_key, ref_values in source.items():
            has_key = key == ref_key if strict else key in ref_key
            ref_values = ref_values or {}
            if has_key:
                # parse a dict with list of refs i.e ``{"edges": [{"node": {"__ref": "Product21"}}]}``
                if isinstance(ref_values, dict) and "edges" in ref_values:
                    ref_values = ref_values.get("edges") or []

                # parse a list of refs i.e ``[{"node": {"__ref": "Product21"}}]``
                # parse a list of refs i.e ``[{"__ref": "Product21"}]``
                if isinstance(ref_values, list):
                    ref_values = [
                        ref_value.get("node") or {}
                        if "node" in ref_value
                        else ref_value
                        for ref_value in ref_values
                        if ref_value
                    ]

                # parse a dict ref e.g ``{"__ref": "Product21"}``
                if isinstance(ref_values, dict) and ref_type in ref_values:
                    ref_values = [ref_values]

                # collect refs from a list of refs i.e ``[{"__ref": "Product21"}]``
                ref_values = [ref_value for ref_value in ref_values if ref_value]
                ref_values = [
                    (ref_value.get(ref_type) or "").strip()
                    for ref_value in ref_values
                    if ref_value
                ]
                ref_values = {ref_value for ref_value in ref_values if ref_value}

                # return and exit
                return ref_values
                break

    def parse_ref_key(self, key=None, source=None, ref_type="__ref"):
        """Parse associated/related reference key from a source.

        Parameters
        ----------
        key (str):
            Valid related data key.

        source (dict):
            Valid portion of page script data as source.

        type (str):
            Valid type of related data. Default to ``__ref``.

        Returns
        -------
        data (str|None):
            Valid key to referenced data.
        """
        ref_keys = self.parse_ref_keys(
            key=key,
            source=source,
            ref_type=ref_type,
            strict=True,
        )
        ref_key = next(iter(ref_keys), None)

        return ref_key

    def parse_ref_values(self, *keys, source=None):
        """Parse associated/related reference values from a source.

        Parameters
        ----------
        source (dict):
            Valid portion of page script data as source.

        keys (*str):
            Valid keys of related data.

        Returns
        -------
        value (list):
            Valid list of ``dict`` of related data.
        """
        if not keys or not source or not isinstance(source, dict):
            return []

        ref_values = [source.get(key) for key in keys if key]
        ref_values = [value for value in ref_values if value]

        return ref_values
