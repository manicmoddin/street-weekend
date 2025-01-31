from bs4 import BeautifulSoup
import yaml
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint

browser = webdriver.Firefox()


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

current_working_dir = get_script_path()
with open(current_working_dir + "/config.yaml", "r") as f:
    config = yaml.safe_load(f)

year = config['year']
base_url = config['base_url']

browser.get(base_url)
html = browser.page_source

soup = BeautifulSoup(html, "html.parser")

this_year_entries = soup.findAll('div', class_="AttractionWrapperEntrylistColums33")
print(len(this_year_entries))

racers = []

for entry in this_year_entries:
    racer_name = entry.find('div', class_="RacerName")
    race_number = entry.find('div', class_="RacerNumber")
    race_car_logos = entry.find('div', class_="RacerLogos")
    race_car_man = ''
    racer_nat = ''

    print(entry)
    logo_id = 0
    for race_logo in race_car_logos:
        if logo_id == 0:
            race_car_man = race_logo['title']
            logo_id = logo_id + 1
        else:
            racer_nat = race_logo['title']

    racer = {"name" : racer_name.text.strip(), "number":race_number.text.strip(), "car_man":race_car_man.strip(), "nationality":racer_nat.strip()}
    racers.append(racer)

    print(f"Name:         {racer_name.text.strip()}")
    print(f"Number:       {race_number.text.strip()}")
    print(f"Manufacturer: {race_car_man.strip()}")
    print(f"Natanality:   {racer_nat.strip()}")
    print()

browser.close()

pprint(racers)

# Now comes the fun bit - Looping though the list to pull out details.
# What is the most popular manufacturer taking part?
manufacturers = dict()
for racer in racers:
    manufact = racer['car_man']
    if manufact in manufacturers:
        manufacturers[manufact] =  manufacturers[manufact] +1
    else:
         manufacturers[manufact] = 1

sorted_manufacturers = sorted(manufacturers, key=manufacturers.get, reverse=True)
for m in sorted_manufacturers:
    print(m, manufacturers[m])
