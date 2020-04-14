import scrapy
import json
from os import path
from ..items import WebsitesScraperItem
from ..modules.utils import get_data_from_conf_file
from constants import path_jsonl_file


class NewsSpider(scrapy.Spider):
    name = 'news'

    def __init__(self, data_index):
        super().__init__()
        self.data_index = data_index
        self.__website_data = get_data_from_conf_file(data_index)
        self.start_urls = [self.__website_data.get('website_url')]
        path_to_jsonl = f"{path_jsonl_file}/{self.__website_data.get('website_name')}.jsonl"
        self.__urls = self.__init_url_list_from_file(path_to_jsonl)
        self.__BASE_URL = self.__website_data.get('website_url')

    def parse(self, response):
        index_page_urls = response.css(self.__website_data.get('index_url_selector')).extract()
        for url in self.__get_url_to_scrape(index_page_urls):
            yield scrapy.Request(url, callback=self.parse_page, meta={'page_url': url})

    def parse_page(self, response):
        """
        This function scrapes main text from the web page,
        after that finds all links which are not found in global list of links
        because we dont want to scrape again the page that is already scraped,
        and at the end do recursively call to this function (parse page) f
        or every link found on this web page, which is not already scraped
        """

        page_url_selector = self.__website_data.get('page_url_selector')
        scraped_urls = response.css(page_url_selector).extract()

        for url in self.__get_url_to_scrape(scraped_urls):
            yield scrapy.Request(url, callback=self.parse_page, meta={'page_url': url})

        yield self.get_page_items(response)

    def get_page_items(self, response):
        page_data_selector = self.__website_data.get('page_data_selectors')
        page_url = response.meta.get('page_url')

        items = WebsitesScraperItem()
        items['page_url'] = page_url
        for item_name, item_selector in page_data_selector.items():
            items[item_name] = response.css(item_selector).extract()

        if items['body']:
            return items
        else:
            return None

    def __init_url_list_from_file(self, path_to_file):
        urls = list()
        if path.exists(path_to_file):
            with open(path_to_file) as f:
                urls = [json.loads(line).get('page_url') for line in f]
        return list(set(urls))

    def __create_absolute_url(self, url):
        if url.startswith(self.__BASE_URL):
            absolute_url = url.split('?')[0]
        elif url.startswith("/"):
            absolute_url = self.__BASE_URL + url
            absolute_url = absolute_url.split('?')[0]
        else:
            absolute_url = None
        return absolute_url

    def __get_url_to_scrape(self, urls):
        for url in urls:
            absolute_url = self.__create_absolute_url(url)
            if not absolute_url or absolute_url in self.__urls:
                continue
            self.__urls.append(absolute_url)
            yield absolute_url
