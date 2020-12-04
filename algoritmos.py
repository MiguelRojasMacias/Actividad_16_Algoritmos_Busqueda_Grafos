import math

def distancia_euclidiana(origenX, origenY, destinoX, destinoY):
    x_1 = origenX
    y_1 = origenY
    x_2 = destinoX
    y_2 = destinoY

    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    return distancia

