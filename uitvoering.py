import platform
import time

from termcolor import colored

from EventDataSegment import EventDataSegment
from FSConnector import FSConnector
from JsonToWegsegmentProcessor import JsonToWegsegmentProcessor
from PostGISConnector import PostGISConnector
from PostGISToWegsegmentProcessor import PostGISToWegsegmentProcessor
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager
from WegLocatieData import WegLocatieData


def add_exceptions(segmenten):
    instances_to_remove = []
    for instance in segmenten:
        if instance.ident8 == 'N0100001':
            if 'AWV121' in instance.gebied and instance.begin.opschrift == 0:
                instances_to_remove.append(instance)
            if 'AWV123' in instance.gebied and instance.begin.opschrift == 2.3:
                instance.begin.positie = 3.4
                instance.begin.opschrift = 3.4
                instance.begin.afstand = 0
                instance.lengte = instance.eind.positie - instance.begin.positie
        if instance.ident8 == 'N0120001':
            if 'AWV121' in instance.gebied and instance.begin.opschrift == 1:
                instance.eind.positie = 4.3
                instance.eind.opschrift = 4.3
                instance.eind.afstand = 0
                instance.lengte = instance.eind.positie - instance.begin.positie
        if instance.ident8 == 'N1120001':
            if 'AWV123' in instance.gebied and instance.begin.opschrift == 0:
                instance.begin.positie = 1.2
                instance.begin.opschrift = 1.2
                instance.begin.afstand = 0
                instance.lengte = instance.eind.positie - instance.begin.positie

