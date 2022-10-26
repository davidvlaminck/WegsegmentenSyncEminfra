from EventDataSegment import EventDataSegment
from WegLocatieData import WegLocatieData


def add_exceptions(segmenten):
    instances_to_remove = []
    for instance in segmenten:
        # brabo 1
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
        # LANTIS
        if instance.ident8 == 'A0140001' and 'AWV121' in instance.gebied:
            instance.gebied = 'LANTIS'
        if instance.ident8 == 'R0010001' and 'AWV121' in instance.gebied:
            instance.eind.positie = 14.350
            instance.eind.opschrift = 14.350
            instance.eind.afstand = 0
            instance.lengte = instance.eind.positie - instance.begin.positie
        if instance.ident8 == 'A0110002' and 'AWV121' in instance.gebied:
            instance.begin.positie = 68.0
            instance.begin.opschrift = 68.0
            instance.begin.afstand = 0
            instance.lengte = instance.eind.positie - instance.begin.positie
        # N0700001;37.9;-21;49.8;1;Agentschap Wegen en Verkeer - AWV121
        if instance.ident8 == 'N0700001' and 'AWV121' in instance.gebied:
            instance.eind.positie = 48.5
            instance.eind.opschrift = 48.5
            instance.eind.afstand = 0
            instance.lengte = instance.eind.positie - instance.begin.positie

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

    r1_lantis = EventDataSegment()
    r1_lantis.begin = WegLocatieData()
    r1_lantis.eind = WegLocatieData()
    r1_lantis.ident8 = 'R0010001'
    r1_lantis.gebied = 'LANTIS'
    r1_lantis.eigenbeheer = False
    r1_lantis.begin.positie = 14.350
    r1_lantis.begin.opschrift = 14.350
    r1_lantis.begin.afstand = 0
    r1_lantis.eind.positie = 16.706
    r1_lantis.eind.opschrift = 16.706
    r1_lantis.eind.afstand = 0
    segmenten.append(r1_lantis)

    a11_lantis = EventDataSegment()
    a11_lantis.begin = WegLocatieData()
    a11_lantis.eind = WegLocatieData()
    a11_lantis.ident8 = 'A0110002'
    a11_lantis.gebied = 'LANTIS'
    a11_lantis.eigenbeheer = False
    a11_lantis.begin.positie = 63.768
    a11_lantis.begin.opschrift = 64.1
    a11_lantis.begin.afstand = -332
    a11_lantis.eind.positie = 68.0
    a11_lantis.eind.opschrift = 68.0
    a11_lantis.eind.afstand = 0
    segmenten.append(a11_lantis)

    n70_lantis = EventDataSegment()
    n70_lantis.begin = WegLocatieData()
    n70_lantis.eind = WegLocatieData()
    n70_lantis.ident8 = 'N0700001'
    n70_lantis.gebied = 'LANTIS'
    n70_lantis.eigenbeheer = False
    n70_lantis.begin.positie = 48.5
    n70_lantis.begin.opschrift = 48.5
    n70_lantis.begin.afstand = 0
    n70_lantis.eind.positie = 49.12
    n70_lantis.eind.opschrift = 49.1
    n70_lantis.eind.afstand = 20
    segmenten.append(n70_lantis)

    n70_awv = EventDataSegment()
    n70_awv.begin = WegLocatieData()
    n70_awv.eind = WegLocatieData()
    n70_awv.ident8 = 'A0110002'
    n70_awv.gebied = 'Agentschap Wegen en Verkeer - AWV121'
    n70_awv.eigenbeheer = False
    n70_awv.begin.positie = 49.12
    n70_awv.begin.opschrift = 49.1
    n70_awv.begin.afstand = 20
    n70_awv.eind.positie = 49.801
    n70_awv.eind.opschrift = 49.8
    n70_awv.eind.afstand = 1
    segmenten.append(n70_awv)

    return segmenten
