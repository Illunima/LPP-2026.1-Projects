from Card import Card
from Deck import Deck, SideDeck
from Sigil import Airborne, Sprinter
import random

# Hospeda as batalhas entre o jogador e o patrono.

class BattleTable():
    def __init__(self, player, scribe):
        self.scale = 0
        # A balança mede a quantidade de dano causado diretamente entre os jogadores.
        # Ataques diretos ao oponente adicionam pesos proporcionais ao dano causado.

        self.player_side = [ None, None, None, None ]
        # Cartas do jogador na mesa

        self.scribe_side = [ None, None, None, None ]
        # Cartas do patrono na mesa

        self.scribe_queue = [ None, None, None, None ]
        # O patrono não joga cartas diretamente no campo de batalha.
        # Ele joga cartas em posição de espera que depois avançam para o combate.
        # O patrono não deve obedecer o custo das cartas.
        # Dessa forma o jogador pode antecipar as jogadas do patrono.

        self.player = player
        self.player_bones = 0
        # A quantidade de Ossos do jogador.

        self.scribe = scribe
        self.ongoing = True
        self.player_turn = True
        self.starvation = 0
        # A fome serve para prevenir que uma batalha dure para sempre

        self.queue_script = BatlleScript.random_script().copy()
        # Lista com todas as próximas jogadas do patrono

    # Avança as cartas em espera do patrono para o campo de batalha.

    def scribe_advance(self):
        for i in range(4):
            if self.scribe_queue[i] != None:    # Para cada carta na fila,
                if self.scribe_side[i] == None: # se não houver nenhuma carta à frente
                    self.scribe_side[i] = self.scribe_queue[i] # Insere a carta naquela posição
                    self.scribe_side[i].pos = i + 1            # Atualiza a posição da carta
                    self.scribe_queue[i] = None                # Remove a carta da fila
                    print(f"A carta {self.scribe_side[i].name} avança para a posição {i+1} do campo do oponente.")           

    # Prepara as próximas cartas que o patrono vai colocar em espera.

    def scribe_to_play(self):
        if len(self.queue_script) > 0:        # Se houverem próximas jogadas programadas,
            upnext = self.queue_script.pop(0) # extrai as cartas a serem jogadas
            for pos in range(4):
                if upnext[pos] != None:                         # Se houver uma carta para ser jogada naquela posição da fila
                    if self.scribe_queue[pos] == None:          # e aquela posição da fila está vazia
                        self.scribe_queue[pos] = upnext[pos]    # Coloca a próxima carta na espera
                        print(f"O patrono se prepara para avançar a carta {self.scribe_queue[pos].name} na posição {pos+1}")
                    else:                                       # Caso não haja espaço
                        aux = ( None, None, None, None)         # Adiciona uma nova jogada ao script
                        aux[pos] = upnext[pos]                  # com a carta que seria posicionada
                        self.queue_script.append(aux)
            del upnext

    # Exibe todas as carta na mesa.

    def view_table(self):
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

    # Controla o turno do jogador. Poderia ter partes do código dividido em outros métodos para ficar mais organizado.

    def player_to_play(self):
        while self.player_turn == True:
            print("Digite 'hand' para exibir todas as cartas na sua mão junto a sua quantidade de Ossos.\n" \
            "Digite 'view' para exibir todas as cartas na mesa.\n" \
            "Digite 'play' para invocar uma carta de sua mão.\n" \
            "Digite 'bell' para encerrar seu turno.\n" \
            f"Estado atual da balança = {self.scale}")
            action = input()
            match action:
                case 'play': # Inicia uma tentativa de invocar uma carta
                    print(f"Digite o número da carta na sua mão que deseja jogar (1-{len(self.player.hand)}):")
                    card_index = int(input()) - 1                       # Lê a carta que o jogador que jogar e ajusta a posição
                    if 0 <= card_index < len(self.player.hand):
                        card_to_play = self.player.hand[card_index]     # Recebe a carta escolhida pelo jogador
                        ready = False                       # Se todos os requisitos são atingidos para que a carta possa ser posicionada
                        needed_cost_type = card_to_play.cost_type
                        needed_cost_amount = card_to_play.cost
                        if needed_cost_type == "Sangue":
                            blood_value = 0                             # Valor total de Sangue sacrificado até o momento
                            marked_index = []                           # Posição das cartas escolhidas para o sacrifício
                            if needed_cost_amount == 0:
                                free_position = False                   # Cartas sem custo precisam apenas de uma posição livre na mesa
                                for pos in range(4):
                                    if self.player_side[pos] == None:   # Procura uma posição vazia
                                        free_position = True
                                        break
                                if free_position == False:
                                    print("Não há espaço suficiente para invocar esta carta.")
                                    continue                    # Encerra a ação de jogar uma carta
                            while blood_value < needed_cost_amount:
                                print(f"É preciso sacrificar {needed_cost_amount-blood_value} de Sangue para invocar a carta {card_to_play.name}." \
                                f" Selecione uma carta do seu lado da mesa para sacrificar (1-4) ou '0' para cancelar:")
                                sacrifice_index = int(input()) - 1 # Lê a posição da carta que o jogador quer sacrificar
                                if sacrifice_index == -1:          # Cancela o sacrifício quando o jogador digitar '0'
                                    print("Invocação cancelada.")
                                    marked_index.clear()           # Cartas escolhidas para sacrifício até este momento não serão sacrificadas
                                    blood_value = 0
                                    break
                                if 0 <= sacrifice_index < 4:
                                    if self.player_side[sacrifice_index] == None:
                                        print("Esta posição está vazia.")
                                    else:
                                        sacrifice_worth = self.player_side[sacrifice_index].blood_sacrifice()
                                        if sacrifice_worth == 0:
                                            print("Esta carta não pode ser sacrificada.")
                                            continue
                                        blood_value += sacrifice_worth       # Adiciona o valor de sangue da carta escolhida ao total de Sangue sacrificado      
                                        marked_index.append(sacrifice_index) # Marca a carta escolhida para ser sacrificada
                                        print(f"A carta {self.player_side[sacrifice_index].name} será sacrificada por {sacrifice_worth} de Sangue.")
                                else:
                                    print("Índice de carta inválido. Tente novamente.")
                            for index in marked_index: # Executa o sacrificio de todas as cartas marcadas para serem sacrificadas
                                self.player_bones += self.player_side[index].sacrifice(self.player_side) # O sacrifício retorna a quantidade de Ossos da carta sacrificada
                            if needed_cost_amount == 0:
                                print(f"Digite uma posição livre para invocar a carta {card_to_play.name} (1-4:)") # Cartas sem custo não precisam de sacrifício
                                ready = True                       # Indica que a carta está pronta para ser jogada
                            elif blood_value == needed_cost_amount:
                                print(f"Sacrificio completo. Digite uma posição livre para invocar a carta {card_to_play.name} (1-4):")
                                ready = True            
                            elif blood_value > needed_cost_amount: # É possivel exceder a quantidade necessária para um sacrifício. Isso não traz qualquer consequência
                                print(f"Sacrificio excedente. Digite uma posição livre para invocar a carta {card_to_play.name} (1-4):")
                                ready = True
                        elif needed_cost_type == "Ossos":
                            free_position = False
                            for pos in range(4):                  # Cartas de Ossos sempre precisam de uma posição livre para serem jogadas,
                                if self.player_side[pos] == None: # visto que sem algum sacrifício não é possível abrir espaço na mesa
                                    free_position = True
                                    break
                            if free_position == False:
                                print("Não há espaço suficiente para invocar esta carta.")
                                continue                          # Encerra a ação de jogar uma carta
                            if self.player_bones >= needed_cost_amount: # Se o jogador possui Ossos suficientes para jogar a carta escolhida
                                self.player_bones -= needed_cost_amount # deduz esse custo dos Ossos do jogador
                                print(f"Digite uma posição livre para gastar {needed_cost_amount} Ossos e invocar a carta {card_to_play.name} (1-4):")
                                ready = True                            # e indica que a carta está pronta para ser jogada
                            else:
                                print("Ossos insuficientes para invocar esta carta.")
                        while ready == True:                            # Se a carta estiver pronta para ser jogada
                                placement_index = int(input()) - 1      # Lê a posição escolhida pelo jogador para posicionar a carta
                                if 0 <= placement_index < 4:
                                    if self.player_side[placement_index] == None:                   # Se não houver nenhuma carta na posição escolhida
                                        self.player_side[placement_index] = card_to_play            # coloca a carta naquela posição da mesa
                                        self.player_side[placement_index].pos = placement_index + 1 # altera a posição da carta para a posição escolhida
                                        self.player.hand.pop(card_index)                            # remove a carta da mão do jogador
                                        ready = False                                               # Encerra o posicionamento da carta
                                    else:
                                        print(f"Esta posição já está ocupada. Escolha outra posição para invocar a carta {card_to_play.name}:")
                                else:                                                       # Note que uma vez que a carta está pronta para ser jogada,
                                    print("Posição inválida. Tente novamente (1-4).")       # não é possivel cancelar esta ação
                    else:
                        if len(self.player.hand) == 0:
                            print("Não há cartas em sua mão para jogar.")
                        else:
                            print("Índice de carta inválido. Tente novamente.")
                case 'bell': # Aperta o sino na mesa, encerrando o turno do jogador
                    return 
                case 'hand': # Exibe a quantidade de Ossos e as cartas na mão no jogador
                    print(f"Ossos: {self.player_bones}")
                    if len(self.player.hand) == 0:
                        print("Não há cartas em sua mão.")
                    else:
                        print("Cartas na sua mão:")
                        self.player.view_hand()
                case 'view': # Exibe todas as cartas posicionadas na mesa
                    self.view_table()
                case _:
                    print("Entrada inválida.")

    # Permite que o jogador escolha de qual deck deseja comprar no início de seu turno.

    def player_draw(self):
        card_drawn = False
        while card_drawn == False:
            if len( self.player.sidedeck.stack ) <= 0 and len( self.player.deck.stack ) <= 0: # Se não houverem mais cartas para o jogador comprar
                if self.starvation < 1: # Inicia a inanição, caso já não estiver presente
                    print("Sem cartas para comprar. A fome aparece.")
                    self.starvation += 1
                    return self.starvation
                else:                   # Continua a inanição
                    print("Sem cartas para comprar. A fome se intensifica.")
                    self.starvation += 1
                    return self.starvation
            print("Digite 'deck' para comprar do deck principal ou 'side' para comprar do sidedeck:")
            chosen_deck = input()
            if chosen_deck == 'deck':
                if len( self.player.deck.stack ) > 0:       # Se houverem cartas no deck principal
                    draw = self.player.deck.draw()          # Compra a carta no topo do deck
                    self.player.hand.append( draw )         # e a insere na mão do jogador
                    card_drawn = True                       # Encerra a compra de carta
                    print(f"A carta {draw.name} foi adicionada à sua mão.")
                else:
                    print("Não há cartas restantes no deck principal.")
            elif chosen_deck == 'side':
                if len( self.player.sidedeck.stack ) > 0:   # Se houverem cartas no sidedeck
                    draw = self.player.sidedeck.draw()      # ^^
                    self.player.hand.append( draw )         # ^^
                    card_drawn = True                       # ^^
                    print(f"A carta {draw.name} foi adicionada à sua mão.")
                else:
                    print("Não há cartas restantes no sidedeck.")
            else:
                print("Entrada inválida. Tente 'deck' ou 'side':")
        return self.starvation
    
    # Quando o jogador está sem cartas para comprar em ambos os decks, a fome aparece para acabar com a batalha.
    
    def starve(self, intensity):
        check = random.choices( [ 0, 1, 2, 3 ] )    # Escolhe uma ordem aléatoria das posições no lado do patrono
        for pos in check:                           # Esta ordem é a preferência de onde a inanição deve agir
            if self.player_side[pos] == None:       # Caso a posição esteja livre
                self.player_side[pos] = Card(16)                            # Invoca uma inanição naquela posição
                self.player_side[pos].atk = intensity                       # Iguala o ataque à intensidade da fome
                self.player_side[pos].hp = intensity                        # Iguala a saúde à intensidade da fome
                if intensity > 4:                                           # Com intensidade 5 em diante
                    self.player_side[pos].sigils.add(Airborne.sigil_id())   # a inanição recebe o selo aéreo
                print("A Inanição surge diante de você.")
                return
        for pos in check:                                   # Quando não houver posição livre,
            if self.player_side[pos].name != "Inanição":    # a inanição tenta substituir outra carta presente
                self.player_side[pos] = Card(16)                            # ^^
                self.player_side[pos].atk = intensity                       # ^^
                self.player_side[pos].hp = intensity                        # ^^
                if intensity > 4:                                           # ^^
                    self.player_side[pos].sigils.add(Airborne.sigil_id())   # ^^
                print("A Inanição consome a criatura diante de você.")
                return
        for pos in check:   # Se todas as posições estiverem ocupadas pela inanição, fortaleçe a inanição já naquela posição
            self.player_side[pos].atk = intensity                           # ^^
            self.player_side[pos].hp = intensity                            # ^^
            if intensity > 4:                                               # ^^
                self.player_side[pos].sigils.add(Airborne.sigil_id())       # ^^
            print("A Inanição cresce ainda mais forte.")
            return
        
    # Executa o turno de combate do jogador.
        
    def call_combat_player(self):
        turn_damage = 0 # Total de dano causado diretamente ao oponente neste turno de combate
        turn_bones = 0  # Total de Ossos adquiridos neste turno de combate
        for pos in range(4):        # Inicia o ataque de cada carta, da esquerda para a direita da mesa
            attacker = self.player_side[pos]
            defender = self.scribe_side[pos]
            if attacker != None:    # Se houver uma carta naquela posição
                turn_damage += attacker.strike(self.player_side, self.scribe_side, defender) # Recebe o dano causado diretamente ao oponente por este ataque
                turn_bones += attacker.checkup(self.player_side)    # Recebe os Ossos obtidos, caso o atacante pereca
            if defender != None:    # Se houver uma carta defendendo a posição oposta
                turn_bones += defender.checkup(self.scribe_side)    # Recebe os Ossos obtidos, caso o defensor pereca
        self.scale += turn_damage   # Adiciona pesos no lado da balança do jogador igual ao dano causado diretamente ao oponente neste turno
        sprint = []                 # Guarda todas as cartas do jogador para verificar o selo veloz
        for card in self.player_side:
            if card != None:        # Pega todas as cartas do jogador posicionadas no campo ativo
                sprint.append(card)
        for card in sprint:
            if Sprinter.sigil_id() in card.sigils: # Este selo é ativado no fim do turno de quem possui a carta com o selo
                card.movement(self.player_side)    # Executa o efeito do selo
        return turn_bones
    
    # Executa o turno de combate do patrono.

    def call_combat_scribe(self):
        turn_damage = 0 # Total de dano causado diretamente ao oponente neste turno de combate
        turn_bones = 0  # Total de Ossos adquiridos neste turno de combate
        for pos in range(4):        # Inicia o ataque de cada carta, da esquerda para a direita da mesa
            attacker = self.scribe_side[pos]
            defender = self.player_side[pos]
            if attacker != None:    # Se houver uma carta naquela posição
                turn_damage += attacker.strike(self.scribe_side, self.player_side, defender) # Recebe o dano causado diretamente ao oponente por este ataque
                turn_bones += attacker.checkup(self.scribe_side)    # Recebe os Ossos obtidos, caso o atacante pereca
            if defender != None:    # Se houver uma carta defendendo a posição oposta
                turn_bones += defender.checkup(self.player_side)    # Recebe os Ossos obtidos, caso o defensor pereca
        self.scale -= turn_damage   # Adiciona pesos no lado da balança do patrono igual ao dano causado diretamente ao oponente neste turno
        sprint = []                 # Guarda todas as cartas do patrono para verificar o selo veloz
        for card in self.scribe_side:
            if card != None:        # Pega todas as cartas do patrono posicionadas no campo ativo
                sprint.append(card)
        for card in sprint:
            if Sprinter.sigil_id() in card.sigils: # Este selo é ativado no fim do turno de quem possui a carta com o selo
                card.movement(self.scribe_side)    # Executa o efeito do selo
        return turn_bones
    
    # Incrementa o contador de turnos de presença de cada carta na mesa.
    
    def age_cards(self, side):
        for card in side:
            if card != None:
                card.age += 1

    # Evolui cartas com o selo Infante na mesa.

    def evolve_cards(self, side):
        for card in side:
            if card != None:
                side[card.pos - 1] = card.evolve()
    
    # Executa a rotina de uma batalha.

    def host_table(self):
        self.scale = 0 # Reseta todos os atributos desta classe para uma nova batalha
        self.player_side = [ None, None, None, None ]
        self.scribe_side = [ None, None, None, None ]
        self.scribe_queue = [ None, None, None, None ]
        self.player_bones = 0
        self.ongoing = True
        self.player_turn = True
        self.starvation = 0
        self.queue_script = BatlleScript.random_script().copy()
        self.player.deck.deck_shuffle()     # Embaralha o deck principal do jogador
        self.player.sidedeck.deck_shuffle() # Embaralha o sidedeck do jogador
        for i in range (3):
            self.player.hand.append( self.player.deck.draw() ) # O jogador começa comprando 3 cartas de seu baralho principal
        self.player.hand.append( self.player.sidedeck.draw() ) # e uma de seu baralho de esquilos
        self.scribe_to_play()   # Executa a jogada inicial do patrono 
        self.view_table()       # Exibe o estado inicial da mesa
        print("Cartas na sua mão:")
        self.player.view_hand() # Exibe o estado inicial da mão do jogador
        while self.ongoing == True:
            if self.player_turn == True:
                self.player_to_play()                           # Executa o turno do jogador
                self.player_bones += self.call_combat_player()  # Recebe a quantidade de Ossos obtidos no turno de combate do jogador
                self.age_cards(self.player_side)                # Aumenta a idade das cartas do jogador na mesa
                self.evolve_cards(self.scribe_side)             # Evolui cartas do jogador com o selo infante 
                self.player_turn = False                        # Passa o turno para o patrono
                print(f"Estado atual da balança: {self.scale}") # Exibe o estado atual da balança
                if self.scale >= 5:                     # Se a balança medir 5 ou mais ao lado do jogador
                    self.ongoing = False                # Encerra a batalha
                    print("Você venceu a batalha.")     # e declara a vitória do jogador
                    return self.scale - 5               # Retorna a quantidade excedente de pesos no lado do jogador à necessária para vencer
            else:
                print("Vez do patrono")
                self.scribe_advance()                           # Avança as cartas nas posições de espera do patrono
                self.player_bones += self.call_combat_scribe()  # Recebe a quantidade de Ossos obtidos no turno de combate do patrono
                self.scribe_to_play()                           # Adiciona as cartas jogadas pelo patrono nas posições de espera
                self.age_cards(self.scribe_side)                # Aumenta a idade das cartas do patrono na mesa
                self.evolve_cards(self.player_side)             # Evolui cartas do patrono com o selo infante
                self.player_turn = True                         # Passa o turno para o jogador
                print(f"Estado atual da balança: {self.scale}") # Exibe o estado atual da balança
                if self.scale <= -5:                    # Se a balança medir 5 ou mais ao lado do patrono
                    self.ongoing = False                # Encerra a batalha
                    print("Você perdeu a batalha.")     # e declara a derrota do jogador
                    return -1
                hunger = self.player_draw() # Recebe 0 quando o jogador compra uma carta. Se o jogador for incapaz de comprar uma carta,
                if hunger > 0:              # recebe o valor da intensidade da fome
                    self.starve(hunger)     # Ativa a inanição

