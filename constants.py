import pathlib

root_dir = pathlib.Path(__file__).parent.absolute()
path_conf_file = f"{root_dir}/websites_scraper/configuration_data.conf"
path_jsonl_file = root_dir