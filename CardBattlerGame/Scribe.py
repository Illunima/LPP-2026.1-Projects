from Player import Player
from Playtables import MapTable

# O patrono é quem controla o jogo. Ele orquestra todos os eventos e batalhas ao longo do caminho.
# Nessa versão ele não é devidamente utilizado e está incompleto.

class Scribe():
    def __init__(self): # Apenas o patrono das bestas está presente nesta versão
        self.nature = "Beast"
        self.player = Player()
        self.map = MapTable(self.player, self)

    def test_map(self):
        self.map.add_event_node(2)
        self.map.add_event_node(1)