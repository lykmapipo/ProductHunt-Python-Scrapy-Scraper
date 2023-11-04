# Define your item pipelines here to manipulate (validate and process) the data we have scraped before saving it.
#
# Use item pipelines to do:
#   * Cast item value to their corresponding storage type i.e int, float, etc
#   * Drop incomplete item
#   * Drop duplicate item
#   * etc
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from producthunt_scraper.items import ProductItem, ProductLaunchItem

__all__ = [
    "NormalizeItemPipeline",
    "ValidItemFilterPipeline",
    "DuplicateItemFilterPipeline",
]


class NormalizeItemPipeline:
    """Normalize item pipeline."""

    def process_item(self, item, spider):
        """Restructure and reformat item."""
        item_adapter = ItemAdapter(item)

        is_product_launch_item = isinstance(item, ProductLaunchItem)
        is_product_item = isinstance(item, ProductItem)
        if is_product_item:
            product_categories = item_adapter.get("product_categories")
            if not product_categories:
                item_adapter["product_categories"] = None

            product_topics = item_adapter.get("product_topics")
            if not product_topics:
                item_adapter["product_topics"] = None

        if is_product_launch_item:
            launch_topics = item_adapter.get("launch_topics")
            if not launch_topics:
                item_adapter["launch_topics"] = None

        return item


class ValidItemFilterPipeline:
    """Valid item filter pipeline."""

    def process_item(self, item, spider):
        """Verify and drop item which does not have required fields."""
        item_adapter = ItemAdapter(item)
        product_url = item_adapter.get("product_url")
        if product_url:
            return item
        else:
            raise DropItem(f"""Invalid item found: {item!r}""")


class DuplicateItemFilterPipeline:
    """Duplicate item filter pipeline."""

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        """Check and drop duplicates item."""
        item_adapter = ItemAdapter(item)

        is_product_item = isinstance(item, ProductItem)
        item_type = type(item).__name__

        item_id = (
            item_adapter.get("product_id")
            if is_product_item
            else item_adapter.get("launch_id")
        )
        item_id = f"""{item_type}/{item_id}"""

        if item_id and item_id in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(item_id)
            return item
