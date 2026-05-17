# Os selos são propriedades/habilidades especiais que mudam a forma como as cartas interagem umas com as outras nas batalhas.
# Os selos são identificados por nome e seguem a tradução oficial de Inscryption.
# Apenas alguns dos selos do jogo estão presentes pois não houve tempo de implementar todas as interações de todos os selos
# (São mais de 30 selos no jogo original).

class Sigil():
    name = "Sigil"
    @classmethod
    def sigil_id(cls):
        return cls.name

class MightyLeap(Sigil):
    name = "Salto Pujante"
    desc = "Esta criatura bloqueia criaturas diante dela que tenham o selo aéreo."

class Stinky(Sigil):
    name = "Fedor"
    desc = "A criatura diante desta criatura perde 1 de poder."

class Fledgling(Sigil):
    name = "Infante"
    desc = "Esta criatura se transforma em uma forma mais poderosa depois de um turno no tabuleiro."

class Leader(Sigil):
    name = "Líder"
    desc = "Criaturas adjacentes a esta criatura ganham 1 de poder."

class Airborne(Sigil):
    name = "Aéreo"
    desc = "Esta criatura ataca o oponente diretamente, mesmo que haja uma criatura diante dela."

class Sprinter(Sigil):
    name = "Veloz"
    desc = "Esta criatura se move na direção indicada no selo (inicialmente direita) no final do turno de quem a possuir."

class Repulsive(Sigil):
    name = "Repugnância"
    desc = "Impede que esta criatura seja atacada por outra."

class WorthySacrifice(Sigil):
    name = "Sacrifício Digno"
    desc = "Esta criatura concede 3 de Sangue (ao invés de de 1) ao ser sacrificada."

class BoneKing(Sigil):
    name = "Colheita de Ossos"
    desc = "Quando esta criatura morre, concede 4 Ossos em vez de 1."