from termcolor import colored

from BeheerSegment import BeheerSegment
from WegLocatieData import WegLocatieData


class PostGISToWegsegmentProcessor:
    @staticmethod
    def process_json_object(tup):
        event_data_segment = BeheerSegment()
        event_data_segment.uuid = tup[0]
        event_data_segment.naampad = tup[4]
        event_data_segment.actief = tup[3]
        event_data_segment.toestand = tup[2]
        event_data_segment.wegtype = tup[11]
        event_data_segment.beheerder_referentie = tup[12]
        event_data_segment.beheerder_voluit = tup[13]
        event_data_segment.omschrijving = tup[16]
        event_data_segment.ident8 = tup[22]
        event_data_segment.toezichter = tup[34]
        event_data_segment.bestek = tup[35]
        event_data_segment.geometrie = tup[36]

        event_data_segment.begin = WegLocatieData()
        event_data_segment.eind = WegLocatieData()

        PostGISToWegsegmentProcessor.parse_omschrijving(event_data_segment)

        return event_data_segment

    @classmethod
    def parse_omschrijving(cls, data_segment):
        if data_segment.omschrijving is None:
            return
        if 'TUNNEL/' in data_segment.naampad.upper() or 'A11.PPS/' in data_segment.naampad.upper():
            return

        parts = data_segment.omschrijving.split(' - ')
        try:
            if data_segment.actief and len(parts) < 4:
                print(colored('Not a valid omschrijving: ' + data_segment.omschrijving, 'red'))
            else:
                van_tot = parts[2].split(' tot ')
                van_str = van_tot[0].replace('kmpt ', '')
                data_segment.begin.positie = float(van_str)
                tot_str = van_tot[1].replace('kmpt ', '')
                data_segment.eind.positie = float(tot_str)
                data_segment.ident8 = parts[3]
        except:
            print(colored('Not a valid omschrijving: ' + data_segment.omschrijving, 'red'))
