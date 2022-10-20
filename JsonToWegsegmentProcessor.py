import json

import shapely
from shapely import wkt, ops
from EventDataSegment import EventDataSegment
from WegLocatieData import WegLocatieData


class JsonToWegsegmentProcessor:
    def process_json_object_or_list(self, dict_list, is_list=False):
        if not is_list:
            return self.process_json_object(dict_list)

        l = []
        for obj in dict_list:
            l.append(self.process_json_object(obj))
        return l

    def process_json_object(self, dict_list):
        event_data_segment = EventDataSegment()
        event_data_segment.ident8 = dict_list["properties"]["ident8"]
        event_data_segment.wktLineStringZM = self.fs_input_to_wkt_line_string_zm(dict_list["geometry"]["coordinates"])
        shape = shapely.wkt.loads(event_data_segment.wktLineStringZM)
        event_data_segment.wktLineStringZ = shape.wkt
        event_data_segment.begin = WegLocatieData()
        event_data_segment.begin.positie = dict_list["properties"]["locatie"]["begin"]["positie"]
        event_data_segment.begin.bron = dict_list["properties"]["locatie"]["begin"]["bron"]
        event_data_segment.begin.opschrift = dict_list["properties"]["locatie"]["begin"]["opschrift"]
        event_data_segment.begin.afstand = dict_list["properties"]["locatie"]["begin"]["afstand"]
        event_data_segment.begin.ident8 = dict_list["properties"]["locatie"]["begin"]["ident8"]
        event_data_segment.begin.wktPoint = self.fs_input_to_wkt_point(
            dict_list["properties"]["locatie"]["begin"]["geometry"]["coordinates"])
        event_data_segment.eind = WegLocatieData()
        event_data_segment.eind.positie = dict_list["properties"]["locatie"]["eind"]["positie"]
        event_data_segment.eind.bron = dict_list["properties"]["locatie"]["eind"]["bron"]
        event_data_segment.eind.opschrift = dict_list["properties"]["locatie"]["eind"]["opschrift"]
        event_data_segment.eind.afstand = dict_list["properties"]["locatie"]["eind"]["afstand"]
        event_data_segment.eind.ident8 = dict_list["properties"]["locatie"]["eind"]["ident8"]
        event_data_segment.eind.wktPoint = self.fs_input_to_wkt_point(
            dict_list["properties"]["locatie"]["eind"]["geometry"]["coordinates"])
        event_data_segment.id = dict_list["properties"]["id"]

        event_data_segment.eigenbeheer = dict_list["properties"]["eigenbeheer"]
        event_data_segment.gebied = dict_list["properties"]["gebied"]
        event_data_segment.lengte = dict_list["properties"]["lengte"]
        event_data_segment.creatiedatum = dict_list["properties"]["creatiedatum"]  # date
        event_data_segment.wijzigingsdatum = dict_list["properties"]["wijzigingsdatum"]  # date
        return event_data_segment

    def process_json(self, json_list) -> [EventDataSegment]:
        returnlist = []

        for el in json_list:
            dict_list = json.loads(el.replace('\n', ''))
            eventDataAC = self.process_json_object_or_list(dict_list)
            returnlist.append(eventDataAC)

        return returnlist

    @staticmethod
    def fs_input_to_wkt_line_string_zm(fs_input):
        s = 'LINESTRING ZM ('
        for punt in fs_input:
            for fl in punt:
                s += str(fl) + ' '
            s = s[:-1] + ', '
        s = s[:-2] + ')'
        return s

    @staticmethod
    def fs_input_to_wkt_point(FSInput):
        s = ' '.join(list(map(str, FSInput)))
        return f'POINT ({s})'

    @staticmethod
    def sort_list(list_segmenten):
        return list(sorted(list_segmenten, key=lambda x: (x.ident8, x.begin.positie)))

    @staticmethod
    def clean_list(list_segmenten):
        list_segmenten = JsonToWegsegmentProcessor.sort_list(list_segmenten)

        new_list = []
        for el in list_segmenten:
            new_list.append(el)

        skip_next = False
        for i in range(len(list_segmenten) - 1):
            if skip_next:
                skip_next = False
                continue
            if list_segmenten[i].ident8 != list_segmenten[i + 1].ident8:
                continue
            if list_segmenten[i].gebied != list_segmenten[i + 1].gebied:
                continue
            if list_segmenten[i].eind.positie != list_segmenten[i + 1].begin.positie:
                if abs(list_segmenten[i].eind.positie - list_segmenten[i + 1].begin.positie) > 0.050:
                    continue
            skip_next = True
            if list_segmenten[i] in new_list:
                new_list.remove(list_segmenten[i])
            if list_segmenten[i + 1] in new_list:
                new_list.remove(list_segmenten[i + 1])

            combined = list_segmenten[i]
            combined.eind = list_segmenten[i + 1].eind
            combined.lengte += list_segmenten[i + 1].lengte
            combined.creatiedatum = max(combined.creatiedatum, list_segmenten[i + 1].creatiedatum)
            combined.wijzigingsdatum = max(combined.wijzigingsdatum, list_segmenten[i + 1].wijzigingsdatum)
            new_list.append(combined)

        return new_list

    @staticmethod
    def keep_one_side(list_segmenten, margin=0.25):
        list_segmenten = JsonToWegsegmentProcessor.sort_list(list_segmenten)

        ups = list(filter(lambda s: s.ident8[-1] == '1', list_segmenten))
        for up_segment in ups:
            down_candidates = list(filter(lambda s: s.ident8 == (up_segment.ident8[:-1] + '2'), list_segmenten))
            for candidate in down_candidates:
                if candidate.gebied != up_segment.gebied:
                    continue
                up_from = up_segment.begin.opschrift + (up_segment.begin.afstand / 1000)
                up_to = up_segment.eind.opschrift + (up_segment.eind.afstand / 1000)
                down_from = candidate.begin.opschrift + (candidate.begin.afstand / 1000)
                down_to = candidate.eind.opschrift + (candidate.eind.afstand / 1000)
                if (abs(up_from - down_from) + abs(up_to - down_to)) < margin:
                    list_segmenten.remove(candidate)
                    continue

                if abs(up_from - down_from) < margin / 2 or abs(up_to - down_to) < margin / 2:
                    # move the segment a little to make comparison easier
                    if up_from > down_from:
                        up_to = up_to - up_from + down_from
                    elif down_from > up_from:
                        up_to = up_to - down_from + up_from

                    if down_to > up_to:
                        list_segmenten.remove(up_segment)
                    elif down_to < up_to:
                        list_segmenten.remove(candidate)

        return list_segmenten

    @staticmethod
    def remove_non_main_roads(list_segmenten):
        new_list = []
        for el in list_segmenten:
            try:
                if el.ident8[4:7] == '000':
                    new_list.append(el)
                elif el.ident8[4] == '9':
                    if el.ident8[5] in ['0', '1']:
                        new_list.append(el)
                    elif el.ident8[5] == '2':
                        if el.ident8[6] in ['0', '1', '2', '3', '4', '5', '6']:
                            new_list.append(el)
            except:
                print(f'problem with id: {el.id} and ident8: {el.ident8}')

        return new_list