# N1120001;0;-10;3.9;53;Agentschap Wegen en Verkeer - AWV123

    for instance_to_remove in instances_to_remove:
        segmenten.remove(instance_to_remove)

    n10_brabo = EventDataSegment()
    n10_brabo.begin = WegLocatieData()
    n10_brabo.eind = WegLocatieData()
    n10_brabo.ident8 = 'N0100001'
    n10_brabo.gebied = 'BRABO I'
    n10_brabo.eigenbeheer = False
    n10_brabo.begin.positie = 0
    n10_brabo.begin.opschrift = 0
    n10_brabo.begin.afstand = 0
    n10_brabo.eind.positie = 3.4
    n10_brabo.eind.opschrift = 3.4
    n10_brabo.eind.afstand = 0
    segmenten.append(n10_brabo)

    n12_brabo = EventDataSegment()
    n12_brabo.begin = WegLocatieData()
    n12_brabo.eind = WegLocatieData()
    n12_brabo.ident8 = 'N0120001'
    n12_brabo.gebied = 'BRABO I'
    n12_brabo.eigenbeheer = False
    n12_brabo.begin.positie = 4.3
    n12_brabo.begin.opschrift = 4.3
    n12_brabo.begin.afstand = 0
    n12_brabo.eind.positie = 6.1
    n12_brabo.eind.opschrift = 6.1
    n12_brabo.eind.afstand = 0
    segmenten.append(n12_brabo)

    n112_brabo = EventDataSegment()
    n112_brabo.begin = WegLocatieData()
    n112_brabo.eind = WegLocatieData()
    n112_brabo.ident8 = 'N1120001'
    n112_brabo.gebied = 'BRABO I'
    n112_brabo.eigenbeheer = False
    n112_brabo.begin.positie = 0
    n112_brabo.begin.opschrift = 0
    n112_brabo.begin.afstand = 0
    n112_brabo.eind.positie = 1.2
    n112_brabo.eind.opschrift = 1.2
    n112_brabo.eind.afstand = 0
    segmenten.append(n112_brabo)

    return segmenten

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
    raw_output = fs_c.get_raw_lines(layer="beheersegmenten", lines=30000)  # beperkt tot X aantal lijnen
    end = time.time()
    print(colored(f'Number of lines from Feature server: {len(raw_output)}', 'green'))
    print(colored(f'Time to get input from feature server: {round(end - start, 2)}', 'yellow'))

    # verwerk de input van de feature server tot een lijst van EventDataSegment objecten
    start = time.time()
    processor = JsonToWegsegmentProcessor()
    list_segmenten = processor.process_json(raw_output)
    end = time.time()
    print(
        colored(f'Time to process feature server lines to Python dataclass objects: {round(end - start, 2)}', 'yellow'))

    for el in list(filter(lambda x: x.id in ['58745', '58771', '58639', '58681', '58646', '58675', '58833', '58765', '59593', '56392', '56682', '58721', '57436', '56693', '56608', '56501'] and x.lengte <= 5, list_segmenten)):
        list_segmenten.remove(el)
        # EventDataSegment(ident8='N0580001, begin=WegLocatieData(positie=27.385), eind=WegLocatieData(positie=27.387), gebied='Agentschap Wegen en Verkeer - AWV313', id='56501', lengte=2)
        # EventDataSegment(ident8='N0390002, begin=WegLocatieData(positie=14.006), eind=WegLocatieData(positie=14.007), gebied='Agentschap Wegen en Verkeer - AWV315', id='56608', lengte=1)
        # EventDataSegment(ident8='N0390001, begin=WegLocatieData(positie=14.014), eind=WegLocatieData(positie=14.015), gebied='Agentschap Wegen en Verkeer - AWV315', id='56693', lengte=1)
        # EventDataSegment(ident8='N0360002, begin=WegLocatieData(positie=25.263), eind=WegLocatieData(positie=25.264), gebied='Agentschap Wegen en Verkeer - AWV316', id='57436', lengte=1)
        # EventDataSegment(ident8='N0080001, begin=WegLocatieData(positie=145.16), eind=WegLocatieData(positie=145.161), gebied='Agentschap Wegen en Verkeer - AWV315', id='58721', lengte=1)
        # EventDataSegment(ident8='N0089071, begin=WegLocatieData(positie=1.846), eind=WegLocatieData(positie=1.846), gebied='Agentschap Wegen en Verkeer - AWV315', id='56682', lengte=0)
        # EventDataSegment(ident8='N0360001, begin=WegLocatieData(positie=25.263), eind=WegLocatieData(positie=25.264), gebied='Agentschap Wegen en Verkeer - AWV316', id='56392', lengte=1)
        # EventDataSegment(ident8='N1200001, begin=WegLocatieData(positie=4.683), eind=WegLocatieData(positie=4.688), gebied='Agentschap Wegen en Verkeer - AWV121', id='59593', lengte=5)
        # EventDataSegment(ident8='N4000002, begin=WegLocatieData(positie=0), eind=WegLocatieData(positie=0.003), gebied='Agentschap Wegen en Verkeer - AWV415', id='58765', lengte=3)
        # EventDataSegment(ident8='N4590002, begin=WegLocatieData(positie=13.15), eind=WegLocatieData(positie=13.151), gebied='Agentschap Wegen en Verkeer - AWV412', id='58833', lengte=1)
        # EventDataSegment(ident8='N4620001, begin=WegLocatieData(positie=11.625), eind=WegLocatieData(positie=11.626), gebied='Agentschap Wegen en Verkeer - AWV415', id='58675', lengte=1)
        # EventDataSegment(ident8='N4000001, begin=WegLocatieData(positie=0), eind=WegLocatieData(positie=0.003), gebied='Agentschap Wegen en Verkeer - AWV415', id='58646', lengte=3)
        # EventDataSegment(ident8='N4590001, begin=WegLocatieData(positie=13.15), eind=WegLocatieData(positie=13.151), gebied='Agentschap Wegen en Verkeer - AWV412', id='58745', lengte=1)
        # EventDataSegment(ident8='N4620002, begin=WegLocatieData(positie=11.625), eind=WegLocatieData(positie=11.626), gebied='Agentschap Wegen en Verkeer - AWV415', id='58771', lengte=1)
        # EventDataSegment(ident8='N4170002, begin=WegLocatieData(positie=3.799), eind=WegLocatieData(positie=3.801), gebied='Agentschap Wegen en Verkeer - AWV415', id='58639', lengte=2)
        # EventDataSegment(ident8='N4170001, begin=WegLocatieData(positie=3.239), eind=WegLocatieData(positie=3.241), gebied='Agentschap Wegen en Verkeer - AWV415', id='58681', lengte=2)

    start = time.time()
    list_segmenten = processor.remove_non_main_roads(list_segmenten)
    for i in range(5):
        list_segmenten = processor.clean_list(list_segmenten)
    list_segmenten = processor.sort_list(list_segmenten)
    end = time.time()
    print(colored(f'Time to combine Python dataclass objects: {round(end - start, 2)}', 'yellow'))

    start = time.time()
    list_segmenten = processor.keep_one_side(list_segmenten)
    end = time.time()
    print(colored(f'Time to remove one side (double data): {round(end - start, 2)}', 'yellow'))

    list_segmenten = add_exceptions(list_segmenten)

    with open("segmenten.csv", "w") as f:
        f.write('ident8;begin.opschrift;begin.afstand;eind.opschrift;eind.afstand;gebied\n')
        for segment in list_segmenten:
            f.write(
                f"{segment.ident8};{segment.begin.opschrift};{segment.begin.afstand};{segment.eind.opschrift};{segment.eind.afstand};{segment.gebied}\n")

    print(colored(f'Number of event data objects: {len(list_segmenten)}', 'green'))

    gebied_exceptions = ['BRABO I']
    segmenten_WDB = list(filter(lambda x: x.gebied.startswith('Agentschap Wegen en Verkeer') or x.gebied in gebied_exceptions, list_segmenten))

    # get eminfra objects
    connector = PostGISConnector(host=db_settings['host'], port=db_settings['port'],
                                 user=db_settings['user'], password=db_settings['password'],
                                 database=db_settings['database'])
    cursor = connector.connection.cursor()
    eminfra_data = []

    query = """
    SELECT assets.*, assettypes."label", beheerders.referentie, beheerders.naam, locatie.* FROM assets 
    LEFT JOIN assettypes ON assets.assettype = assettypes.uuid
    LEFT JOIN locatie ON assets.uuid = locatie.assetuuid 
    LEFT JOIN beheerders ON schadebeheerder = beheerders.uuid
    WHERE assettypes.uri IN ('https://lgc.data.wegenenverkeer.be/ns/installatie#TWeg','https://lgc.data.wegenenverkeer.be/ns/installatie#AWeg','https://lgc.data.wegenenverkeer.be/ns/installatie#NWeg','https://lgc.data.wegenenverkeer.be/ns/installatie#BWeg','https://lgc.data.wegenenverkeer.be/ns/installatie#RWeg')
    """
    cursor.execute(query)
    for record in cursor.fetchall():
        eminfra_data.append(PostGISToWegsegmentProcessor.process_json_object(record))
    cursor.close()

    print(colored(f'Number of data objects from EM-Infra: {len(eminfra_data)}', 'green'))

    for segment_WDB in segmenten_WDB:
        if segment_WDB.id == '58655':
            continue # verified exception

        sorted_candidates = []
        candidates = list(filter(lambda x: x.actief and x.ident8 is not None and x.ident8.startswith(segment_WDB.ident8[0:7]), eminfra_data))
        if len(candidates) == 0:
            print(colored('no valid candidates found for: ', 'red'))
            print(segment_WDB)
            continue

        for c in candidates:
            c.match_score = abs(c.begin.positie - segment_WDB.begin.positie) + abs(c.eind.positie - segment_WDB.eind.positie)

        sorted_candidates = list(sorted(candidates, key=lambda x: x.match_score))

        if sorted_candidates[0].match_score > 0.25:
            print(colored('no valid candidates found for: ', 'yellow'))
            print(segment_WDB)
            print('this is the best match:')
            print(sorted_candidates[0])
            continue
        else:
            print(colored(f'found reasonable match with a score of {sorted_candidates[0].match_score}', 'green'))

        pass
