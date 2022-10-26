import json

import shapely
from shapely import wkt, ops, geometry
from shapely.geometry import MultiLineString, LineString
from termcolor import colored

from EventDataSegment import EventDataSegment
from Referentiepunt import Referentiepunt
from WegLocatieData import WegLocatieData


class JsonToReferentiepuntProcessor:
    def process_json_object_or_list(self, dict_list, is_list=False):
        if not is_list:
            return self.process_json_object(dict_list)

        l = []
        for obj in dict_list:
            l.append(self.process_json_object(obj))
        return l

    def process_json_object(self, dict_list):
        event_data_segment = Referentiepunt()
        event_data_segment.ident8 = dict_list["properties"]["locatie"]["ident8"]
        event_data_segment.opschrift = dict_list["properties"]["opschrift"]
        event_data_segment.afstand = dict_list["properties"]["locatie"]["afstand"]
        event_data_segment.positie = dict_list["properties"]["locatie"]["positie"]
        event_data_segment.id = dict_list["properties"]["id"]
        event_data_segment.wkt_string = dict_list["properties"]["geometry"]

        return event_data_segment

    def process_json(self, json_list) -> [EventDataSegment]:
        returnlist = []

        for el in json_list:
            dict_list = json.loads(el.replace('\n', ''))
            eventDataAC = self.process_json_object_or_list(dict_list)
            returnlist.append(eventDataAC)

        return returnlist
