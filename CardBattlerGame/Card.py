from enum import Enum
from Sigil import MightyLeap, Stinky

class CardPos(Enum):
    HAND = 0
    RIGHTMOST = 1
    RIGHTMID = 2
    LEFTMID = 3
    LEFTMOST = 4
    DISCARD = 5
    DECK = 6

class Card:
    def __init__(self, id):
        self.id = id
        self.pos = CardPos.DECK.value
        self.enhanced = False
        self.nature = self.get_card_nature(id)
        self.data = BeastCard.gen_card()[id]
        self.name = self.data(0)
        self.tribe = self.data(1)
        self.cost = self.data(2)
        self.cost_type = self.data(3)
        self.base_atk = self.data(4)
        self.atk = self.base_atk
        self.base_hp = self.data(5)
        self.hp = self.base_hp
        self.sigils = set()
        for obj in self.data(6):
            self.sigils.add(obj)

    def get_card_nature(id):
        nature_list = [ "Beast", "Beast", "Beast", "Beast" ]
        return nature_list[id]
    
    def display_card(self):
        print(f"=")
        print(f"|{self.name}")
        print(f"| custo: {self.cost} {self.cost_type}")
        print(f"| ataque: {self.base_atk}")
        print(f"| saúde: {self.base_hp}")
        print(f"| selos: ")
        for sigil in self.sigils:
            print(f"- {sigil.name}")
        print(f"=")

class BeastCard(Card):
    squirrel = ( "Esquilo", "", 0, "Sangue", 0, 1, [] )
    stoat = ( "Arminho", "", 1, "Sangue", 1, 3, [] )
    bullfrog = ( "Rã-touro", "reptile", 1, "Sangue", 1, 2, [MightyLeap()] )
    wolf = ( "Lobo", "canine", 2, "Sangue", 3, 2, [] )
    stinkbug = ( "Percevejo", "insect", 2, "Ossos", 1, 2, [Stinky()])

    def gen_card(self):
        return [ self.squirrel, self.stoat, self.bullfrog, self.wolf, self.stinkbug ]