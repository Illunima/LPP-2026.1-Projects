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

# A implementação atual de da classe Card só consegue acomodar cartas de bestas,
# visto que cartas de outras naturezas não são implementadas nessa versão.
# Conseidere o construtor dessa classe como o construtor de uma BeastCard.
# Mesmo assim os métodos permaneceriam bem parecidos.

class Card():
    def __init__(self, id):
        self.id = id
        # As cartas são geradas por id. neste caso, a carta gerada será
        # automaticamente desiganda a natureza de besta.

        self.pos = CardPos.DECK.value
        # Todas as cartas começam inicialmente no deck e serão
        # deslocadas atraves de eventos externos.

        self.enhanced = False
        # Um dos eventos não implementados envolve o aprimoramento de uma carta através do sacrifício de outra carta.
        # Esta carta então receberia a alma da carta sacrificada, junto a todos os selos que esta possuía.
        # Cada carta pode possuir apenas uma alma de outra carta, e não pode passar sua alma adiante.

        self.nature = self.get_card_nature()[id]
        self.data = BeastCard.gen_card()[id]
        # Todas as informações relativas a cada carta estão armazenadas em suas sobreclasses
        # e são recuperadas para gerar um novo objeto da carta.

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
        # As cartas podem possuir zero ou mais selos. Estes estão armazenados em um set visto que o mesmo selo
        # não surte efeito mais de uma vez em uma carta, e desta forma é mais conveniente verificar a presença de um selo específico.

        self.direction = "Right"
        # Guarda a direção do selo Sprinter, quando estiver presente.

        self.age = 0
        # Guarda a quantidade de turnos que esta carta permaneceu na mesa para ativar o efeito do selo Fledgling.

    # Sinceramente, esse método poderia simplismente retornar "Beast", mas ele seria útil com mais naturezas de carta.

    def get_card_nature(self):
        nature_list = [ "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast", "Beast" ]
        return nature_list
    
    # Serve para exibir uma carta no terminal. Outra alternativa mais interessante, porém mais extensa, seria passar
    # as informações de cada linha a ser exibida para que múltiplas cartas pudessem ser exibidas lado a lado,
    # tal qual em Inscryption, mas temos que nos virar com o terminal :\
    
    def display_card(self):
        print(f"=")
        print(f"|{self.name}")
        if self.cost == 0:
            print(f"| custo: 0")
        else:
            print(f"| custo: {self.cost} {self.cost_type}")
        print(f"| ataque: {self.atk}")
        print(f"| saúde: {self.hp}")
        print(f"| selos: ")
        for sigil in self.sigils:
            print(f"| - {sigil}")
        print(f"=")

    # Nem todas as cartas podem ser sacríficadas, outras tem um sacrifício mais valioso,
    # enquanto outras podem ser sacrificadas muitas vezes.
    # Na lista de cartas atual, todas as cartas são criaturas, e no geral toda criatura pode ser sacrificada.

    def blood_sacrifice(self):
        value = 1
        for sigil in self.sigils:
            if sigil == WorthySacrifice():
                value = 3
        return value
    
    # Executa devidamente o sacrifício de uma carta.
    
    def sacrifice(self, own_side):
        self.hp = 0
        return self.checkup(own_side)
    
    # A chave para o combate. Este método seria resonsável por executar o ataque de uma carta, mas acaba também
    # verificando todas as interações de selos possíveis. Essa foi a melhor forma que eu encontrei de exprexar as interações
    # dos selos, visto que os selos presentes na mesa estão sempre mudando e devem ser analisados a cada ataque feito.
    # Ataques diretos resultam em pesos adicionados à balança que são retornados para serem contabilizados.
    
    def strike(self, own_side, oposing_side, target):
        scale_tip = 0
        if target == None: # Ataque direto
            damage = self.atk
            if oposing_side[self.pos - 1] != None: # Verifica cartas à frente
                for sigil in oposing_side[self.pos - 1].sigils:
                    if sigil == Stinky.sigil_id():
                        damage -= 1
            if self.pos - 2 >= 0 and own_side[self.pos - 2] != None: # Verifica cartas à esquerda
                for sigil in own_side[self.pos - 2].sigils:
                    if sigil == Leader.sigil_id():
                        damage += 1
            if self.pos < 4 and own_side[self.pos] != None: # Verifica cartas à direita
                for sigil in own_side[self.pos].sigils:
                    if sigil == Leader.sigil_id():
                        damage += 1
            if damage > 0: # Se a carta não pode causar dano, o ataque não ocorre
                print(f"{self.name} ataca o oponente, adicionando {damage} à balança.")
                scale_tip += damage
        else: # Ataca o alvo
            damage = self.atk
            bypass = False
            repulsive = False
            sprint = False
            for sigil in self.sigils: #Verifica selos nesta carta
                if sigil == Airborne.sigil_id(): # Sobrevoa o alvo
                    bypass = True
                if sigil == Sprinter.sigil_id(): # Tenta se mover após atacar
                    sprint = True
            for sigil in target.sigils: # Verifica selos no alvo
                if sigil == Repulsive.sigil_id(): # Anula o dano
                    repulsive = True
                if  sigil == MightyLeap.sigil_id(): # Impede sobrevoo
                    bypass = False
            if oposing_side[self.pos - 1] != None:
                for sigil in oposing_side[self.pos - 1].sigils:
                    if sigil == Stinky.sigil_id():
                        damage -= 1
            if self.pos - 2 >= 0 and own_side[self.pos - 2] != None:
                for sigil in own_side[self.pos - 2].sigils:
                    if sigil == Leader.sigil_id():
                        damage += 1
            if self.pos < 4 and own_side[self.pos] != None:
                for sigil in own_side[self.pos].sigils:
                    if sigil == Leader.sigil_id():
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
                    target.hp -= damage
            if sprint:
                self.movement(own_side)
        return scale_tip
    
    # Verifica e trata a morte de uma carta. Quando uma carta morre, ela é descaratada
    # e se for uma criatura, o jogador ganhará ossos independente se ele possuia a carta ou como a carta foi morta.
    
    def checkup(self, own_side):
        bones = 1 # A maioria das cartas concede 1 osso ao morrrer
        if self.hp <= 0:
            for sigil in self.sigils: # Verifica selos nesta carta
                if sigil == BoneKing.sigil_id():
                    bones = 4
            if bones > 1:
                print(f"{self.name} pereceu. Você foi concedido {bones} Ossos.")
            else:
                print(f"{self.name} pereceu. Você foi concedido {bones} Osso.")
            own_side[self.pos-1] = None
            self.pos = CardPos.DISCARD.value
            return bones
        return 0
    
    # Realiza a movimentação de carta no próprio lado do tabuleiro, instigado pelo selo Sprinter.
    
    def movement(self, own_side):
        if self.pos == 1:
            self.direction = "Right"
        if self.pos == 4:
            self.direction = "Left"
        if self.direction == "Right":
            if own_side[self.pos] == None:
                own_side[self.pos] = self
                own_side[self.pos - 1] = None
                self.pos += 1
                print(f"{self.name} se move para a direita.")
            elif self.pos != 1:
                self.direction = "Left"
        elif self.direction == "Left":
            if own_side[self.pos - 2] == None:
                own_side[self.pos - 2] = self
                own_side[self.pos - 1] = None
                self.pos -= 1
                print(f"{self.name} se move para a esquerda.")
            elif self.pos != 4:
                self.direction = "Right"

    # Evolui cartas que possuem o selo Fledgling

    def evolve(self):
        if Fledgling.sigil_id() in self.sigils and self.age >= 1:
            match self.id:
                case 6: # Evolui Filhote de lobo para Lobo
                    print(f"A carta {self.name} evolui para Lobo")
                    self.sigils.remove(Fledgling.sigil_id())
                    card = Card(3)
                    card.hp -= self.base_hp - self.hp # Transfere o dano sofrido para a nova forma
                    for sigil in self.sigils:
                        card.sigils.add(sigil) # Transfere selos adicionais para a nova forma
                    self = card
                case 10: # Evolui Ovo de corvo para Corvo
                    print(f"A carta {self.name} evolui para Corvo")
                    self.sigils.remove(Fledgling.sigil_id())
                    card = Card(9)
                    card.hp -= self.base_hp - self.hp # Transfere o dano sofrido para a nova forma
                    for sigil in self.sigils:
                        card.sigils.add(sigil) # Transfere selos adicionais para a nova forma
                    self = card
                case 13: # Evolui Filhote de cervo para Cervo
                    print(f"A Carta {self.name} evolui para Cervo")
                    self.sigils.remove(Fledgling.sigil_id())
                    card = Card(12)
                    card.hp -= self.base_hp - self.hp # Transfere o dano sofrido para a nova forma
                    for sigil in self.sigils:
                        card.sigils.add(sigil) # Transfere selos adicionais para a nova forma
                    self = card
                case _: # Evolui outras cartas para sua forma adulta genérica
                    print(f"A carta {self.name} evolui para sua forma adulta.")
                    self.name += " Ancião"
                    self.atk += 1
                    self.hp += 2
                    self.sigils.remove(Fledgling.sigil_id())
        return self

