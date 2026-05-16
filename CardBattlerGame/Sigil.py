class Sigil():
    name = "Sigil"
    @classmethod
    def sigil_id(cls):
        return cls.name

class MightyLeap(Sigil):
    name = "Salto Pujante"
    desc = "Esta criatura bloqueia criaturas diante dela que tenham o selo aéreo."

class Stinky(Sigil):
    name = "Fedor"
    desc = "A criatura diante desta criatura perde 1 de poder."

class Fledgling(Sigil):
    name = "Fledgling"
    desc = "After surviving for 1 turn, this card grows into a stronger form."

class Leader(Sigil):
    name = "Leader"
    desc = "Creatures adjacent to this card gain 1 power"

class Airborne(Sigil):
    name = "Airborne"
    desc = "This card will ignore oposing cards and strike an opponent directly."

class Sprinter(Sigil):
    name = "Sprinter"
    desc = "At the end of the owner's turn, this card moves in the sigil's direction."

class Repulsive(Sigil):
    name = "Repulsive"
    desc = "If a creature would attack this card, it does not."

class WorthySacrifice(Sigil):
    name = "Worthy Sacrifice"
    desc = "This card counts as 3 Blood  rather than 1 Blood when sacrificed."

class BoneKing(Sigil):
    name = "Bone King"
    desc = "When this card dies, 4 Bones are awarded instead of 1."