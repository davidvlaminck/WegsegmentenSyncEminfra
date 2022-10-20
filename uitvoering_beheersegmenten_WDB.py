import platform
import time

from termcolor import colored

from FSConnector import FSConnector
from JsonToWegsegmentProcessor import JsonToWegsegmentProcessor
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager

if __name__ == '__main__':
    if platform.system() == 'Linux':
        OTLMOW_settings_path = '/home/davidlinux/Documents/AWV/resources/settings_OTLMOW.json'
        this_settings_path = 'settings_OTLMOW_linux.json'
    else:
        OTLMOW_settings_path = 'C:\\resources\\settings_OTLMOW.json'
        this_settings_path = 'C:\\resources\\settings_AWVGedeeldeFuncties.json'

    # een aantal classes uit OTLMOW library gebruiken
    settings_manager = SettingsManager(settings_path=this_settings_path)
    requester = RequesterFactory.create_requester(settings=settings_manager.settings, auth_type='cert', env='prd')

    # haal x aantal afschermende constructies uit de feature server
    fs_c = FSConnector(requester)
    start = time.time()
    print(colored(f'Connecting to Feature server...', 'green'))
    raw_output = fs_c.get_raw_lines(layer="beheersegmenten", lines=30000)  # beperkt tot X aantal lijnen
    end = time.time()
    print(colored(f'Number of lines from Feature server: {len(raw_output)}', 'green'))
    print(colored(f'Time to get input from feature server: {round(end - start, 2)}', 'yellow'))

    # verwerk de input van de feature server tot een lijst van EventDataSegment objecten
    start = time.time()
    processor = JsonToWegsegmentProcessor()
    list_segmenten = processor.process_json(raw_output)
    end = time.time()
    print(colored(f'Time to process feature server lines to Python dataclass objects: {round(end - start, 2)}', 'yellow'))

    #filter_ids = ['8797', '8796', '8798']
    #list_segmenten = list(filter(lambda x: x.id in filter_ids, list_segmenten))

    start = time.time()
    list_segmenten = processor.remove_non_main_roads(list_segmenten)
    print(f'number of segments: {len(list_segmenten)}')
    for i in range(4):
        iter_start = time.time()
        list_segmenten = processor.clean_list(list_segmenten)
        iter_end = time.time()
        print(colored(f'Time for iteration {i}: {round(end - start, 2)}', 'yellow'))
        print(f'number of segments: {len(list_segmenten)}')
    list_segmenten = processor.sort_list(list_segmenten)
    end = time.time()
    print(colored(f'Time to combine Python dataclass objects: {round(end - start, 2)}', 'yellow'))

    start = time.time()
    list_segmenten = processor.keep_one_side(list_segmenten)
    end = time.time()
    print(colored(f'Time to remove one side (double data): {round(end - start, 2)}', 'yellow'))

    with open("segmenten.csv", "w") as f:
        f.write('ident8;begin.opschrift;begin.afstand;eind.opschrift;eind.afstand;gebied\n')
        for segment in list_segmenten:
            f.write(f"{segment.ident8};{segment.begin.opschrift};{segment.begin.afstand};{segment.eind.opschrift};{segment.eind.afstand};{segment.gebied}\n")

    print(colored(f'Number of event data objects: {len(list_segmenten)}', 'green'))