# Atualmente guarda as informações de todas as cartas e pode gerar uma lista com todas as cartas por ordem de id.
# ( Nome, Tribo, Custo, Tipo de custo, Ataque, Saúde, [ Selos ] )

class BeastCard(Card):
    squirrel = ( "Esquilo", "", 0, "Sangue", 0, 1, [] ) #id 0
    stoat = ( "Arminho", "", 1, "Sangue", 1, 3, [] ) #id 1
    bullfrog = ( "Rã-touro", "Reptile", 1, "Sangue", 1, 2, [MightyLeap.sigil_id()] ) #id 2
    wolf = ( "Lobo", "Canine", 2, "Sangue", 3, 2, [] ) #id 3
    stinkbug = ( "Percevejo", "Insect", 2, "Ossos", 1, 2, [Stinky.sigil_id()] )#id 4
    coyote = ( "Coiote", "Canine", 4, "Ossos", 2, 1, [] )#id 5
    wolf_cub = ( "Filhote de lobo", "Canine", 1, "Sangue", 1, 1, [Fledgling.sigil_id()] )#id 6
    alpha = ( "Alfa", "Canine", 4, "Ossos", 1, 2, [Leader.sigil_id()] )#id 7
    sparrow = ( "Pardal", "Avian", 1, "Sangue", 1, 2, [Airborne.sigil_id()] )#id 8
    raven = ( "Corvo", "Avian", 2, "Sanue", 2, 3, [Airborne.sigil_id()] )#id 9
    raven_egg = ( "Ovo de corvo", "Avian", 1, "Sangue", 0, 2, [Fledgling.sigil_id()] )#id 10
    turkey_vulture = ( "Urubu", "Avian", 8, "Ossos", 3, 3, [Airborne.sigil_id()] )#id 11
    elk = ( "Cervo", "Hooved", 2, "Sangue", 2, 4, [Sprinter.sigil_id()] )#id 12
    elk_fawn = ( "Filhote de cervo", "Hooved", 1, "Sangue", 1, 1, [Sprinter.sigil_id(), Fledgling.sigil_id()] )#id 13
    river_snapper = ( "Tartaruga mordedora", "Reptile", 2, "Sangue", 1, 6, [] )#id 14
    rattler = ( "Cascavel", "Reptile", 6, "Ossos", 3, 1, [] )#id 15
    starvation = ( "Inanição", "", 0, "Sangue", 0, 0, [Repulsive()] )#id 16
    all_cards = [ squirrel, stoat, bullfrog, wolf, stinkbug, coyote, wolf_cub, alpha, sparrow, raven, raven_egg, 
        turkey_vulture, elk, elk_fawn, river_snapper, rattler ]

    @classmethod
    def gen_card(cls):
        return BeastCard.all_cards