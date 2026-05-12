from Card import Card
from Deck import Deck, Sidedeck
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
                    self.scribe_side.insert(i, self.scribe_queue[i])
                    self.scribe_queue.insert(i, None)         

    def scribe_to_play(self):
        self.scribe_advance
        upnext = self.queue_script.pop(0)
        for pos in range(4):
            if upnext[pos] != None:
                if self.scribe_queue[pos] == None:
                    self.scribe_queue[pos] = upnext[pos]
                else:
                    aux = ( None, None, None, None)
                    aux[pos] = upnext[pos]
                    self.queue_script.append(aux)
        del aux
        del upnext

    def player_to_play(self):
        self.player_draw

    def player_draw(self):
        card_drawn = False
        while card_drawn == False:
            print("Digite 'deck' para comprar do deck principal ou 'side' para comprar do sidedeck:")
            chosen_deck = input()
            if chosen_deck == 'deck':
                if len( self.player.deck.cards ) > 0:
                    self.player.hand.append( self.player.deck.draw() )
                    card_drawn = True
                else:
                    print("Não há cartas restantes no deck principal.")
            elif chosen_deck == 'side':
                if self.player.sidedeck.cards_left() > 0:
                    draw = self.player.sidedeck.draw()
                    self.player.hand.append( draw )
                    card_drawn = True
                    print(f"{draw} foi adicionado à sua mão.")
                else:
                    print("Não há cartas restantes no sidedeck.")
            elif len( self.player.sidedeck.cards ) <= 0 and len( self.player.deck.cards ) <= 0:
                if self.starvation < 1:
                    print("Sem cartas para comprar. A fome aparece.")
                    self.starvation += 1
                elif self.starvation > 0:
                    print("Sem cartas para comprar. A fome se intensifica.")
                    self.starvation += 1
            else:
                print("Entrada inválida. Tente 'deck' ou 'side':")

                

class BatlleScript():
    script_1 = [ ( None, None, None, None ), ( None, Card(2), None, None ), ( None, None, None, Card(5) ), ( None, Card(8), None, None) ]

    all_scripts = [ script_1 ]

    @classmethod
    def random_script(cls):
        return random.choice( BatlleScript.all_scripts )