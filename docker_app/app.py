from bs4 import BeautifulSoup
import yaml
import os
import requests

import sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

current_working_dir = get_script_path()
with open(current_working_dir + "/config.yaml", "r") as f:
    config = yaml.safe_load(f)

year = config['year']
base_url = config['base_url']

page = requests.get(base_url)
soup = BeautifulSoup(page.content, "html.parser")

this_year_details = soup.find(year)