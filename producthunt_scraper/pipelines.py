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


__all__ = ["ValidItemFilterPipeline"]


class ValidItemFilterPipeline:
    def process_item(self, item, spider):
        """Verify and allow item which has all required fields."""
        adapter = ItemAdapter(item)
        product_url = adapter.get("product_url")
        if product_url:
            return item
        else:
            raise DropItem(f"""Invalid item found: {item!r}""")
