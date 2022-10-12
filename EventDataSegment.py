import dataclasses
from datetime import date

from WegLocatieData import WegLocatieData


@dataclasses.dataclass
class EventDataSegment:
    ident8: str = ''
    wktLineStringZM: str = ''
    wktLineStringZ: str = ''
    begin: WegLocatieData = WegLocatieData()
    eind: WegLocatieData = WegLocatieData()
    gebied: str = ''
    id: str = ''
    lengte: float = -1
    eigenbeheer: bool = None
    creatiedatum: date = None
    wijzigingsdatum: date = None

    def __str__(self):
        return f"EventDataSegment(ident8='{self.ident8}, begin=WegLocatieData(positie={self.begin.positie}), eind=WegLocatieData(positie={self.eind.positie}), gebied='{self.gebied}', id='{self.id}', lengte={self.lengte})"
