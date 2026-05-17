from Card import Card
from Deck import Deck, SideDeck
from Sigil import Airborne, Fledgling
import random

class BattleTable():
    def __init__(self, player, scribe):
        self.scale = 0
        self.player_side = [ None, None, None, None ]
        self.scribe_side = [ None, None, None, None ]
        self.scribe_queue = [ None, None, None, None ]
        self.player = player
        self.player_bones = 0
        self.scribe = scribe
        self.ongoing = True
        self.player_turn = True
        self.starvation = 0
        self.queue_script = BatlleScript.random_script().copy()

    def scribe_advance(self):
        for i in range(4):
            if self.scribe_queue[i] != None:
                if self.scribe_side[i] == None:
                    self.scribe_side.pop(i)
                    self.scribe_side.insert(i, self.scribe_queue[i])
                    self.scribe_side[i].pos = i + 1
                    self.scribe_queue.pop(i)
                    self.scribe_queue.insert(i, None)
                    print(f"A carta {self.scribe_side[i].name} avança para a posição {i+1} do campo do oponente.")           

    def scribe_to_play(self):
        if len(self.queue_script) > 0:
            upnext = self.queue_script.pop(0)
            for pos in range(4):
                if upnext[pos] != None:
                    if self.scribe_queue[pos] == None:
                        self.scribe_queue[pos] = upnext[pos]
                        print(f"O patrono se prepara para avançar a carta {self.scribe_queue[pos].name} na posição {pos+1}")
                    else:
                        aux = ( None, None, None, None)
                        aux[pos] = upnext[pos]
                        self.queue_script.append(aux)
            del upnext

    def player_to_play(self):
        while self.player_turn == True:
            print("Digite 'hand' para exibir todas as cartas na sua mão junto a sua quantidade de Ossos.\n" \
            "Digite 'view' para exibir todas as cartas na mesa.\n" \
            "Digite 'play' para invocar uma carta de sua mão.\n" \
            "Digite 'bell' para encerrar seu turno.\n" \
            f"Estado atual da balança = {self.scale}")
            action = input()
            if action == 'play':
                print(f"Digite o número da carta na sua mão que deseja jogar (1-{len(self.player.hand)}):")
                card_index = int(input()) - 1
                if 0 <= card_index < len(self.player.hand):
                    card_to_play = self.player.hand[card_index]
                    ready = False
                    needed_cost_type = card_to_play.cost_type
                    needed_cost_amount = card_to_play.cost
                    if needed_cost_type == "Sangue":
                        blood_value = 0
                        marked_index = []
                        if needed_cost_amount == 0:
                            free_position = False
                            for pos in range(4):
                                if self.player_side[pos] == None:
                                    free_position = True
                                    break
                            if free_position == False:
                                print("Não há espaço suficiente para invocar esta carta.")
                                continue
                        while blood_value < needed_cost_amount:
                            print(f"É preciso sacrificar {needed_cost_amount-blood_value} de Sangue para invocar esta carta." \
                            f" Selecione uma carta do seu lado da mesa para sacrificar (1-4) ou '0' para cancelar:")
                            sacrifice_index = int(input()) - 1
                            if sacrifice_index == -1:
                                print("Invocação cancelada.")
                                marked_index.clear()
                                blood_value = 0
                                break
                            if 0 <= sacrifice_index < 4 and self.player_side[sacrifice_index] != None:
                                sacrifice_worth = self.player_side[sacrifice_index].blood_sacrifice()
                                if sacrifice_worth == 0:
                                    print("Esta carta não pode ser sacrificada. Escolha outra ou digite '0' para cancelar.")
                                    continue
                                blood_value += sacrifice_worth
                                marked_index.append(sacrifice_index)
                                print(f"A carta {self.player_side[sacrifice_index].name} será sacrificada por {sacrifice_worth} de Sangue.")
                            else:
                                print("Índice de carta inválido. Tente novamente.")
                        for index in marked_index:
                            self.player_bones += self.player_side[index].sacrifice(self.player_side)
                        if needed_cost_amount == 0:
                            print(f"Digite uma posição livre para invocar a carta {card_to_play.name} (1-4:)")
                            ready = True
                        elif blood_value == needed_cost_amount:
                            print(f"Sacrificio completo. Digite uma posição livre para invocar a carta {card_to_play.name} (1-4):")
                            ready = True
                        elif blood_value > needed_cost_amount:
                            print(f"Sacrificio excedente. Digite uma posição livre para invocar a carta {card_to_play.name} (1-4):")
                            ready = True
                    elif needed_cost_type == "Ossos":
                        free_position = False
                        for pos in range(4):
                            if self.player_side[pos] == None:
                                free_position = True
                                break
                        if free_position == False:
                            print("Não há espaço suficiente para invocar esta carta.")
                            continue
                        if self.player_bones >= needed_cost_amount:
                            self.player_bones -= needed_cost_amount
                            print(f"Digite uma posição livre para gastar {needed_cost_amount} Ossos e invocar a carta {card_to_play.name} (1-4):")
                            ready = True
                        else:
                            print("Ossos insuficientes para invocar esta carta.")
                    while ready == True:
                            placement_index = int(input()) - 1
                            if 0 <= placement_index < 4:
                                if self.player_side[placement_index] == None:
                                    card_to_play.pos = placement_index + 1
                                    self.player_side[placement_index] = card_to_play
                                    self.player.hand.pop(card_index)
                                    ready = False
                                else:
                                    print(f"Esta posição já está ocupada. Escolha outra posição para invocar a carta {card_to_play.name}:")
                            else:
                                print("Posição inválida. Tente novamente (1-4).")
                else:
                    if len(self.player.hand) == 0:
                        print("Não há cartas em sua mão para jogar.")
                    else:
                        print("Índice de carta inválido. Tente novamente.")
            elif action == 'bell':
                return
            elif action == 'hand':
                print(f"Ossos: {self.player_bones}")
                if len(self.player.hand) == 0:
                    print("Não há cartas em sua mão.")
                else:
                    print("Cartas na sua mão:")
                    self.player.view_hand()
            elif action == 'view':
                print("Cartas no seu lado da mesa:")
                for pos in range(4):
                    card = self.player_side[pos]
                    if card != None:
                        print(f"Posição {pos+1}:")
                        card.display_card()
                    else:
                        print(f"Posição {pos+1}: Vazia")
                print("Cartas no lado da mesa do patrono:")
                for pos in range(4):
                    card = self.scribe_side[pos]
                    if card != None:
                        print(f"Posição {pos+1}:")
                        card.display_card()
                    else:
                        print(f"Posição {pos+1}: Vazia")
                print("Cartas nas posições de espera do patrono:")
                for pos in range(4):
                    card = self.scribe_queue[pos]
                    if card != None:
                        print(f"Posição {pos+1}:")
                        card.display_card()
                    else:
                        print(f"Posição {pos+1}: Vazia")
            else:
                print("Entrada inválida.")

    def player_draw(self):
        card_drawn = False
        while card_drawn == False:
            if len( self.player.sidedeck.stack ) <= 0 and len( self.player.deck.stack ) <= 0:
                if self.starvation < 1:
                    print("Sem cartas para comprar. A fome aparece.")
                    self.starvation += 1
                    return self.starvation
                else:
                    print("Sem cartas para comprar. A fome se intensifica.")
                    self.starvation += 1
                    return self.starvation
            print("Digite 'deck' para comprar do deck principal ou 'side' para comprar do sidedeck:")
            chosen_deck = input()
            if chosen_deck == 'deck':
                if len( self.player.deck.stack ) > 0:
                    draw = self.player.deck.draw()
                    self.player.hand.append( draw )
                    card_drawn = True
                    print(f"A carta {draw.name} foi adicionada à sua mão.")
                else:
                    print("Não há cartas restantes no deck principal.")
            elif chosen_deck == 'side':
                if len( self.player.sidedeck.stack ) > 0:
                    draw = self.player.sidedeck.draw()
                    self.player.hand.append( draw )
                    card_drawn = True
                    print(f"A carta {draw.name} foi adicionada à sua mão.")
                else:
                    print("Não há cartas restantes no sidedeck.")
            else:
                print("Entrada inválida. Tente 'deck' ou 'side':")
        return self.starvation
    
    def starve(self, intensity):
        check = random.choices( [ 0, 1, 2, 3 ] )
        for pos in check:
            if self.player_side[pos] == None:
                self.player_side[pos] = Card(16)
                self.player_side[pos].atk = intensity
                self.player_side[pos].hp = intensity
                if intensity > 4:
                    self.player_side[pos].sigils.add(Airborne.sigil_id())
                print("A Inanição surge diante de você.")
                return
        for pos in check:
            if self.player_side[pos].name != "Inanição":
                self.player_side[pos] = Card(16)
                self.player_side[pos].atk = intensity
                self.player_side[pos].hp = intensity
                if intensity > 4:
                    self.player_side[pos].sigils.add(Airborne.sigil_id())
                print("A Inanição consome a criatura diante de você.")
                return
        for pos in check:
            self.player_side[pos].atk = intensity
            self.player_side[pos].hp = intensity
            if intensity > 4:
                self.player_side[pos].sigils.add(Airborne.sigil_id())
            print("A Inanição cresce ainda mais forte.")
            return
        
    def call_combat_player(self):
        turn_damage = 0
        turn_bones = 0
        for pos in range(4):
            attacker = self.player_side[pos]
            defender = self.scribe_side[pos]
            if attacker != None:
                turn_damage += attacker.strike(self.player_side, self.scribe_side, defender)
                turn_bones += attacker.checkup(self.player_side)
            if defender != None:
                turn_bones += defender.checkup(self.scribe_side)
        self.scale += turn_damage
        return turn_bones

    def call_combat_scribe(self):
        turn_damage = 0
        turn_bones = 0
        for pos in range(4):
            attacker = self.scribe_side[pos]
            defender = self.player_side[pos]
            if attacker != None:
                turn_damage += attacker.strike(self.scribe_side, self.player_side, defender)
                turn_bones += attacker.checkup(self.scribe_side)
            if defender != None:
                turn_bones += defender.checkup(self.player_side)
        self.scale -= turn_damage
        return turn_bones
    
    def age_cards(self, side):
        for card in side:
            if card != None:
                card.age += 1

    def evolve_cards(self, side):
        for card in side:
            if card != None:
                side[card.pos - 1] = card.evolve()
    
    def host_table(self):
        self.player.deck.deck_shuffle()
        for i in range (3):
            self.player.hand.append( self.player.deck.draw() )
        self.player.hand.append( self.player.sidedeck.draw() )
        self.scribe_to_play()
        print("Cartas no seu lado da mesa:")
        for pos in range(4):
            card = self.player_side[pos]
            if card != None:
                print(f"Posição {pos+1}:")
                card.display_card()
            else:
                print(f"Posição {pos+1}: Vazia")
        print("Cartas no lado da mesa do patrono:")
        for pos in range(4):
            card = self.scribe_side[pos]
            if card != None:
                print(f"Posição {pos+1}:")
                card.display_card()
            else:
                print(f"Posição {pos+1}: Vazia")
        print("Cartas nas posições de espera do patrono:")
        for pos in range(4):
            card = self.scribe_queue[pos]
            if card != None:
                print(f"Posição {pos+1}:")
                card.display_card()
            else:
                print(f"Posição {pos+1}: Vazia")
        print("Cartas na sua mão:")
        self.player.view_hand()
        while self.ongoing == True:
            if self.player_turn == True:
                self.player_to_play()
                self.player_bones += self.call_combat_player()
                self.age_cards(self.player_side)
                self.player_turn = False
                self.evolve_cards(self.scribe_side)
                print(f"Estado atual da balança: {self.scale}")
                if self.scale >= 5:
                    self.ongoing = False
                    print("Você venceu a batalha.")
                    return ( "win", self.scale - 5 )
            else:
                print("Vez do patrono")
                self.scribe_advance()
                self.player_bones += self.call_combat_scribe()
                self.scribe_to_play()
                self.age_cards(self.scribe_side)
                self.player_turn = True
                self.evolve_cards(self.player_side)
                print(f"Estado atual da balança: {self.scale}")
                if self.scale <= -5:
                    self.ongoing = False
                    print("Você perdeu a batalha.")
                    return ( "loss", 0 )
                hunger = self.player_draw()
                if hunger > 0:
                    self.starve(hunger)

