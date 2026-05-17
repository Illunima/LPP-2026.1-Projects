from Card import Card
import random

# O deck de cartas do jogador existe em dois estados: completo e atual.
# O deck completo seria a coleção de cartas que o jogador possui ao longo do jogo.
# O deck atual é o deck usado comprar as cartas em uma batalha.

class Deck:
    def __init__(self):
        self.cards = [] # Deck completo
        self.stack = [] # Deck atual

    # Compra uma carta do deck atual.

    def draw(self):
        if len(self.stack) == 0:
            return None
        else:
            return self.stack.pop()
        
    # Adiciona uma carta ao deck completo.
        
    def add(self, card):
        self.cards.append(card)

    # Remove uma carta do deck completo.
    
    def remove(self, card):
        self.cards.remove(card)

    # Obtém a carta em uma posição do deck completo.
    
    def get_card(self, i):
        return self.cards.index(i)
    
    # Substitui uma carta no deck completo.
    
    def replace(self, old, new):
        self.cards.remove(old)
        self.cards.insert(new)

    # Embaralha as cartas do deck atual.
    
    def deck_shuffle(self):
        random.seed(None, 2)            # Gera uma nova seed com o horário do sistema
        self.stack.clear()              # Limpa o deck atual
        temp = self.cards.copy()        # Gera uma cópia do deck completo
        while len(temp) != 0:
            card = random.choice(temp)  # Escolhe uma carta aleatória da cópia
            temp.remove(card)           # Remove essa carta da cópia
            self.stack.append(card)     # e adiciona ao deck atual
    
    # Adiciona o conjunto inicial padrão de cartas ao deck completo

    def starting_deck_1(self):
        self.add(Card(1))
        self.add(Card(2))
        self.add(Card(3))
        self.add(Card(4))

    @classmethod
    def pick_cards(cls, amount):        # Gera uma seleção aleatória de todas as cartas disponíveis para adicionar ao deck.
        deck = Deck()                   # Um deck é criado com todas as cartas disponíveis e depois é embaralhado.
        cards = []                      # A seleção de cartas é formada comprando cartas desse deck embaralhado.
        for i in range(1, 16):          # Dessa forma, a selecão não terá cartas repetidas.
            deck.add(Card(i))
        deck.deck_shuffle()
        for i in range(amount):
            cards.append(deck.draw())
        return cards

# Também conhecido como deck de esquilos ou deck de sacrifícios.

class SideDeck(Deck):
    def __init__(self): # Contém 10 esquilos e até então não é modificado ao longo do jogo
        self.cards = [ Card(0), Card(0), Card(0), Card(0), Card(0), Card(0), Card(0), Card(0), Card(0), Card(0) ]
        self.stack = self.cards.copy()

    def deck_shuffle(self): # Não precisa ser embaralhado, apenas reabastecido
        self.stack = self.cards.copy()