# Contém scripts de jogadas para serem usados pelo patrono em batalhas.

class BatlleScript():
    script_1 = [ ( None, Card(2), None, None ), ( None, None, None, Card(5) ), ( None, None, None, None ), ( None, Card(8), None, None) ]
    script_2 = [ ( Card(8), None, None, None ), ( None, None, None, Card(10) ), (None, Card(11), None, None )]
    script_3 = [ ( None, None, Card(14), None ), ( Card(2), None, None, None), ( None, None, Card(15), None ), ( None, None, None, None ),
                 ( None, None, None, Card(3) )]

    all_scripts = [ script_1, script_2, script_3 ]

    @classmethod
    def random_script(cls):
        return random.choice( BatlleScript.all_scripts )

# Define todos os eventos que aparecem no mapa a ser trilhado pelo jogador. (incompleto)

class MapEvent():
    def __init__(self, name):
        self.name = name

    @classmethod
    def add_card(cls, player):
        print("Você se depara com 3 criaturas. Você deve escolher uma delas para adicionar ao seu baralho:")
        card_options = Deck.pick_cards(3)   # Oferece 3 cartas aleatórias ao jogador
        for i in range (3):
            print(f"Carta {i+1}")
            card_options[i].display_card()  # Exibe as cartas oferecidas
            print("")
        card_picked = False
        while card_picked == False:         # O jogador deve escolher uma das 3 cartas para adicionar ao seu deck
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


# A mesa contendo o mapa que o jogador percorre. (incompleto)    

class MapTable():
    def __init__(self, player, scribe):
        self.player = player
        self.scribe = scribe
        self.road = []

    def add_event_node(self, event_id):
        match event_id:
            case 1:
                self.road.append(MapEvent("battle"))
            case 2:
                self.road.append(MapEvent("add_card"))
        return
