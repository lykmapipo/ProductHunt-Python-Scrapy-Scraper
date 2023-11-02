# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from dataclasses import dataclass, field
from typing import Optional, List


__all__ = ["ProductItem", "ProductLaunchItem"]


@dataclass
class ProductItem:
    """Product item."""

    product_id: Optional[str] = field(default=None)
    product_slug: Optional[str] = field(default=None)
    product_name: Optional[str] = field(default=None)
    product_tagline: Optional[str] = field(default=None)
    product_description: Optional[str] = field(default=None)
    product_url: Optional[str] = field(default=None)
    product_website_url: Optional[str] = field(default=None)
    product_rating: Optional[float] = field(default=None)
    product_followers_count: Optional[int] = field(default=None)
    product_total_votes_count: Optional[int] = field(default=None)
    product_reviewers_count: Optional[int] = field(default=None)
    product_reviews_count: Optional[int] = field(default=None)
    product_posts_count: Optional[int] = field(default=None)
    product_stacks_count: Optional[int] = field(default=None)
    product_alternatives_count: Optional[int] = field(default=None)
    product_tips_count: Optional[int] = field(default=None)
    product_addons_count: Optional[int] = field(default=None)
    product_platforms: Optional[List[str]] = field(default=None)
    product_categories: Optional[List[str]] = field(default=None)
    product_topics: Optional[List[str]] = field(default=None)


@dataclass
class ProductLaunchItem:
    """ProductLaunch item."""

    launch_id: Optional[str] = field(default=None)
    launch_slug: Optional[str] = field(default=None)
    launch_name: Optional[str] = field(default=None)
    launch_tagline: Optional[str] = field(default=None)
    launch_description: Optional[str] = field(default=None)
    launch_url: Optional[str] = field(default=None)
    launch_votes_count: Optional[int] = field(default=None)
    launch_comments_count: Optional[int] = field(default=None)
    launch_daily_rank: Optional[int] = field(default=None)
    launch_weekly_rank: Optional[int] = field(default=None)
    launch_created_at: Optional[str] = field(default=None)
    launch_featured_at: Optional[str] = field(default=None)
    launch_updated_at: Optional[str] = field(default=None)
    product_id: Optional[str] = field(default=None)
    product_name: Optional[str] = field(default=None)
    product_url: Optional[str] = field(default=None)
