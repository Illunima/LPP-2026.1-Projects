from Card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []
        self.stack = []

    def draw(self):
        if len(self.stack) == 0:
            return None
        else:
            return self.stack.pop()
        
    def add(self, card):
        self.cards.append(card)
    
    def remove(self, card):
        self.cards.remove(card)
    
    def get_card(self, i):
        return self.stack.index(i)
    
    def replace(self, old, new):
        self.stack.remove(old)
        self.stack.insert(new)
    
    def shuffle(self):
        self.stack.clear()
        temp = self.cards.copy()
        while len(temp) != 0:
            card = random.choice(temp)
            temp.remove(card)
            self.stack.append(card)
    
    def starting_deck_1(self):
        self.add(Card(1))
        self.add(Card(2))
        self.add(Card(3))
        self.add(Card(4))


class SideDeck(Deck):
    def __init__(self):
        self.cards = [ Card(0), Card(0), Card(0), Card(0), Card(0), Card(0), Card(0), Card(0), Card(0), Card(0) ]
        self.stack = self.cards.copy()

    def shuffle(self):
        self.stack = self.cards.copy()
