""""
Scrapy settings for producthunt_scraper project

For simplicity, this file contains only settings considered important or
commonly used. You can find more settings consulting the documentation:

* https://docs.scrapy.org/en/latest/topics/settings.html
* https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
* https://docs.scrapy.org/en/latest/topics/spider-middleware.html

Scrapy developers, if you add a setting here remember to:

* add it in alphabetical order
* group similar settings without leaving blank lines
* add project defined/custom settings last

"""
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

# find .env and load up the entries as environment variables
load_dotenv(find_dotenv())

# Whether the AjaxCrawlMiddleware will be enabled
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#std-setting-AJAXCRAWL_ENABLED
AJAXCRAWL_ENABLED = bool(os.environ.get("AJAXCRAWL_ENABLED", False))

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_DEBUG = bool(os.environ.get("AUTOTHROTTLE_DEBUG", False))
AUTOTHROTTLE_ENABLED = bool(os.environ.get("AUTOTHROTTLE_ENABLED", False))
AUTOTHROTTLE_MAX_DELAY = float(os.environ.get("AUTOTHROTTLE_MAX_DELAY", 60.0))
AUTOTHROTTLE_START_DELAY = float(os.environ.get("AUTOTHROTTLE_START_DELAY", 5.0))
AUTOTHROTTLE_TARGET_CONCURRENCY = float(
    os.environ.get("AUTOTHROTTLE_TARGET_CONCURRENCY", 1.0)
)


# The name of the bot implemented by this Scrapy project
# (also known as the project name). This name will be used for the logging too.
BOT_NAME = "producthunt-scraper"

# Whether the Compression middleware will be enabled.
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#std-setting-COMPRESSION_ENABLED
COMPRESSION_ENABLED = bool(os.environ.get("COMPRESSION_ENABLED", True))

# Maximum number of concurrent items (per response) to process in parallel in item pipelines.
# See https://docs.scrapy.org/en/latest/topics/settings.html#concurrent-items
CONCURRENT_ITEMS = int(os.environ.get("CONCURRENT_ITEMS", 100))

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# See https://docs.scrapy.org/en/latest/topics/settings.html#concurrent-requests
CONCURRENT_REQUESTS = int(os.environ.get("CONCURRENT_REQUESTS", 16))
# The maximum number of concurrent (i.e. simultaneous) requests that will be performed to any single domain.
# See https://docs.scrapy.org/en/latest/topics/settings.html#concurrent-requests-per-domain
CONCURRENT_REQUESTS_PER_DOMAIN = int(
    os.environ.get("CONCURRENT_REQUESTS_PER_DOMAIN", 8)
)
# The maximum number of concurrent (i.e. simultaneous) requests that will be performed to any single IP
# See https://docs.scrapy.org/en/latest/topics/settings.html#concurrent-requests-per-ip
CONCURRENT_REQUESTS_PER_IP = int(os.environ.get("CONCURRENT_REQUESTS_PER_IP", 0))

# Enables working with sites that require cookies, such as those that use sessions
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.cookies
COOKIES_ENABLED = bool(os.environ.get("COOKIES_ENABLED", True))
COOKIES_DEBUG = bool(os.environ.get("COOKIES_DEBUG", False))

# Override the default request headers used for Scrapy HTTP Requests.
# See https://docs.scrapy.org/en/latest/topics/settings.html#default-request-headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": str(
        os.environ.get(
            "ACCEPT", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        )
    ),
    "Accept-Language": str(os.environ.get("ACCEPT_LANGUAGE", "en")),
}

# The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed.
# See https://docs.scrapy.org/en/latest/topics/settings.html#depth-limit
DEPTH_LIMIT = int(os.environ.get("DEPTH_LIMIT", 0))

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = float(os.environ.get("DOWNLOAD_DELAY", 0))

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
    "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
    # "producthunt_scraper.middlewares.ProducthuntScraperDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Feed exports configurations
# See https://docs.scrapy.org/en/latest/topics/feed-exports.html
FEED_TEMPDIR = str(os.environ.get("FEED_TEMPDIR"))
FEED_STORE_EMPTY = bool(os.environ.get("FEED_STORE_EMPTY", True))
FEED_EXPORT_ENCODING = str(os.environ.get("FEED_EXPORT_ENCODING", "utf-8"))
FEED_EXPORT_BATCH_ITEM_COUNT = int(os.environ.get("FEED_EXPORT_BATCH_ITEM_COUNT", 0))

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = bool(os.environ.get("HTTPCACHE_ENABLED", False))
HTTPCACHE_DIR = str(os.environ.get("HTTPCACHE_DIR", "httpcache"))
HTTPCACHE_EXPIRATION_SECS = int(os.environ.get("HTTPCACHE_EXPIRATION_SECS", 0))

# Whether or not to enable the HttpProxyMiddleware.
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpproxy-enabled
HTTPPROXY_ENABLED = bool(os.environ.get("HTTPPROXY_ENABLED", True))

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "producthunt_scraper.pipelines.ProducthuntScraperPipeline": 300,
# }

# Enable and configure logging
LOG_ENABLED = bool(os.environ.get("LOG_ENABLED", True))

# Module where to create new spiders using the genspider command
# See https://docs.scrapy.org/en/latest/topics/settings.html#newspider-module
NEWSPIDER_MODULE = "producthunt_scraper.spiders"

# Whether the Redirect middleware will be enabled
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#redirect-enabled
REDIRECT_ENABLED = bool(os.environ.get("REDIRECT_ENABLED", True))

# Whether the Retry middleware will be enabled.
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#retry-enabled
RETRY_ENABLED = bool(os.environ.get("RETRY_ENABLED", True))
RETRY_TIMES = int(
    os.environ.get("RETRY_TIMES", 2)
)  # initial response + 2 retries = 3 requests

# Obey robots.txt rules
# https://docs.scrapy.org/en/latest/topics/settings.html#robotstxt-obey
ROBOTSTXT_OBEY = bool(os.environ.get("ROBOTSTXT_OBEY", False))

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "producthunt_scraper.middlewares.ProducthuntScraperSpiderMiddleware": 543,
# }

# A list of modules where Scrapy will look for spiders.
# See https://docs.scrapy.org/en/latest/topics/settings.html#spider-modules
SPIDER_MODULES = ["producthunt_scraper.spiders"]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = str(
    os.environ.get(
        "USER_AGENT",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    )
)  # noqa
FAKEUSERAGENT_PROVIDERS = [
    "scrapy_fake_useragent.providers.FakeUserAgentProvider",  # this is the first provider we'll try
    "scrapy_fake_useragent.providers.FakerProvider",  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    "scrapy_fake_useragent.providers.FixedUserAgentProvider",  # fall back to USER_AGENT value
]

# Disable Telnet Console (enabled by default)
# See https://docs.scrapy.org/en/latest/topics/settings.html#telnetconsole-enabled
TELNETCONSOLE_ENABLED = bool(os.environ.get("TELNETCONSOLE_ENABLED", True))

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Custom settings for the producthunt project
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DATA_DIR = BASE_DIR / "data"

PRODUCTHUNT_ALLOWED_DOMAINS = ["producthunt.com"]
PRODUCTHUNT_BASE_URL = "https://www.producthunt.com"
PRODUCTHUNT_TOPICS_BASE_URL = f"""{PRODUCTHUNT_BASE_URL}/topics"""
PRODUCTHUNT_PRODUCTS_BASE_URL = f"""{PRODUCTHUNT_BASE_URL}/products"""
PRODUCTHUNT_PRODUCT_SORT_FILTERS = [
    "best_rated",
    "most_followed",
    "most_recent",
]
