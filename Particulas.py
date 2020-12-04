from particula import Particula
import json

class Particulas:
    def __init__(self):
        self.contenedor = []
    
    def agregar_final(self, particula:Particula):
        self.contenedor.append(particula)
    
    def agregar_inicio(self, particula:Particula):
        self.contenedor.insert(0, particula)

    def mostrar(self):
        for particulas in self.contenedor:
            print(particulas)

    def __str__(self):
        return "".join(
            str(particulas) + '\n'for particulas in self.contenedor #añade cada particula como si fuera un string
        )#con las comillas creamos un string vacio y join recibe N cantidad de elementos

    def __len__(self):
        return len(self.contenedor)

    def __iter__(self):
        self.cont = 0

        return self

    def __next__(self):
        if self.cont < len(self.contenedor):
            particula = self.contenedor[self.cont]
            self.cont += 1
            return particula
        else:
            raise StopIteration # asi se mandas excepciones y el stop rompe el ciclo


    def guardar(self, ubicacion):
        try:
            with open(ubicacion, 'w') as archivo:
                lista = [particula.to_dict() for particula in self.contenedor]
                print(lista)
                json.dump(lista, archivo, indent=5)
            return 1
        except:
            return 0

    def abrir(self, ubicacion):
        try:
            with open(ubicacion, 'r') as archivo:
                lista = json.load(archivo)
                self.contenedor = [Particula(**particula) for particula in lista] # con los asteriscos las llaves y valres de json los convierta a parametros
            return 1
        except:
            return 0
    
