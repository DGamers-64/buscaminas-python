import random, os

class Tablero:
    minas: int
    ancho: int
    alto: int
    casillas: list
    casillasFalsas: list

    def __init__(self, minas, ancho, alto):
        if minas >= (ancho * alto):
            self.minas = 5
            self.ancho = 5
            self.alto = 5
        else:
            self.minas = minas
            self.ancho = ancho
            self.alto = alto

    def generarTableroReal(self):
        self.casillas = [[] for i in range(self.alto)]
        for i in range(len(self.casillas)):
            self.casillas[i] = [0 for i in range(self.ancho)]
        for i in range(self.minas):
            colocada = False
            while colocada == False:
                fila = random.randint(0,self.alto-1)
                columna = random.randint(0,self.ancho-1)
                if self.casillas[fila][columna] != "O":
                    self.casillas[fila][columna] = "O"
                    listaCoordsAdyacentes = self.listaCoordsAdyacentes(fila, columna)
                    for i in listaCoordsAdyacentes:
                        if self.casillas[i[0]][i[1]] != "O":
                            self.casillas[i[0]][i[1]] += 1
                    colocada = True
                else:
                    continue
        for i in range(len(self.casillas)):
            for j in range(len(self.casillas[i])):
                if self.casillas[i][j] == 0:
                    self.casillas[i][j] = " "

    def generarTableroFalso(self):
        self.casillasFalsas = [[] for i in range(self.alto)]
        for i in range(len(self.casillasFalsas)):
            self.casillasFalsas[i] = ["■" for i in range(self.ancho)]

    def dibujarTableroReal(self):
        for i in range(self.alto):
            print(" · ", end="")
            for j in range(self.ancho):
                print("— · ", end="")
            print()
            print(" | ", end="")
            for j in range(self.ancho):
                print(self.casillas[i][j], " | ", sep="", end="")
            print()
        print(" · ", end="")
        for j in range(self.ancho):
            print("— · ", end="")
        print()
        print()

    def dibujarTableroFalso(self):
        for i in range(self.alto):
            print(" · ", end="")
            for j in range(self.ancho):
                print("— · ", end="")
            print()
            print(" | ", end="")
            for j in range(self.ancho):
                print(self.casillasFalsas[i][j], " | ", sep="", end="")
            print()
        print(" · ", end="")
        for j in range(self.ancho):
            print("— · ", end="")
        print()
        print()

    def preguntarCoordenadas(self):
        print(" Fila > ", end="")
        fila = int(input())
        print(" Columna > ", end="")
        columna = int(input())
        return (fila-1, columna-1)
    
    def limpiarCasilla(self, fila, columna):
        self.casillasFalsas[fila][columna] = self.casillas[fila][columna]
        if self.casillasFalsas[fila][columna] == " ":
            self.limpiarCeros(fila, columna)

    def comprobarBomba(self):
        for i in self.casillasFalsas:
            if "O" in i:
                return True
        return False
    
    def limpiarConsola(self):
        os.system("cls")

    def ganador(self):
        contador = 0
        for i in self.casillasFalsas:
            for j in i:
                if j == "■":
                    contador += 1
        if contador == self.minas:
            return True
        else:
            return False

    def listaCoordsAdyacentes(self, fila, columna):
        lista = []
        if fila > 0:
            lista.append((fila-1, columna))
        if fila > 0 and columna > 0:
            lista.append((fila-1, columna-1))
        if fila > 0 and columna < self.ancho-1:
            lista.append((fila-1, columna+1))
        if fila < self.alto-1:
            lista.append((fila+1, columna))
        if fila < self.alto-1 and columna > 0:
            lista.append((fila+1, columna-1))
        if fila < self.alto-1 and columna < self.ancho-1:
            lista.append((fila+1, columna+1))
        if columna > 0:
            lista.append((fila, columna-1))
        if columna < self.ancho-1:
            lista.append((fila, columna+1))
        return lista
    
    def limpiarCeros(self, fila, columna):
        listaAdyacentes = self.listaCoordsAdyacentes(fila, columna)
        listaVecinos = []
        for i in listaAdyacentes:
            if self.casillasFalsas[i[0]][i[1]] == "■":
                listaVecinos.append(i)
        for i in listaVecinos:
            self.casillasFalsas[i[0]][i[1]] = self.casillas[i[0]][i[1]]
        listaCeros = []
        for i in listaVecinos:
            if self.casillasFalsas[i[0]][i[1]] == " ":
                listaCeros.append(i)
        for i in listaCeros:
            self.limpiarCeros(i[0],i[1])
        return

def main():
    print("Ancho: ", end="")
    ancho = int(input())
    print("Alto: ", end="")
    alto = int(input())
    print("Minas: ", end="")
    minas = int(input())
    tablero = Tablero(minas, ancho, alto)
    tablero.limpiarConsola()
    tablero.generarTableroReal()
    tablero.generarTableroFalso()
    while not tablero.comprobarBomba() and not tablero.ganador():
        tablero.dibujarTableroFalso()
        fila, columna = tablero.preguntarCoordenadas()
        tablero.limpiarCasilla(fila, columna)
        tablero.limpiarConsola()
    tablero.dibujarTableroReal()
    if tablero.comprobarBomba():
        print("┌──────────┐")
        print("│ SE ACABÓ │")
        print("└──────────┘")
    elif tablero.ganador():
        print("┌────────────┐")
        print("│ HAS GANADO │")
        print("└────────────┘")
    input()

if __name__ == "__main__":
    main()