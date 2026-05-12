from Player import Player
from Scribe import Scribe
from Card import Card
from Playtables import BattleTable

scribe = Scribe()
player_1 = Player()
print("Este é seu deck inicial:")
player_1.view_deck()
extra_card = input("Digite o id de uma carta para adicioná-la ao seu deck, digite o id 0 para prosseguir: ")
if extra_card != "0":
    player_1.deck.add( Card(extra_card) )
test_battle = BattleTable( player_1, scribe )
test_battle.host_table()