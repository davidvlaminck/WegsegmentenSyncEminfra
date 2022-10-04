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

