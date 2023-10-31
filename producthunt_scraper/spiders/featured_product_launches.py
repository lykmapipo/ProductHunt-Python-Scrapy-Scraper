"""Featured product launches scraping spiders.

How it works:

This spider, do:
    1. Scrape url of top featured product launches from producthunt home page.
    2. Scrape information for each featured product launch url
    3. Save batches of featured product launches per day.

Usage:

To scrape `featured product launches`, run:
>>> scrapy crawl featured-product-launches
"""

import json
from datetime import datetime

import scrapy

from producthunt_scraper.settings import (
    BASE_DATA_DIR,
    PRODUCTHUNT_ALLOWED_DOMAINS,
    PRODUCTHUNT_POSTS_BASE_URL,
    PRODUCTHUNT_BASE_URL,
)

# selectors
FEATURED_LAUNCH_URL_SELECTOR = "div[data-test=homepage-section-0] div[data-test*=post-item] a[href*=posts]::attr(href)"
FEATURED_LAUNCH_SCRIPT_DATA_SELECTOR = "script#__NEXT_DATA__::text"

# mappings
FEATURED_LAUNCH_DATA_MAPPINGS = {
    "id": "launch_id",
    "slug": "launch_slug",
    "name": "launch_name",
    "tagline": "launch_tagline",
    "description": "launch_description",
    "url": "launch_url",
    "votesCount": "launch_votes_count",
    "commentsCount": "launch_comments_count",
    "dailyRank": "launch_daily_rank",
    "weeklyRank": "launch_weekly_rank",
    "createdAt": "launch_created_at",
    "featuredAt": "launch_featured_at",
    "updatedAt": "launch_updated_at",
}


class FeaturedProductLaunchesSpider(scrapy.Spider):
    """Scrape top featured product launches."""

    name = "featured-product-launches"
    allowed_domains = PRODUCTHUNT_ALLOWED_DOMAINS
    start_urls = [PRODUCTHUNT_BASE_URL]

    data_dir = BASE_DATA_DIR
    last_scraped_date = datetime.utcnow().date()

    custom_settings = {
        "FEEDS": {
            "%(data_dir)s/%(name)s/date=%(last_scraped_date)s/part-%(batch_id)d.jsonl": {
                "format": "jsonlines",
                "overwrite": True,
            }
        },
    }

    def __init__(self, *args, **kwargs):
        super(FeaturedProductLaunchesSpider, self).__init__(*args, **kwargs)
        self.last_scraped_date = datetime.utcnow().date()

    def parse(self, response=None, **kwargs):
        # check url type
        response_url = str(response.url)
        is_base_url = response_url == PRODUCTHUNT_BASE_URL
        is_post_url = response_url.startswith(PRODUCTHUNT_POSTS_BASE_URL)

        # ignore unknown urls
        if not is_base_url and not is_post_url:
            return

        # parse home page and follow each featured product launch url
        if is_base_url:
            yield from self.parse_featured_product_launches_page(
                response=response,
                **kwargs,
            )

        # parse product launch page and yield product launch data
        if is_post_url:
            yield from self.parse_featured_product_launch_page(
                response=response,
                **kwargs,
            )

    def parse_featured_product_launches_page(self, response=None, **kwargs):
        """Parse producthunt home page and follow featured product launch urls."""

        # parse featured product launch urls
        urls = response.css(FEATURED_LAUNCH_URL_SELECTOR)
        urls = set(urls.getall())

        # follow each featured product launch page
        for url in urls:
            yield response.follow(url, self.parse)

    def parse_featured_product_launch_page(self, response=None, **kwargs):
        """Parse featured product launch page and yield a launch item."""

        # parse product launch raw data
        raw_data = self.parse_featured_product_launch_data(
            response=response,
            **kwargs,
        )

        # collect, transform and format product launch data
        # from raw product launch data
        for raw_data_key, raw_data_value in raw_data.items():
            if (
                "Post" in raw_data_key
                and "product" in raw_data_value
                and "structuredData" in raw_data_value
            ):
                # collect basic data
                data = {
                    data_key: raw_data_value.get(raw_key, None)
                    for raw_key, data_key in FEATURED_LAUNCH_DATA_MAPPINGS.items()
                }

                # collect and link product details
                product_ref = raw_data_value.get("product", {})
                product_ref = product_ref.get("__ref", "").strip()
                if product_ref:
                    product = raw_data.get(product_ref, {})
                    data["product_id"] = product.get("id", None)
                    data["product_name"] = product.get("name", None)
                    data["product_url"] = product.get("url", None)

                # TODO: collect and link extra data

                yield data

    def parse_featured_product_launch_data(self, response=None, **kwargs):
        """Parse raw featured product launch data from a page script data."""

        # parse data
        data = response.css(FEATURED_LAUNCH_SCRIPT_DATA_SELECTOR)
        data = data.get() or "{}"

        # cast and select data
        data = json.loads(data)
        data = data.get("props", {}).get("apolloState", {})

        return data
