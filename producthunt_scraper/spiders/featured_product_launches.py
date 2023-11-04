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

from datetime import datetime

import scrapy

from producthunt_scraper.itemloaders import ProductLaunchItemLoader
from producthunt_scraper.items import ProductLaunchItem
from producthunt_scraper.settings import (
    BASE_DATA_DIR,
    PRODUCTHUNT_ALLOWED_DOMAINS,
    PRODUCTHUNT_BASE_URL,
    PRODUCTHUNT_POSTS_BASE_URL,
)
from producthunt_scraper.spiders.mixins import PageScriptDataMixin

# selectors
FEATURED_LAUNCH_URL_SELECTOR = "div[data-test=homepage-section-0] div[data-test*=post-item] a[href*=posts]::attr(href)"

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


__all__ = ["FeaturedProductLaunchesSpider"]


class FeaturedProductLaunchesSpider(scrapy.Spider, PageScriptDataMixin):
    """Scrape top featured product launches."""

    name = "featured-product-launches"
    allowed_domains = PRODUCTHUNT_ALLOWED_DOMAINS
    data_dir = BASE_DATA_DIR
    last_scraped_date = datetime.utcnow().date()

    def __init__(self, *args, **kwargs):
        super(FeaturedProductLaunchesSpider, self).__init__(*args, **kwargs)
        self.last_scraped_date = datetime.utcnow().date()

    def start_requests(self):
        """Generate first requests to crawl for this spider."""
        start_urls = [PRODUCTHUNT_BASE_URL]
        for start_url in start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse, meta={})

    def parse(self, response=None, **kwargs):
        """Process responses and return scraped data and/or more URLs to follow."""
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
        raw_data = self.parse_page_script_data(response=response, **kwargs)

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
                # TODO: ensure launch with products
                product_ref = raw_data_value.get("product") or {}
                product_ref = product_ref.get("__ref", "").strip()
                if product_ref:
                    product = raw_data.get(product_ref, {})
                    data["product_id"] = product.get("id", None)
                    data["product_name"] = product.get("name", None)
                    data["product_url"] = product.get("url", None)

                # TODO: collect and link extra data

                # load and yield an product launch item
                item_loader = ProductLaunchItemLoader(item=ProductLaunchItem())
                item_loader.add_value(None, data)
                item = item_loader.load_item()
                yield item
