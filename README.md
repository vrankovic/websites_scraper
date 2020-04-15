Websites Scraper is the tool developed to help scraping text data from websites. It allows users to define css selectors
for the desired websites and scrape data by running one command. Input file is configuration file called 
```configuration_data.conf``` and output files are files in jsonl format which contains scraped data defined with css 
selectors in configuration file. Css selectors should be defined by the user in the configuration file 
The configuration file should be defined by user as in the following example:
```
[
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
    },
    {
        "website_name": "scilogs.spektrum",
        "website_url": "https://scilogs.spektrum.de",
        "index_url_selector": "a.post__permalink::attr(href), a.menu-item__link::attr(href)",
        "index_data_selectors": {},
        "page_url_selector": "a.post__permalink::attr(href), a.page-numbers::attr(href)",
        "page_data_selectors": {
            "date": ".post__date::text",
            "title": ".post__headline::text",
            "author": ".author-details a::text",
            "body": ".post__content--is-content p::text, .post__content--is-content span::text, .post__content--is-content li::text"
        }
    }
]
```
This example describes the configuration file which contains css selectors for scraping two websites: 
```https://scilogs.spektrum.de``` and ```https://www.20min.ch```.
```website_name``` field is required and it represents the name of the output file. ```website_url``` is required field 
and it represents the index page od the website that should be scraped. ```index_url_selector``` is required field and 
it represents css selectors for selecting urls from the index page and those urls are used as starting point for further
scraping of website. ```index_data_selectors``` is required field which represents selectors for the data that should be
 scraped from the index page (it can be empty if there is no data in index page that should be scraped). 
 ```page_url_selector``` is required field which represents selectors for selecting urls in web pages. 
 ```page_data_selectors``` is required field that represents object with optional fields. Every field in this object 
 represents css selectors for data that should be scraped and that is going to be found in output file. Those optional 
 fields in configuration file should be also defined in the items.py file like in example: ```author = scrapy.Field()```
 If rhe field is defined in configuration and not in the items.py file, it will create an error. On the other hand, it 
 is completely fine and allowed to have fields defined in items.py and not defined in the configuration file.
 Only data fields defined in configuration file are going to be visible in the output file.
 
The tool can be ran successfully if the following instructions are followed:

* Clone the repository:
```
git clone https://github.com/choco-brownies/websites_scraper.git
```
* In the websites_scraper directory create and activate virtual environment:
```
cd websites_scraper
virtualenv -p python3 venv
source venv/bin/activate
```
* Install all dependencies from the file requirements.txt:
```
pip install -r requirements.txt
```
* Define css selectors in the configuration file websites_scraper/websites_scraper/configuration_data.conf:

* Start Web Scraper tool:
```
python run_scraper.py
```