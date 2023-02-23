class player():
    def __init__(self,name="", game=""):
        self.name = name
        self.game = game

    def get_game (self):
        while True:
            self.game = input(f'{self.name} por favor indica que juego quieres jugar [H] Horca [G] Guillotina: ')
            if self.game in ('H', 'G'):
                break
            print('Debes ingresar [H] o [G]')

class game():
    def __init__(self,player):
        self.player = player
        self.tries = 0
        self.choice_type_game(self.player.game)
      

    def choice_type_game(self,type):
        #Dependiendo del juego desarrollamos los tableros y porque reemplazaremos cada linea
        if self.player.game == 'H':
            self.table = [[None]*3 for i in range(3)]
            self.replaces = [
                ('O',0,1),
                ('|',0,1),
                ('/',1,0),
                ('|',1,1),
                ("\\",1,2),
                ('/',2,0),
                ("\\",2,2)
            ]

    def get_table(self):
        tableStr = ' +---+\n |   |\n'
        for i in range(3):
            tableStr+= " "
            for j in range(3):
                tableStr += self.table[i][j].piece if self.table[i][j] else " "
            tableStr+=" |\n"
        tableStr+='     |\n =====\n'
        return tableStr         


print('***** INICIA EL JUEGO *****')

player = player(name=input('Ingresa tu nombre: '))
player.get_game()

juego = game(player)

print(juego.get_table())