import dataclasses


@dataclasses.dataclass
class WegLocatieData:
    positie: float = 0
    bron: str = ''
    ident8: str = ''
    opschrift: float = 0
    afstand: float = 0
    wktPoint: str = ''