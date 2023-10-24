"""Trending products scraping spiders.

How it works:

This spider, do:
    1. Scrape trending topics from producthunt topics page.
    2. Scrape top products, for each trending topic page based on trending order.
    3. Save batches of trending products per day.

Usage:

To scrape `trending products`, run:
>>> scrapy crawl trending-products
"""

import json
from datetime import datetime
from urllib.parse import urlencode

import scrapy

from producthunt_scraper.settings import (
    BASE_DATA_DIR,
    PRODUCTHUNT_ALLOWED_DOMAINS,
    PRODUCTHUNT_PRODUCT_SORT_FILTERS,
    PRODUCTHUNT_PRODUCTS_BASE_URL,
    PRODUCTHUNT_TOPICS_BASE_URL,
)

# selectors
TRENDING_TOPIC_URL_SELECTOR = "div[data-test=trending-topics-card] a::attr(href)"
TRENDING_PRODUCT_URL_SELECTOR = "main[class=layoutMain] ul > div > div > a::attr(href)"
PRODUCT_SCRIPT_DATA_SELECTOR = "script#__NEXT_DATA__::text"

# mappings
PRODUCT_DATA_MAPPINGS = {
    "id": "product_id",
    "slug": "product_slug",
    "name": "product_name",
    "tagline": "product_tagline",
    "description": "product_description",
    "url": "product_url",
    "websiteUrl": "product_website_url",
    "reviewsRating": "product_rating",
    "followersCount": "product_followers_count",
    "totalVotesCount": "product_total_votes_count",
    "reviewersCount": "product_reviewers_count",
    "reviewsCount": "product_reviews_count",
    "postsCount": "product_posts_count",
    "stacksCount": "product_stacks_count",
    "alternativesCount": "product_alternatives_count",
    "tipsCount": "product_tips_count",
    "addonsCount": "product_addons_count",
    "platforms": "product_platforms",
}


class TrendingProductsSpider(scrapy.Spider):
    """Scrape top trending products from trending topics."""

    name = "trending-products"
    allowed_domains = PRODUCTHUNT_ALLOWED_DOMAINS
    start_urls = [PRODUCTHUNT_TOPICS_BASE_URL]

    data_dir = BASE_DATA_DIR
    last_scraped_date = datetime.utcnow().date()

    custom_settings = {
        "FEEDS": {
            "%(data_dir)s/%(name)s/date=%(last_scraped_date)s/part-%(batch_id)d.jsonl": {
                "format": "jsonlines",
                "overwrite": True,
                "store_empty": False,
                "batch_item_count": 100,
            }
        },
    }

    def __init__(self, *args, **kwargs):
        super(TrendingProductsSpider, self).__init__(*args, **kwargs)
        self.last_scraped_date = datetime.utcnow().date()

    def parse(self, response, **kwargs):
        # check url type
        response_url = str(response.url)
        is_topic_url = response_url.startswith(PRODUCTHUNT_TOPICS_BASE_URL)
        is_product_url = response_url.startswith(PRODUCTHUNT_PRODUCTS_BASE_URL)

        # ignore unknown urls
        if not is_topic_url and not is_product_url:
            return

        # parse main topics page and yield trending topics pages urls
        if response_url == PRODUCTHUNT_TOPICS_BASE_URL:
            trending_topic_urls = self.parse_topics_page(response=response, **kwargs)
            for trending_topic_url in trending_topic_urls:
                yield response.follow(trending_topic_url, self.parse)

        # parse topic page and yield trending products urls
        if is_topic_url and response_url != PRODUCTHUNT_TOPICS_BASE_URL:
            product_urls = self.parse_topic_page(response=response, **kwargs)
            for product_url in product_urls:
                yield response.follow(product_url, self.parse)

        # parse product page and yield product dictionary/item
        if is_product_url:
            yield from self.parse_product_page(response=response, **kwargs)

    def parse_topics_page(self, response=None, **kwargs):
        """Parse main topics page and yield trending topics pages urls."""

        # parse trending topic urls from topics page
        trending_topic_urls = response.css(TRENDING_TOPIC_URL_SELECTOR)
        trending_topic_urls = set(trending_topic_urls.getall())

        # compile trending topic url per products sort filter
        for trending_topic_url in trending_topic_urls:
            for sort_filter in PRODUCTHUNT_PRODUCT_SORT_FILTERS:
                products_sort_filter = {"order": sort_filter}
                encoded_products_sort_filter = urlencode(products_sort_filter)
                topic_url = f"""{trending_topic_url}?{encoded_products_sort_filter}"""
                yield topic_url

    def parse_topic_page(self, response=None, **kwargs):
        """Parse topic page and yield trending products urls."""

        # parse product urls from topic page
        product_urls = response.css(TRENDING_PRODUCT_URL_SELECTOR)
        product_urls = set(product_urls.getall())

        # compile and yield product page url
        for product_url in product_urls:
            yield product_url

    def parse_product_page(self, response=None, **kwargs):
        """Parse product page and yield a product item."""
        raw_product = self.parse_product_data(response=response, **kwargs)
        for key, value in raw_product.items():
            if "Product" in key and "structuredData" in value:
                # parse basic product data
                basic_data = self._parse_product_basic_data(raw_base_product=value)

                # parse extra product data (i.e categories, topics etc.)
                extra_data = self._parse_product_extra_data(
                    raw_base_product=value,
                    raw_product=raw_product,
                )

                # yield product data
                product = {**basic_data, **extra_data}
                yield product

    def parse_product_data(self, response=None, **kwargs):
        """Parse raw product data from a product page script data."""
        raw_product = response.css(PRODUCT_SCRIPT_DATA_SELECTOR).get() or "{}"
        raw_product = json.loads(raw_product)
        raw_product = raw_product.get("props", {})
        raw_product = raw_product.get("apolloState", {})
        return raw_product

    def _parse_product_basic_data(self, raw_base_product={}):
        """Parse product basic details from product script data."""
        product_basic_data = {}

        for basic_key, data_key in PRODUCT_DATA_MAPPINGS.items():
            data_value = raw_base_product.get(basic_key, None)
            product_basic_data[data_key] = data_value

        return product_basic_data

    def _parse_product_extra_data(self, raw_base_product={}, raw_product={}):
        """Parse product extra details from product script data."""
        product_categories = []
        product_topics = []

        for key, value in raw_base_product.items():
            # parse product categories
            if "categories" in key:
                categories = value or []
                categories = [
                    category.get("__ref", None)
                    for category in categories
                    if "__ref" in category
                ]
                categories = [
                    raw_product.get(category, None)
                    for category in categories
                    if category
                ]
                categories = [
                    category.get("displayName", category.get("name", None))
                    for category in categories
                    if category
                ]
                product_categories = list(set(v for v in categories if v))

            # parse product topics
            if "topics" in key:
                topics = (value or {}).get("edges", [])
                topics = [
                    topic.get("node", {}).get("__ref", None)
                    for topic in topics
                    if topic
                ]
                topics = [raw_product.get(topic, None) for topic in topics if topic]
                topics = [topic.get("name", None) for topic in topics if topic]
                product_topics = list(set(v for v in topics if v))

        return {
            "product_categories": product_categories,
            "product_topics": product_topics,
        }
