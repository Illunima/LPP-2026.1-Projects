from enum import Enum
from Sigil import MightyLeap, Stinky, Fledgling, Leader, Airborne, Sprinter, Repulsive, WorthySacrifice, BoneKing

class CardPos(Enum):
    HAND = 0
    RIGHTMOST = 1
    RIGHTMID = 2
    LEFTMID = 3
    LEFTMOST = 4
    DISCARD = 5
    DECK = 6

class Card():
    def __init__(self, id):
        self.id = id
        self.pos = CardPos.DECK.value
        self.enhanced = False
        self.nature = self.get_card_nature()[id]
        self.data = BeastCard.gen_card()[id]
        self.name = self.data[0]
        self.tribe = self.data[1]
        self.cost = self.data[2]
        self.cost_type = self.data[3]
        self.base_atk = self.data[4]
        self.atk = self.base_atk
        self.base_hp = self.data[5]
        self.hp = self.base_hp
        self.sigils = set()
        for obj in self.data[6]:
            self.sigils.add(obj)

    def get_card_nature(self):
        nature_list = [ "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast" ]
        return nature_list
    
    def display_card(self):
        print(f"=")
        print(f"|{self.name}")
        print(f"| custo: {self.cost} {self.cost_type}")
        print(f"| ataque: {self.base_atk}")
        print(f"| saúde: {self.base_hp}")
        print(f"| selos: ")
        for sigil in self.sigils:
            print(f"| - {sigil.name}")
        print(f"=")

    def blood_sacrifice(self):
        value = 1
        for sigil in self.sigils:
            if sigil == WorthySacrifice():
                value = 3
        return value
    
    def sacrifice(self, own_side):
        self.hp = 0
        self.checkup(own_side)
    
    def strike(self, own_side, oposing_side, target):
        scale_tip = 0
        for card in target:
            if target == None:
                damage = self.atk
                for sigil in oposing_side[self.pos].sigils:
                    if sigil == Stinky():
                        damage -= 1
                if self.pos - 1 >= 0:
                    for sigil in own_side[self.pos - 1].sigils:
                        if sigil == Leader():
                            damage += 1
                if self.pos + 1 < 4:
                    for sigil in own_side[self.pos + 1].sigils:
                        if sigil == Leader():
                            damage += 1
                print(f"{self.name} ataca o oponente, adicionando {damage} à balança.")
            else:
                scale_tip += damage
                bypass = False
                damage = self.atk
                repulsive = False
                for sigil in self.sigils:
                    if sigil == Airborne():
                        bypass = True
                for sigil in target.sigils:
                    if sigil == Repulsive():
                        repulsive = True
                    if  sigil == MightyLeap():
                        bypass = False
                for sigil in oposing_side[self.pos].sigils:
                    if sigil == Stinky():
                        damage -= 1
                if self.pos - 1 >= 0:
                    for sigil in own_side[self.pos - 1].sigils:
                        if sigil == Leader():
                            damage += 1
                if self.pos + 1 < 4:
                    for sigil in own_side[self.pos + 1].sigils:
                        if sigil == Leader():
                            damage += 1
                if bypass:
                    if damage > 0:
                        print(f"{self.name} ataca por cima de {target.name}, adicionando {damage} à balança.")
                        scale_tip += damage
                elif repulsive:
                    print(f"{self.name} não consegue atacar {target.name}.")
                else:
                    if damage > 0:
                        print(f"{self.name} ataca {target.name}, causando {damage} de dano.")
        return scale_tip
    
    def checkup(self, own_side):
        bones = 1
        if self.hp <= 0:
            for sigil in self.sigils:
                if sigil == BoneKing():
                    bones = 4
            print(f"{self.name} pereceu. Você foi concedido {bones} Ossos.")
            own_side[self.pos] = None
            self.pos = CardPos.DISCARD.value
            return bones
        return 0
        
                    

class BeastCard(Card):
    squirrel = ( "Esquilo", "", 0, "Sangue", 0, 1, [] ) #id 0
    stoat = ( "Arminho", "", 1, "Sangue", 1, 3, [] ) #id 1
    bullfrog = ( "Rã-touro", "reptile", 1, "Sangue", 1, 2, [MightyLeap()] ) #id 2
    wolf = ( "Lobo", "canine", 2, "Sangue", 3, 2, [] ) #id 3
    stinkbug = ( "Percevejo", "insect", 2, "Ossos", 1, 2, [Stinky()])#id 4
    coyote = ( "Coiote", "canine", 4, "Ossos", 2, 1, [] )#id 5
    wolf_cub = ( "Filhote de lobo", "canine", 1, "Sangue", 1, 1, [Fledgling()] )#id 6
    alpha = ( "Alfa", "canine", 4, "Ossos", 1, 2, [Leader()] )#id 7
    sparrow = ( "Pardal", "Avian", 1, "Sangue", 1, 2, [Airborne()] )#id 8
    raven = ( "Corvo", "Avian", 2, "Sanue", 2, 3, [Airborne()] )#id 9
    raven_egg = ( "Ovo de corvo", "Avian", 1, "Sangue", 0, 2, [Fledgling()] )#id 10
    turkey_vulture = ( "Urubu", "Avian", 8, "Ossos", 3, 3, [Airborne()] )#id 11
    elk = ( "Cervo", "Hooved", 2, "Sangue", 2, 4, [Sprinter()] )#id 12
    elk_fawn = ( "Filhote de cervo", "Hooved", 1, "Sangue", 1, 1, [Sprinter(), Fledgling()] )#id 13
    river_snapper = ( "Tartaruga mordedora", "Reptile", 2, "Sangue", 1, 6, [] )#id 14
    rattler = ( "Cascavel", "Reptile", 6, "Ossos", 3, 1, [] )#id 15
    starvation = ( "Inanição", "", 0, "Sangue", 0, 0, [Repulsive()] )#id 16
    all_cards = [ squirrel, stoat, bullfrog, wolf, stinkbug, coyote, wolf_cub, alpha, sparrow, raven, raven_egg, 
        turkey_vulture, elk, elk_fawn, river_snapper, rattler ]

    @classmethod
    def gen_card(cls):
        return BeastCard.all_cards