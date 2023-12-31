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

from datetime import datetime
from urllib.parse import urlencode

import scrapy

from producthunt_scraper.itemloaders import ProductItemLoader
from producthunt_scraper.items import ProductItem
from producthunt_scraper.settings import (
    BASE_DATA_DIR,
    PRODUCTHUNT_ALLOWED_DOMAINS,
    PRODUCTHUNT_PRODUCT_SORT_FILTERS,
    PRODUCTHUNT_PRODUCTS_BASE_URL,
    PRODUCTHUNT_TOPICS_BASE_URL,
)
from producthunt_scraper.spiders.mixins import PageScriptDataMixin

# selectors
TRENDING_TOPIC_URL_SELECTOR = "div[data-test=trending-topics-card] a::attr(href)"
TRENDING_PRODUCT_URL_SELECTOR = "main[class=layoutMain] ul > div > div > a::attr(href)"

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


__all__ = ["TrendingProductsSpider"]


class TrendingProductsSpider(scrapy.Spider, PageScriptDataMixin):
    """Scrape top trending products from trending topics."""

    name = "trending-products"
    allowed_domains = PRODUCTHUNT_ALLOWED_DOMAINS
    data_dir = BASE_DATA_DIR
    last_scraped_date = datetime.utcnow().date()

    def __init__(self, *args, **kwargs):
        super(TrendingProductsSpider, self).__init__(*args, **kwargs)
        self.last_scraped_date = datetime.utcnow().date()

    def start_requests(self):
        """Generate first requests to crawl for this spider."""
        start_urls = [PRODUCTHUNT_TOPICS_BASE_URL]
        for start_url in start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse, meta={})

    def parse(self, response=None, **kwargs):
        """Process response and return scraped data and/or more URLs to follow."""
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
        raw_product = self.parse_script_data(response=response, **kwargs)
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

                # load and yield an product item
                item_loader = ProductItemLoader(item=ProductItem())
                item_loader.add_value(None, product)
                item = item_loader.load_item()
                yield item

    def _parse_product_basic_data(self, raw_base_product=None):
        """Parse product basic details from product script data."""
        raw_base_product = raw_base_product or {}
        product_basic_data = {}

        for basic_key, data_key in PRODUCT_DATA_MAPPINGS.items():
            data_value = raw_base_product.get(basic_key, None)
            product_basic_data[data_key] = data_value

        return product_basic_data

    def _parse_product_extra_data(self, raw_base_product=None, raw_product=None):
        """Parse product extra details from product script data."""
        raw_base_product = raw_base_product or {}
        raw_product = raw_product or {}

        # parse product topics
        topic_keys = self.parse_ref_keys(key="topics", source=raw_base_product)
        topics = self.parse_ref_values(*topic_keys, source=raw_product)
        topics = {topic.get("name") for topic in topics}
        topics = list({topic for topic in topics if topic})

        # parse product categories
        category_keys = self.parse_ref_keys(key="categories", source=raw_base_product)
        categories = self.parse_ref_values(*category_keys, source=raw_product)
        categories = {category.get("name") for category in categories}
        categories = list({category for category in categories if category})

        return {
            "product_categories": categories,
            "product_topics": topics,
        }
