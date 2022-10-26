import platform
import time

import pandas
from termcolor import colored

from FSConnector import FSConnector
from JsonToReferentiepuntProcessor import JsonToReferentiepuntProcessor
from JsonToWegsegmentProcessor import JsonToWegsegmentProcessor
from PostGISConnector import PostGISConnector
from PostGISToWegsegmentProcessor import PostGISToWegsegmentProcessor
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager
from uitzonderingen import add_exceptions


def district_ref_to_name_mapping(ref):
    mapping = {
        '312A': '312 Autosnelwegen Zuid',
        '311A': '311 Autosnelwegen Noord',
        '719': 'Zuid-Limburg',
        '717': 'West-Limburg',
        '125': 'Vosselaar',
        '212': 'Vilvoorde',
        '414': 'Sint-Niklaas',
        '112': 'Puurs',
        '316': 'Pittem',
        '412': 'Oudenaarde',
        '315': 'Oostende',
        '718': 'Oost-Limburg',
        '312': 'Kortrijk',
        '313': 'Ieper',
        '411': 'Gent',
        '114': 'Geel',
        '413': 'Eeklo',
        '720': 'Centraal-Limburg',
        '311': 'Brugge',
        '123': 'Brecht',
        '121': 'Antwerpen',
        '415': 'Aalst',
        '213': 'Leuven',
        '211': 'Halle',
        '214': 'Aarschot'
    }
    return mapping[ref]


def map_toestand(toestand):
    return toestand.upper().replace('-', '_')


def map_schadebeheerder(omschrijving):
    return omschrijving.split(' - ')[1].replace('district ', '')[0:3]


