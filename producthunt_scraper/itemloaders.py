# Define here the loaders to populate items you scraped
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/loaders.html


from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

__all__ = ["ProductItemLoader", "ProductLaunchItemLoader"]


class ProductItemLoader(ItemLoader):
    """Product item loader."""

    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    product_rating_in = MapCompose(float)
    product_followers_count_in = MapCompose(int)
    product_total_votes_count_in = MapCompose(int)
    product_reviewers_count_in = MapCompose(int)
    product_reviews_count_in = MapCompose(int)
    product_posts_count_in = MapCompose(int)
    product_stacks_count_in = MapCompose(int)
    product_alternatives_count_in = MapCompose(int)
    product_tips_count_in = MapCompose(int)
    product_addons_count_in = MapCompose(int)

    product_platforms_out = Identity()
    product_categories_out = Identity()
    product_topics_out = Identity()


class ProductLaunchItemLoader(ItemLoader):
    """ProductLaunch item loader."""

    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    launch_votes_count_in = MapCompose(int)
    launch_comments_count_in = MapCompose(int)
    launch_daily_rank_in = MapCompose(int)
    launch_weekly_rank_in = MapCompose(int)

    launch_topics_out = Identity()
