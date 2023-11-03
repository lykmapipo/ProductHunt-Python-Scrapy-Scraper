# ProductHunt-Python-Scrapy-Scraper

Python [Scrapy](https://github.com/scrapy/scrapy) spiders that scrapes [products](#product) and [launches](#launch) data from [producthunt.com](https://www.producthunt.com).

## Features
- Item [schema](https://github.com/lykmapipo/ProductHunt-Python-Scrapy-Scraper/blob/main/producthunt_scraper/items.py) for `trending products` and `featured product launches` defined using `dataclass`
- Item [pipelines](https://github.com/lykmapipo/ProductHunt-Python-Scrapy-Scraper/blob/main/producthunt_scraper/pipelines.py) to `normalize`, `validate` and `drop` duplicate items.
- [Download middlewares](https://github.com/lykmapipo/ProductHunt-Python-Scrapy-Scraper/blob/main/producthunt_scraper/middlewares.py) to random user agents.

## Requirements

- [Python 3.8+](https://www.python.org/)
- [pip 23.3+](https://github.com/pypa/pip)
- [Scrapy 2.11+](https://github.com/scrapy/scrapy)

## Usage

- Clone this repository

- Install all dependencies

```sh
pip install -e .
```

- To scrape `featured product launches`, run:

```sh
scrapy crawl featured-product-launches
```

- To scrape `trending products`, run:

```sh
scrapy crawl trending-products
```

## Data Exploration
The scraped data is saved in [`jsonline`](https://jsonlines.org/) format and may be found at `./data/<spider-name>/date=<scraped-date>`. Where `spider-name` is a name of the spider e.g `featured-product-launches` and `scraped-date` is the date when the spider was runned.

Example, for `featured-product-launches` spider runned on `2023-10-24`, then the data may be found at `./data/featured-product-launches/date=2023-10-24`.

- Explore part of the data using `pandas`, use:
```python
import pandas as pd

# replace the date part with your scraping date
# file = "./data/trending-products/date=2023-10-24/part-1.jsonl"
file = "./data/featured-product-launches/date=2023-10-24/part-1.jsonl"
df = pd.read_json(file, lines=True)

df.info()
```

- To explore all the data using `pandas`, use:
```python
import glob
import pandas as pd

# replace the date part with your scraping date
# files = glob.glob("./data/trending-products/date=2023-10-24/*.jsonl")
files = glob.glob("./data/featured-product-launches/date=2023-10-24/*.jsonl")
dfs = [pd.read_json(file, lines=True) for file in files]
df = pd.concat(dfs, ignore_index=True)

df.info()
```

## Contribute

It will be nice, if you open an issue first so that we can know what is going on, then, fork this repo and push in your ideas. Do not forget to add a bit of test(s) of what value you adding.

## Questions/Contacts

lallyelias87@gmail.com, or open a GitHub issue


## Schema

### Launch

The `featured-product-launches` spider extract the following ``launch`` fields from featured product launches pages:

```python
@dataclass
class ProductLaunchItem:
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
```

### Product

The `trending-products` spider extract the following ``product`` fields from trending product pages:

```python
@dataclass
class ProductItem:
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
```

## Licence

The MIT License (MIT)

Copyright (c) lykmapipo & Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
