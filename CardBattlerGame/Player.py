from Deck import Deck, SideDeck

class Player():
    def __init__(self):
        self.deck = Deck()
        self.deck.starting_deck_1()
        self.sidedeck = SideDeck()
        self.hand = []
        self.scale = 0

    def view_deck(self):
        for card in self.deck.cards:
            card.display_card()
            print("")

    def view_hand(self):
        for i in range( len(self.hand) ):
            print(f"Carta {i+1}")
            self.hand[i].display_card()
        print("")