from Player import Player
from Scribe import Scribe
from Card import Card
from Playtables import BattleTable, MapEvent

scribe = Scribe()
player_1 = Player()
print("Este é seu deck inicial:")
player_1.view_deck()
#extra_card = input("Digite o id de uma carta para adicioná-la ao seu deck, digite o id 0 para prosseguir: ")
#try:
#    extra_card = int(extra_card)
#    if extra_card > 0 and extra card_ < 16:
#        player_1.deck.add( Card(extra_card) )
#except:
#    pass
move = input("Pressione enter para prosseguir")
MapEvent.add_card(player_1)
move = input("Pressione enter para prosseguir para a batalha")
test_battle = BattleTable( player_1, scribe )
test_battle.host_table()