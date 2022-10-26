import json
import platform
import time

import pandas
from termcolor import colored

from FSConnector import FSConnector
from JsonToWegsegmentProcessor import JsonToWegsegmentProcessor
from PostGISConnector import PostGISConnector
from PostGISToWegsegmentProcessor import PostGISToWegsegmentProcessor
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager
from uitzonderingen import add_exceptions


def process_json_object_or_list(dict_list, is_list=False):
    if not is_list:
        return json.loads(dict_list.replace('\n', ''))

    l = []
    for el in dict_list:
        l.append(json.loads(el.replace('\n', '')))
    return l


if __name__ == '__main__':
    if platform.system() == 'Linux':
        OTLMOW_settings_path = '/home/davidlinux/Documents/AWV/resources/settings_OTLMOW.json'
        this_settings_path = '/home/davidlinux/Documents/AWV/resources/settings_AwvinfraPostGISSyncer.json'
    else:
        OTLMOW_settings_path = 'C:\\resources\\settings_OTLMOW.json'
        this_settings_path = 'C:\\resources\\settings_AWVGedeeldeFuncties.json'

    # een aantal classes uit OTLMOW library gebruiken
    settings_manager = SettingsManager(settings_path=this_settings_path)
    db_settings = settings_manager.settings['databases']['prd']

    requester = RequesterFactory.create_requester(settings=settings_manager.settings, auth_type='cert', env='prd')

    # haal x aantal afschermende constructies uit de feature server
    fs_c = FSConnector(requester)
    start = time.time()
    print(colored(f'Connecting to Feature server...', 'green'))
    raw_output = fs_c.get_raw_lines(layer="verkeersborden", lines=300)  # beperkt tot X aantal lijnen
    end = time.time()
    print(colored(f'Number of lines from Feature server: {len(raw_output)}', 'green'))
    print(colored(f'Time to get input from feature server: {round(end - start, 2)}', 'yellow'))

    # verwerk de input van de feature server tot een lijst van EventDataSegment objecten
    start = time.time()

    d = process_json_object_or_list(raw_output, is_list=True)
    df = pandas.DataFrame.from_dict(d, orient='columns')
    end = time.time()
    print(
        colored(f'Time to process feature server lines to Python dataclass objects: {round(end - start, 2)}', 'yellow'))

