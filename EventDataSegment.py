import dataclasses
from datetime import date

from shapely.geometry.base import BaseGeometry

from WegLocatieData import WegLocatieData


@dataclasses.dataclass
class EventDataSegment:
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
    shape: BaseGeometry = None
    override_geometry = False

    def __str__(self):
        return f"EventDataSegment(ident8='{self.begin.ident8}, begin=WegLocatieData(positie={self.begin.positie}), eind=WegLocatieData(positie={self.eind.positie}), gebied='{self.gebied}', id='{self.id}', lengte={self.lengte})"