class BatlleScript():
    script_1 = [ ( None, Card(2), None, None ), ( None, None, None, Card(5) ), ( None, None, None, None ), ( None, Card(8), None, None) ]

    all_scripts = [ script_1 ]

    @classmethod
    def random_script(cls):
        return random.choice( BatlleScript.all_scripts )

class MapEvent():
    def __init__(self, name):
        self.name = name

    @classmethod
    def add_card(cls, player):
        print("Você se depara com 3 criaturas. Você deve escolher uma delas para adicionar ao seu baralho:")
        card_options = Deck.pick_cards(3)
        for i in range (3):
            print(f"Carta {i+1}")
            card_options[i].display_card()
            print("")
        card_picked = False
        while card_picked == False:
            action = input("Escolha uma carta (1-3): ")
            try:
                card_index = int(action) - 1
            except:
                ("Entrada inválida.")
                continue
            if card_index < 3 and card_index >= 0:
                player.deck.add(card_options[card_index])
                print(f"A carta {card_options[card_index].name} foi adicionada ao seu baralho.")
                card_picked = True
            else:
                print("Indice invállido.")
        return


    

class MapTable():
    def __init__(self, player, scribe):
        self.player = player
        self.scribe = scribe
        self.road = []

    def add_event_node(self, event_id):
        match event_id:
            case 0:
                self.road.append(MapEvent("battle"))
            case 1:
                self.road.append(MapEvent("add_card"))
        return
