from Player import Player
from Scribe import Scribe
from Card import Card
from Playtables import BattleTable, MapEvent
from Sigil import Sigil

scribe = Scribe()
player_1 = Player()
print("Este é seu deck inicial:")
player_1.view_deck()
move = input("Pressione enter para prosseguir")
MapEvent.add_card(player_1)
move = input("Pressione enter para prosseguir para a batalha")
test_battle = BattleTable( player_1, scribe )
session = test_battle.host_table()
while session >= 0:
    move = input("Pressione enter para prosseguir. digite 'exit' para sair: ")
    if move == 'exit':
        break
    MapEvent.add_card(player_1)
    print("Este é o seu deck atual:")
    player_1.view_deck()
    move = input("Pressione enter para prosseguir para a batalha. digite 'exit' para sair: ")
    if move == 'exit':
        break
    session = test_battle.host_table()