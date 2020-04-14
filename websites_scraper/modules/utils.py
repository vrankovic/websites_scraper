from constants import path_conf_file
from ..modules.exceptions import NoConfFile
import json
from os import path


def get_data_from_conf_file(index, conf_path=path_conf_file):
    if not path.exists(conf_path):
        raise NoConfFile
    with open(conf_path) as f:
        data_str = f.read()
        data = json.loads(data_str)
        return data[int(index)]

