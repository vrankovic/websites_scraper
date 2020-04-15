import scrapy
import json
from os import path
from ..items import WebsitesScraperItem
from ..modules.utils import get_data_from_conf_file
from constants import jsonl_file_directory


class WebsitesSpider(scrapy.Spider):
    name = 'news'

    def __init__(self, data_index):
        super().__init__()
        self.data_index = data_index
        self.__website_data = get_data_from_conf_file(data_index)
        self.start_urls = [self.__website_data.get('website_url')]
        path_to_jsonl = f"{jsonl_file_directory}/{self.__website_data.get('website_name')}.jsonl"
        self.__urls = self.__init_url_list_from_file(path_to_jsonl)
        self.__BASE_URL = self.__website_data.get('website_url')

    def parse(self, response):
        """
        Method inherited from scrapy.Spider class and it gets response as the crawled page from self.start_urls.
        It selects all urls from the crawled page defined by css selector in configuration_data.conf file and
        recursively crawls web pages for every url.
        """
        index_page_urls = response.css(self.__website_data.get('index_url_selector')).extract()
        for url in self.__get_url_to_scrape(index_page_urls):
            yield scrapy.Request(url, callback=self.parse_page, meta={'page_url': url})

    def parse_page(self, response):
        """
        Method which gets crawled web page through response parameter, scrapes all urls from it, do recursive call to
        this message for every scraped url and yields text data found in this page
        """
        page_url_selector = self.__website_data.get('page_url_selector')
        scraped_urls = response.css(page_url_selector).extract()

        for url in self.__get_url_to_scrape(scraped_urls):
            yield scrapy.Request(url, callback=self.parse_page, meta={'page_url': url})

        yield self.get_page_items(response)

    def get_page_items(self, response):
        """
        Method used to create WebsiteScraperItem and return it if body field is not empty.
        """
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
        """
        Method which is used to get names of all web pages that are already scraped and are stored in jsonl file.
        This is done because the data that is already scraped doesn't need to be scraped again.
        """
        urls = list()
        if path.exists(path_to_file):
            with open(path_to_file) as f:
                urls = [json.loads(line).get('page_url') for line in f]
        return list(set(urls))

    def __create_absolute_url(self, url):
        """
        Method used to create absolute url for every web page.
        """
        if url.startswith(self.__BASE_URL):
            absolute_url = url.split('?')[0]
        elif url.startswith("/"):
            absolute_url = self.__BASE_URL + url
            absolute_url = absolute_url.split('?')[0]
        else:
            absolute_url = None
        return absolute_url

    def __get_url_to_scrape(self, urls):
        """
        Generator which yields only urls that are not found in self.__urls which represents the list of already scraped
        urls. If the url is not scraped, it is appended to self.__urls list and yielded.
        """
        for url in urls:
            absolute_url = self.__create_absolute_url(url)
            if not absolute_url or absolute_url in self.__urls:
                continue
            self.__urls.append(absolute_url)
            yield absolute_url