def map_toezichtgroep(omschrijving):
    schadebeheerder = map_schadebeheerder(omschrijving)
    mapping = {
        '1': 'WA_DISTRICT',
        '2': 'WVB_DISTRICT',
        '3': 'WWV_DISTRICT',
        '4': 'WOV_DISTRICT',
        '7': 'WLB_DISTRICT'
    }
    try:
        return mapping[schadebeheerder[0:1]]
    except KeyError:
        schadebeheerder = omschrijving.split(' - ')[1].replace('district ', '')
        print(colored(f'no mapping for {omschrijving}', 'red'))
        return ''


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

    # # haal x aantal referentiepunten uit de feature server
    # fs_c = FSConnector(requester)
    # start = time.time()
    # print(colored(f'Connecting to Feature server...', 'green'))
    # raw_output = fs_c.get_raw_lines(layer="referentiepunten", lines=30000)  # beperkt tot X aantal lijnen
    # end = time.time()
    # print(colored(f'Number of lines from Feature server: {len(raw_output)}', 'green'))
    # print(colored(f'Time to get input from feature server: {round(end - start, 2)}', 'yellow'))
    #
    # # verwerk de input van de feature server tot een lijst van EventDataSegment objecten
    # start = time.time()
    # processor = JsonToReferentiepuntProcessor()
    # referentiepunten = processor.process_json(raw_output)
    # end = time.time()
    # print(
    #     colored(f'Time to process feature server lines to Python dataclass objects: {round(end - start, 2)}', 'yellow'))

    # haal x aantal afschermende constructies uit de feature server
    fs_c = FSConnector(requester)
    start = time.time()
    print(colored(f'Connecting to Feature server...', 'green'))
    raw_output = fs_c.get_raw_lines(layer="beheersegmenten", lines=300)  # beperkt tot X aantal lijnen
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

    for el in list(filter(lambda x: x.id in ['58745', '58771', '58639', '58681', '58646', '58675', '58833', '58765',
                                             '59593', '56392', '56682', '58721', '57436', '56693', '56608', '56501',
                                             '56674'] and x.lengte <= 5, list_segmenten)):
        list_segmenten.remove(el)
        # EventDataSegment(ident8='N0089072, begin=WegLocatieData(positie=1.846), eind=WegLocatieData(positie=1.847), gebied='Agentschap Wegen en Verkeer - AWV315', id='56674', lengte=1)
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
    print(f'number of segments: {len(list_segmenten)}')
    for i in range(5):
        iter_start = time.time()
        list_segmenten = processor.clean_list(list_segmenten)
        iter_end = time.time()
        print(colored(f'Time for iteration {i}: {round(iter_end - iter_start, 2)}', 'yellow'))
        print(f'number of segments: {len(list_segmenten)}')
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
    segmenten_WDB = list(
        filter(lambda x: x.gebied.startswith('Agentschap Wegen en Verkeer') or x.gebied in gebied_exceptions,
               list_segmenten))

    # get eminfra objects
    connector = PostGISConnector(host=db_settings['host'], port=db_settings['port'],
                                 user=db_settings['user'], password=db_settings['password'],
                                 database=db_settings['database'])
    cursor = connector.connection.cursor()
    eminfra_data = []

    query = """
    WITH koppelingen AS (
        SELECT * 
        FROM bestekkoppelingen 
            LEFT JOIN bestekken ON bestekken.uuid = bestekkoppelingen.bestekuuid 
        WHERE bestekkoppelingen.koppelingstatus = 'ACTIEF' AND bestekken.edeltabesteknummer LIKE '%MOW/AWV/2017/10%')
    SELECT assets.*, assettypes."label", beheerders.referentie, beheerders.naam, locatie.*, identiteiten.gebruikersnaam, koppelingen.aannemernaam, geometrie.wkt_string
        FROM assets 
            LEFT JOIN assettypes ON assets.assettype = assettypes.uuid
            LEFT JOIN locatie ON assets.uuid = locatie.assetuuid 
            LEFT JOIN geometrie ON assets.uuid = geometrie.assetuuid
            LEFT JOIN beheerders ON schadebeheerder = beheerders.uuid
            LEFT JOIN identiteiten on identiteiten.uuid = assets.toezichter
            LEFT JOIN koppelingen ON koppelingen.assetuuid = assets.uuid
    WHERE assets.actief = TRUE AND assettypes.uri IN ('https://lgc.data.wegenenverkeer.be/ns/installatie#TWeg','https://lgc.data.wegenenverkeer.be/ns/installatie#AWeg','https://lgc.data.wegenenverkeer.be/ns/installatie#NWeg','https://lgc.data.wegenenverkeer.be/ns/installatie#BWeg','https://lgc.data.wegenenverkeer.be/ns/installatie#RWeg')
    """
    cursor.execute(query)
    for record in cursor.fetchall():
        eminfra_data.append(PostGISToWegsegmentProcessor.process_json_object(record))
    cursor.close()

    print(colored(f'Number of data objects from EM-Infra: {len(eminfra_data)}', 'green'))

    matched_segments_WDB = []
    matched_eminfra_data = []

    df = pandas.DataFrame()

    lines_csv = []

    for segment_WDB in segmenten_WDB:
        if segment_WDB.id == '58655':
            continue  # verified exception

        sorted_candidates = []
        candidates = list(
            filter(lambda x: x.actief and x.ident8 is not None and x.ident8.startswith(segment_WDB.ident8[0:7]),
                   eminfra_data))
        if len(candidates) == 0:
            print(colored('no valid candidates found for: ', 'red'))
            print(segment_WDB)
            continue

        beheerder = segment_WDB.gebied.replace('Agentschap Wegen en Verkeer - AWV', '')
        for c in candidates:
            c.match_score = abs(c.begin.positie - segment_WDB.begin.positie) + abs(
                c.eind.positie - segment_WDB.eind.positie)

            if c.omschrijving is None or ' - ' not in c.omschrijving:
                c.match_score += 2.0
            else:
                district_in_omschrijving = c.omschrijving.split(' - ')[1][9:12]
                if beheerder != district_in_omschrijving:
                    c.match_score += 1.0

        sorted_candidates = list(sorted(candidates, key=lambda x: x.match_score))

        if sorted_candidates[0].match_score > 0.25:
            print(colored('no valid candidates found for: ', 'yellow'))
            print(segment_WDB)
            print('this is the best match:')
            print(sorted_candidates[0])
            continue
        else:
            print(colored(f'found reasonable match with a score of {sorted_candidates[0].match_score}', 'green'))
            # print(segment_WDB.wktLineStringZ)
            best_match = sorted_candidates[0]
            matched_eminfra_data.append(best_match)
            matched_segments_WDB.append(segment_WDB)

            if best_match.toestand != 'in-gebruik':
                print(colored(
                    f'bad toestand for: {best_match.naampad} link: https://apps.mow.vlaanderen.be/eminfra/installaties/{best_match.uuid}',
                    'red'))

            if segment_WDB.ident8[0:7] != best_match.ident8[0:7]:
                print(colored(f'{best_match.naampad}: ident8 not correct: {segment_WDB.ident8} vs {best_match.ident8}',
                              'red'))

            beheerder = segment_WDB.gebied.replace('Agentschap Wegen en Verkeer - AWV', '')
            district_in_omschrijving = best_match.omschrijving.split(' - ')[1][9:12]
            schadebeheerder = best_match.beheerder_referentie
            beheerobject = best_match.naampad.split('/')[0]
            naampad_beheerder = beheerobject.split('.')[1][0:3]

            if best_match.bestek is None:
                print(colored(f'{best_match.naampad}: bestek not found, should be {beheerder} '
                              f'link: https://apps.mow.vlaanderen.be/eminfra/installaties/{best_match.uuid}', 'red'))
            elif district_ref_to_name_mapping(beheerder) not in best_match.bestek:
                print(colored(f'{best_match.naampad}: bestek not correct: {beheerder} vs {best_match.bestek} '
                              f'link: https://apps.mow.vlaanderen.be/eminfra/installaties/{best_match.uuid}', 'red'))

            correction_needed = False

            if beheerder != district_in_omschrijving:
                print(colored(
                    f'{best_match.naampad}: beheerder != omschrijving: {beheerder} vs {best_match.omschrijving}',
                    'red'))
                correction_needed = True

            if beheerder != schadebeheerder:
                print(colored(f'{best_match.naampad}: beheerder != schadebeheerder: {beheerder} vs {schadebeheerder}',
                              'red'))
                correction_needed = True

            if beheerder != naampad_beheerder:
                print(colored(f'{best_match.naampad}: beheerder not in naampad: {beheerder} vs {naampad_beheerder}',
                              'red'))
                correction_needed = True

            if correction_needed:
                df1 = pandas.DataFrame({'id': [best_match.uuid], 'naampad': [best_match.naampad],
                                        'type': ['lgc:installatie#NWeg'], 'actief': [best_match.actief],
                                        'toestand': [map_toestand(best_match.toestand)],
                                        'schadebeheerder|referentie': [map_schadebeheerder(best_match.omschrijving)],
                                        'toezicht|toezichtgroep': [map_toezichtgroep(best_match.omschrijving)],
                                        'toezicht|toezichter': [best_match.toezichter]})

                df = pandas.concat([df, df1])

            simplified = segment_WDB.shape.simplify(1)
            lines_csv.append(f'{segment_WDB.id};{best_match.naampad};orig;{simplified}')
            lines_csv.append(f'{segment_WDB.id};{best_match.naampad};simplified;{simplified}')

            # if segment_WDB.wktLineStringZ != best_match.geometrie:
            #     response = requester.put(
            #         url=f'eminfra/core/api/installaties/{best_match.uuid}/installaties/ops/update-locatie-ident8',
            #         json={
            #             "uuids": [best_match.uuid],
            #             "async": False,
            #             "ident8": segment_WDB.ident8
            #         })
            #     print(response.status_code)
            #
            #     response = requester.put(url=f'eminfra/core/api/installaties/{best_match.uuid}'
            #                                  '/kenmerken/80052ed4-2f91-400c-8cba-57624653db11/geometrie',
            #                              json={"geometrie": str(simplified)})
            #     print(response.status_code)
            #
            #
            # pass

    for matched_segment in matched_segments_WDB:
        segmenten_WDB.remove(matched_segment)

    for matched_eminfra in matched_eminfra_data:
        if matched_eminfra not in eminfra_data:
            print(f'using segment twice: {matched_eminfra}')
        else:
            eminfra_data.remove(matched_eminfra)

    print(f'count remaining eminfra data: {len(eminfra_data)}')
    print(f'count remaining WDB data: {len(segmenten_WDB)}')

    if len(df) > 0:
        df.to_excel('beheersegmenten_correcties.xlsx')
    pass

    with open("wktstrings.csv", "w") as f:
        f.write('id;naampad;wkt\n')
        for line in lines_csv:
            f.write(line + '\n')
