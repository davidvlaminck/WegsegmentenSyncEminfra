import json

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
        event_data_segment.eind.wktPoint = self.fs_input_to_wkt_point(dict_list["properties"]["locatie"]["eind"]["geometry"]["coordinates"])
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

    def clean_list(self, list_segmenten):
        list_segmenten = list(sorted(list_segmenten, key=lambda x: (x.ident8, x.begin.opschrift, x.begin.afstand)))

        new_list = []
        for el in list_segmenten:
            new_list.append(el)

        skip_next = False
        for i in range(len(list_segmenten)-1):
            if skip_next:
                skip_next = False
                continue
            if list_segmenten[i].ident8 != list_segmenten[i+1].ident8 or list_segmenten[i].gebied != list_segmenten[i+1].gebied:
                continue
            if list_segmenten[i].eind.opschrift != list_segmenten[i+1].begin.opschrift:
                continue
            if list_segmenten[i].eind.afstand != list_segmenten[i+1].begin.afstand:
                continue
            skip_next = True
            if list_segmenten[i] in new_list:
                new_list.remove(list_segmenten[i])
            if list_segmenten[i+1] in new_list:
                new_list.remove(list_segmenten[i+1])
            combined = list_segmenten[i]
            combined.eind = list_segmenten[i+1].eind
            combined.lengte += list_segmenten[i+1].lengte
            combined.creatiedatum = max(combined.creatiedatum, list_segmenten[i+1].creatiedatum)
            combined.wijzigingsdatum = max(combined.wijzigingsdatum, list_segmenten[i + 1].wijzigingsdatum)
            new_list.append(combined)

        return new_list




