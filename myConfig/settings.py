
BOT_NAME = "test"

SPIDER_MODULES = ["myConfig.spiders"]
NEWSPIDER_MODULE = "myConfig.spiders"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 0.3
CONCURRENT_REQUESTS_PER_DOMAIN = 4
CONCURRENT_REQUESTS_PER_IP = 4
TELNETCONSOLE_ENABLED = False
HTTPERROR_ALLOWED_CODES = [403, 401, 400, 504, 404, 429, 503]
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 30 * 1000,  # 30 seconds
}
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 4
PLAYWRIGHT_BROWSER_TYPE = "chromium"
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 900,
    'myConfig.middlewares.RobotsTxtMiddleware': 543,
}

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DEPTH_LIMIT = 2
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"
SCHEDULER_MEMORY_QUEUE = "scrapy.squeues.FifoMemoryQueue"
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 180000  # 180s
CLOSESPIDER_TIMEOUT = 300
CLOSESPIDER_ITEMCOUNT = 300
CLOSESPIDER_PAGECOUNT = 300
DNS_TIMEOUT = 3
RETRY_ENABLED = False
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 120
DUPEFILTER_DEBUG = True

LOG_LEVEL = 'INFO'
