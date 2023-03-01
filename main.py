import random
import json
import string

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
        self.failedLetters = []
        self.choice_type_game(self.player.game)
        self.choiceWord()

    def choiceWord(self):
        print()
        print('Resolviendo el listado de categorias...')
        print('Seleccionado al azar una categoria tematica...')

        with open('words.json','r') as f:
            data = json.loads(f.read())

        categories = list(data.keys())
        self.selectedCategory = random.choice(categories)
        self.word = random.choice(data[self.selectedCategory])
        
        print(f'La categoria seleccionada es: {self.selectedCategory}')
        print()
        print(f'Revolviendo el listado de palabras dentro de la categoría {self.selectedCategory}...')
        print(f'Seleccionando al azar una palabra de la categoría {self.selectedCategory}')

        self.uncompleteword = [None]*len(self.word)

    def choice_type_game(self,type):
        #Dependiendo del juego desarrollamos los tableros y porque reemplazaremos cada linea
        if self.player.game == 'H':
            self.table = [[None]*3 for i in range(3)]
            self.replaces = [
                ('O',0,1),
                ('|',1,1),
                ('/',1,0),
                ("\\",1,2),
                ('/',2,0),
                ("\\",2,2)
            ]

    def get_table(self):
        if self.player.game == 'H':
            tableStr = ' +---+\n |   |\n'
            for i in range(3):
                tableStr+= ""
                for j in range(3):
                    tableStr += self.table[i][j] if self.table[i][j] else " "
                tableStr+="  |\n"
            tableStr+='     |\n =====\n'
            return tableStr         

    def uncompleteWord(self):
        uncompleteString = ' '
        for i in range(len(self.word)):
            uncompleteString+= self.uncompleteword[i] if self.uncompleteword[i] else '_ '  

        return uncompleteString

    def failed(self):
        #Crear string de las letras que han fallado
        lista = ''
        for i in range(len(self.failedLetters)):
            lista+= self.failedLetters[i]
            lista+=' '
        print('Letras fallidas:', 'Aun no se han cometido errores' if len(self.failedLetters) == 0 else lista)
        

    def inputLetter(self):
        print()
        print(f'Categoria: {self.selectedCategory}')
        print('La palabra seleccionada es:', self.uncompleteWord())
        self.failed()
        #Peticion de la letra
        print()       
        while True:
            letter = input('Indique una letra o pulse (+) para elegir una letra al azar: ')
            if letter == '+':
                print('Seleccionando letra al azar...')
                while True:
                    select = random.choice(string.ascii_lowercase)
                    letterInputed = self.getLetter(select)
                    if letterInputed == True:
                        print(f'Letra seleccionada: {select}')
                        if self.tries != 0:    
                            print('¡Muchachos! detengan el montaje del cadalso por ahora')
                            print(self.get_table())
                        return self.checkWin()
                    elif letterInputed == False:
                        print(f'Letra seleccionada: {select}')
                        return self.wrongWord()
                break
            else:
                try:
                    taster = float(letter)
                    print('Debes ingresar una letra del abedecedario...')
                except:
                    X = self.getLetter(letter=letter)
                    if X == True:
                        if self.tries != 0 :
                            print('¡Muchachos! detengan el montaje del cadalso por ahora')
                            print(self.get_table())
                        return self.checkWin()
                    elif X == False:
                        return self.wrongWord()
                    else:
                        print('Esa letra ya se habia usado antes... ')
                        return self.wrongWord()
            
    def getLetter(self,letter):
        if letter in self.failedLetters:
            return None
        else:
            if letter in self.word:  
                if letter in self.uncompleteword:
                    return None
                else:
                    self.setLetter(letter=letter)
                    return True
            else:
                self.failedLetters.append(letter)
                return False  

    def setLetter(self,letter):
        for i in range(len(self.word)):
            if letter == self.word[i]:
                self.uncompleteword[i] = letter                   

    def wrongWord(self):
        if self.player.game == 'H':
            if self.tries == 0:
                print('Lo lamento pero empezo el montaje del cadalso')
                print(self.get_table())
                
            else:
                x = self.replaces[self.tries-1]
                self.table[x[1]][x[2]] = x[0]
                print('Sigan con el montaje del cadalso!!')
                print(self.get_table())
        self.tries+=1

        return False

    def checkWin(self):
        for i in range(len(self.word)):
            if self.word[i] != self.uncompleteword[i]:
                return False
        return True

    def whioutTries(self):
        if self.tries == 7:
            print('Has muerto!!!')
            self.get_table()
            return True
        return False

    def restart(self):
        while True:
            X = input('¿Desean volver a tomar la partida Si [S] No [N]?:')
            if X == 'S':
                return True
            elif X == 'N':
                print('*** GRACIAS POR JUGAR ***')
                return False
            else:
                print('Debes ingresar una opcion valida!!')

    def win(self):
        print('La palabra seleccionada es:', self.uncompleteWord())
        self.failed()
        print(f'¡Muy bien! La palabra es: {self.word}')
                
    def clear(self):
        self.choiceWord()
        self.tries = 0
        self.uncompleteword = [None]*len(self.word)
        self.table = [[None]*3 for i in range(3)] 
        self.failedLetters = []

#Inicia el juego

print('*** HORCA O GUILLOTINA ***')

player = player(name=input('Por favor indique nombre del (la) participante: '))
player.get_game()

juego = game(player)

while True:
    if juego.inputLetter():
        juego.win()
        print()
        if juego.restart():
            print('*******************************************************************************')
            juego.clear()
        else:
            break
    else:
        if juego.whioutTries():
            print()
            if juego.restart():
                print('*******************************************************************************')
                juego.clear()
            else:
                break
