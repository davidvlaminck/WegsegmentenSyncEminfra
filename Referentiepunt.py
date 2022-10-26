import dataclasses


@dataclasses.dataclass
class Referentiepunt:
    ident8: str = ''
    id: str = ''
    opschrift: float = -1
    afstand: float = -1
    positie: float = -1
    wkt_string: str = ''

    def __str__(self):
        return f"Referentiepunt(ident8='{self.ident8}, positie={self.positie}, id='{self.id}')"
