from algoritmos import distancia_euclidiana

class Particula:
    def __init__(self, id = 0, origenX = 0, origenY = 0, destinoX = 0, destinoY = 0, velocidad = 0, colorR = 0, colorG = 0, colorB = 0, distancia = 0):
        self.__id = id
        self.__origenX = origenX
        self.__origenY = origenY
        self.__destinoX = destinoX
        self.__destinoY = destinoY
        self.__velocidad = velocidad
        self.__colorR = colorR
        self.__colorG = colorG
        self.__colorB = colorB
        self.__distancia = distancia_euclidiana(origenX, origenY, destinoX, destinoY)

    def  __str__(self):
        return(
            'Id: ' + str(self.__id) + '\n' +
            'Origen X: ' + str(self.__origenX) + '\n' +
            'Origen Y: ' + str(self.__origenY) + '\n' +
            'Destino X: ' + str(self.__destinoX) + '\n' +
            'Destino Y: ' + str(self.__destinoY) + '\n' +
            'Velocidad: ' + str(self.__velocidad) + '\n' +
            'Color R: ' + str(self.__colorR) + '\n' +
            'Color G: ' + str(self.__colorG) + '\n' +
            'Color B:  ' + str(self.__colorB) + '\n' +
            'Distancia: ' + str(self.__distancia) + '\n'
        )


    @property
    def id(self):
        return self.__id

    @property
    def origenX(self):
        return self.__origenX

    @property
    def origenY(self):
        return self.__origenY

    @property
    def destinoX(self):
        return self.__destinoX

    @property
    def destinoY(self):
        return self.__destinoY

    @property
    def velocidad(self):
        return self.__velocidad

    @property
    def colorR(self):
        return self.__colorR

    @property
    def colorG(self):
        return self.__colorG

    @property
    def colorB(self):
        return self.__colorB

    @property
    def distancia(self):
        return self.__distancia
    
    def to_dict(self): #esto retorna un diccionario
        return {
            "id" : self.__id,
            "origenX" : self.__origenX,
            "origenY" : self.__origenY,
            "destinoX" : self.__destinoX,
            "destinoY" : self.__destinoY,
            "velocidad" : self.__velocidad,
            "colorR" : self.__colorR,
            "colorG" : self.__colorG,
            "colorB" : self.__colorB,
        }