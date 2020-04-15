import subprocess
import json
from os import path
from websites_scraper.modules.exceptions import NoConfFile
from constants import path_conf_file


class ScraperEngine:

    def crawler_inputs(self, conf_path):
        """
        Generator method which yields objects from the configuration file
        """
        if not path.exists(conf_path):
            raise NoConfFile
        with open(conf_path) as f:
            data_str = f.read()
            data = json.loads(data_str)
            for website_data in data:
                yield website_data

    def start_crawlers(self, conf_path=path_conf_file):
        """
        Method used to run web scraper. It loops trough every object in the configuration file and runs scraper for each
        of them.
        """
        try:
            for data_index, website_data in enumerate(self.crawler_inputs(conf_path)):
                subprocess.run(f'scrapy crawl news -a data_index={data_index} -o '
                               f'{website_data.get("website_name")}.jsonl -t jsonlines', shell=True)
        except NoConfFile:
            raise NoConfFile(f"ERROR: Configuration file with the path {conf_path} does not exist!")

"""
Creating an object of scraper engine and starting all crawlers
"""
se = ScraperEngine()
se.start_crawlers()
