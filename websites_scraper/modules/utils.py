from constants import path_conf_file
from ..modules.exceptions import NoConfFile
import json
from os import path


def get_data_from_conf_file(index, conf_path=path_conf_file):
    """
    Method which returns data from the configuration file. Configuration file is made as list of json objects,
    where each object represents data (css selectors) required to scrape one website. Method returns dictionary object
    with provided index as parameter
    example:
    {
        "website_name": "20Min",
        "website_url": "https://www.20min.ch",
        "index_url_selector": ".teaser_thematiclinks a::attr(href)",
        "index_data_selectors": {},
        "page_url_selector": "h2 a::attr(href)",
        "page_data_selectors": {
            "date": "#story_content .clearfix p span::text",
            "title": ".story_titles h1 span::text",
            "body": ".story_text p::text , .story_titles h3::text"
        }
    }
    """
    if not path.exists(conf_path):
        raise NoConfFile
    with open(conf_path) as f:
        data_str = f.read()
        data = json.loads(data_str)
        return data[int(index)]

