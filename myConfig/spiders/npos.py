import re
import scrapy
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor

emails_re = re.compile(r"\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b", re.IGNORECASE)


class GrantsSpider(scrapy.Spider):
    name = "npos"
    reported_links = []
    link_extractor = LinkExtractor(unique=True)
    npos = {}

    async def errback_close_page(self, failure):
        self.logger.error(f'Error processing page: {repr(failure)}')
        if "playwright_page" in failure.request.meta:
            page = failure.request.meta["playwright_page"]
            if page:
                await page.close()
                self.logger.info(f"Closed page due to error: {page}")
        raise CloseSpider(reason='Forbidden by robots.txt')

    def start_requests(self):
        if not self.start_urls and hasattr(self, "start_url"):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            npo = self.npos[url]
            logging.info("### crawl: %s", url)
            yield scrapy.Request(
                url, callback=self.my_parse, dont_filter=True,meta={"playwright": True, "playwright_include_page": True,'dont_redirect': True}, cb_kwargs={"npo": npo},
                errback=self.errback_close_page
            )

    async def my_parse(self, response, npo):
        page = response.meta["playwright_page"]
        self.reported_links.append(response.url)
        try:
            _ = response.text
        except AttributeError as exc:
            logging.debug(f"Skipping {response.url}: {exc}")
            await page.close()
            return

        body, match = self.is_page(response, None)
        for email in emails_re.findall(body):
            yield {
                "ein": npo["ein"],
                "name": npo["name"],
                "type": npo["type"],
                "msg": "link-email",
                "match": email,
                "text": email,
                "url": response.url,
                "timestamp": datetime.utcnow(),
            }

        for link in response.xpath("//a"):
            href = link.xpath("./@href").get()

            if not href or href.startswith("javascript:") or href.startswith("#"):
                continue

            if not href.startswith("http"):
                href = response.urljoin(href)

            if href not in self.reported_links:
                yield scrapy.Request(
                    href, callback=self.my_parse,
                    meta={"playwright": True, "playwright_include_page": True, 'dont_redirect': True},
                    cb_kwargs={"npo": npo},
                    errback=self.errback_close_page
                )

        await page.close()

    def is_page(self, response, re_expression):
        sel = scrapy.Selector(response)
        sel.xpath("//head").remove()
        sel.xpath("//header").remove()
        # sel.xpath("//footer").remove()
        sel.xpath("//navbar").remove()
        sel.xpath("//a").remove()
        body = sel.get()
        bs_doc = BeautifulSoup(body, features="lxml").get_text(strip=True, separator=" ")
        if not re_expression:
            return bs_doc, None
        if re_expression.search(bs_doc):
            matches = list(set(list(re.findall(re_expression, bs_doc))[0]))
            if "" in matches:
                matches.remove("")
            return bs_doc, matches
        return None, None