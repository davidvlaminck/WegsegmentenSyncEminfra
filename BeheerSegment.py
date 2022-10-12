import dataclasses
from datetime import date

from WegLocatieData import WegLocatieData


@dataclasses.dataclass
class BeheerSegment:
    uuid: str = ''
    ident8: str = ''
    wktLineStringZM: str = ''
    wktLineStringZ: str = ''
    begin: WegLocatieData = WegLocatieData()
    eind: WegLocatieData = WegLocatieData()
    wegtype: str = ''
    naampad: str = ''
    actief: bool = None
    beheerder_referentie: str = ''
    beheerder_voluit: str = ''
    omschrijving: str = ''
    actie: str = ''
    match_score: float = -1

    def __str__(self):
        return f"BeheerSegment(ident8='{self.ident8}, begin=WegLocatieData(positie={self.begin.positie}), eind=WegLocatieData(positie={self.eind.positie}), beheerder='{self.beheerder_referentie}', uuid='{self.uuid}')"

