# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# useful for handling different item types with a single interface
from importlib import import_module
from scrapy import signals

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

from fake_useragent import FakeUserAgent

__all__ = ["RandomUserAgentMiddleware", "RetryRandomUserAgentMiddleware"]


class RandomUserAgentMiddleware:
    """Set random ``User-Agent`` header per spider or use a default value from settings."""

    def __init__(self, user_agent=None):
        self.user_agent_fallback = (
            user_agent
            or f"""Scrapy/{import_module("scrapy").__version__} (+https://scrapy.org)"""
        )
        self.user_agent_provider = FakeUserAgent(fallback=self.user_agent_fallback)

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(user_agent=crawler.settings.get("USER_AGENT"))
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, "user_agent", self.user_agent_provider.random)

    def process_request(self, request, spider):
        request.headers.setdefault("User-Agent", self.user_agent_provider.random)


class RetryRandomUserAgentMiddleware(RetryMiddleware):
    """Set random ``User-Agent`` header on request retry."""

    def __init__(self, crawler):
        super(RetryRandomUserAgentMiddleware, self).__init__(crawler.settings)
        self.user_agent_fallback = (
            crawler.settings.get("USER_AGENT")
            or f"""Scrapy/{import_module("scrapy").__version__} (+https://scrapy.org)"""
        )
        self.user_agent_provider = FakeUserAgent(fallback=self.user_agent_fallback)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response

        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            request.headers["User-Agent"] = self.user_agent_provider.random
            return self._retry(request, reason, spider) or response

        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.exceptions_to_retry) and not request.meta.get(
            "dont_retry", False
        ):
            request.headers["User-Agent"] = self.user_agent_provider.random
            return self._retry(request, exception, spider)
