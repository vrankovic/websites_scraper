import pathlib

"""
Path to the configuration file and to the directory with files which contains scraped data
"""
root_dir = pathlib.Path(__file__).parent.absolute()
path_conf_file = f"{root_dir}/websites_scraper/configuration_data.conf"
jsonl_file_directory = root_dir