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


from producthunt_scraper.items import ProductItem


__all__ = ["ValidItemFilterPipeline", "DuplicateItemFilterPipeline"]


class ValidItemFilterPipeline:
    """Valid item filter pipeline."""

    def process_item(self, item, spider):
        """Verify and drop item which does not have required fields."""
        adapter = ItemAdapter(item)
        product_url = adapter.get("product_url")
        if product_url:
            return item
        else:
            raise DropItem(f"""Invalid item found: {item!r}""")


class DuplicateItemFilterPipeline:
    """Duplicates item filter pipeline."""

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        """Check and drop duplicates item."""
        adapter = ItemAdapter(item)

        is_product = isinstance(item, ProductItem)
        item_type = type(item).__name__

        item_id = adapter.get("product_id") if is_product else adapter.get("launch_id")
        item_id = f"""{item_type}/{item_id}"""

        if item_id and item_id in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(item_id)
            return item
