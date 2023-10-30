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
from pathlib import Path

from producthunt_scraper.env import env

# Whether the AjaxCrawlMiddleware will be enabled
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#std-setting-AJAXCRAWL_ENABLED
AJAXCRAWL_ENABLED = env("AJAXCRAWL_ENABLED", False, bool)

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_DEBUG = env("AUTOTHROTTLE_DEBUG", False, bool)
AUTOTHROTTLE_ENABLED = env("AUTOTHROTTLE_ENABLED", False, bool)
AUTOTHROTTLE_MAX_DELAY = env("AUTOTHROTTLE_MAX_DELAY", 60.0, float)
AUTOTHROTTLE_START_DELAY = env("AUTOTHROTTLE_START_DELAY", 5.0, float)
AUTOTHROTTLE_TARGET_CONCURRENCY = env("AUTOTHROTTLE_TARGET_CONCURRENCY", 1.0, float)


# The name of the bot implemented by this Scrapy project
# (also known as the project name). This name will be used for the logging too.
BOT_NAME = "producthunt-scraper"

# Whether the Compression middleware will be enabled.
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#std-setting-COMPRESSION_ENABLED
COMPRESSION_ENABLED = env("COMPRESSION_ENABLED", True, bool)

# Maximum number of concurrent items (per response) to process in parallel in item pipelines.
# See https://docs.scrapy.org/en/latest/topics/settings.html#concurrent-items
CONCURRENT_ITEMS = env("CONCURRENT_ITEMS", 100, int)

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# See https://docs.scrapy.org/en/latest/topics/settings.html#concurrent-requests
CONCURRENT_REQUESTS = env("CONCURRENT_REQUESTS", 16, int)

# The maximum number of concurrent (i.e. simultaneous) requests that will be performed to any single domain.
# See https://docs.scrapy.org/en/latest/topics/settings.html#concurrent-requests-per-domain
CONCURRENT_REQUESTS_PER_DOMAIN = env("CONCURRENT_REQUESTS_PER_DOMAIN", 8, int)

# The maximum number of concurrent (i.e. simultaneous) requests that will be performed to any single IP
# See https://docs.scrapy.org/en/latest/topics/settings.html#concurrent-requests-per-ip
CONCURRENT_REQUESTS_PER_IP = env("CONCURRENT_REQUESTS_PER_IP", 0, int)

# Enables working with sites that require cookies, such as those that use sessions
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.cookies
COOKIES_ENABLED = env("COOKIES_ENABLED", True, bool)
COOKIES_DEBUG = env("COOKIES_DEBUG", False, bool)

# Override the default request headers used for Scrapy HTTP Requests.
# See https://docs.scrapy.org/en/latest/topics/settings.html#default-request-headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": env(
        "ACCEPT", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", str
    ),
    "Accept-Language": env("ACCEPT_LANGUAGE", "en", str),
}

# The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed.
# See https://docs.scrapy.org/en/latest/topics/settings.html#depth-limit
DEPTH_LIMIT = env("DEPTH_LIMIT", 0, int)

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = env("DOWNLOAD_DELAY", 0, int)

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
FEED_TEMPDIR = env("FEED_TEMPDIR", None)
FEED_STORE_EMPTY = env("FEED_STORE_EMPTY", True, bool)
FEED_EXPORT_ENCODING = env("FEED_EXPORT_ENCODING", "utf-8", str)
FEED_EXPORT_BATCH_ITEM_COUNT = env("FEED_EXPORT_BATCH_ITEM_COUNT", 0, int)

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = env("HTTPCACHE_ENABLED", False, bool)
HTTPCACHE_DIR = env("HTTPCACHE_DIR", "httpcache", str)
HTTPCACHE_EXPIRATION_SECS = env("HTTPCACHE_EXPIRATION_SECS", 0, int)

# Whether or not to enable the HttpProxyMiddleware.
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpproxy-enabled
HTTPPROXY_ENABLED = env("HTTPPROXY_ENABLED", True, bool)

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "producthunt_scraper.pipelines.ProducthuntScraperPipeline": 300,
# }

# Enable and configure logging
LOG_ENABLED = env("LOG_ENABLED", True, bool)

# Module where to create new spiders using the genspider command
# See https://docs.scrapy.org/en/latest/topics/settings.html#newspider-module
NEWSPIDER_MODULE = "producthunt_scraper.spiders"

# Whether the Redirect middleware will be enabled
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#redirect-enabled
REDIRECT_ENABLED = env("REDIRECT_ENABLED", True, bool)

# Whether the Retry middleware will be enabled.
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#retry-enabled
RETRY_ENABLED = env("RETRY_ENABLED", True, bool)
RETRY_TIMES = env("RETRY_TIMES", 2, int)  # initial response + 2 retries = 3 requests

# Obey robots.txt rules
# https://docs.scrapy.org/en/latest/topics/settings.html#robotstxt-obey
ROBOTSTXT_OBEY = env("ROBOTSTXT_OBEY", False, bool)

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "producthunt_scraper.middlewares.ProducthuntScraperSpiderMiddleware": 543,
# }

# A list of modules where Scrapy will look for spiders.
# See https://docs.scrapy.org/en/latest/topics/settings.html#spider-modules
SPIDER_MODULES = ["producthunt_scraper.spiders"]

# The default User-Agent to use when crawling (fallback)
# See https://docs.scrapy.org/en/latest/topics/settings.html#user-agent
USER_AGENT = env(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    str,
)
FAKEUSERAGENT_PROVIDERS = [
    "scrapy_fake_useragent.providers.FakeUserAgentProvider",  # this is the first provider we'll try
    "scrapy_fake_useragent.providers.FakerProvider",  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    "scrapy_fake_useragent.providers.FixedUserAgentProvider",  # fall back to USER_AGENT value
]

# Disable Telnet Console (enabled by default)
# See https://docs.scrapy.org/en/latest/topics/settings.html#telnetconsole-enabled
TELNETCONSOLE_ENABLED = env("TELNETCONSOLE_ENABLED", True, bool)

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
