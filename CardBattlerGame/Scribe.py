from Player import Player
from Playtables import MapTable

class Scribe():
    def __init__(self):
        self.style = 0
        self.player = Player()
        self.map = MapTable(self.player, self)

    def test_map(self):
        self.map.add_event_node(1)
        self.pam.add_event_node(0)