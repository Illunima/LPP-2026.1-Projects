from Deck import Deck, SideDeck

class Player:
    def __init__(self):
        self.deck = Deck()
        self.deck.starting_deck_1()
        self.side_deck = SideDeck()
        self.hand = []
        self.scale = 0