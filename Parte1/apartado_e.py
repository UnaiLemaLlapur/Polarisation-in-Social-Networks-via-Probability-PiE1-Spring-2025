import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from typing import Callable


def actualizacion_opinion(x: float, contenido: int) -> float:
    """ Modifica el contenido basado en exposicion a contenido de izquierdas o de derechas. """
    if contenido == -1: #Contenido de izquierdas
        return x - (1 + x) / 4
    else: #Contenido de derechas
        return x + (1 - x) / 4

def abandono(n: int, regla: Callable[[float], int], distribucion: str) -> None:

    if distribucion == 'S1':
        x0 = np.random.uniform(-1,1,n) #Distribución U([-1,1])
    elif distribucion == 'S2':
        x0 = np.random.normal(0, sqrt(1/13), n) #Distribución N(0,σ^2 = 1/13)
        x0 = np.clip(x0, -1, 1) #asegurar que esté dentro de [-1,1]
    
    cuenta_abandonos: list[int] = []

    for x in x0:
        c = 0
        while True:
            c += 1
            contenido = regla(x) #Determinar si el contenido es de derechas o de izquierdas
            alineado = (contenido == -1 and x < 0) or (contenido == 1 and x > 0) #Comprovar si coincide con la opinion
            

            p_abandono = 0.05 if alineado else 0.25
            if np.random.random() < p_abandono:
                break

            x = actualizacion_opinion(x, contenido)

        cuenta_abandonos.append(c)
    columnas:list[int]=[0,10,20,30,40,50,60,70,80,90,100, 110]
    plt.hist(cuenta_abandonos, bins=columnas, edgecolor="black", alpha=0.7)
    plt.xlabel("Número de contenidos consumidos antes de abandonar")
    plt.ylabel("Número de usuarios")
    plt.title(f"Regla: {regla.__name__} | Distribución: {distribucion}")
    plt.show()
        

def R1(x: float) -> int:

    prob_izq = (1-x)**2 / ( (1+x)**2 + (1-x)**2 )
    if np.random.random() < prob_izq: 
        return -1  #Se muestra contenido de izquierda
    else: 
        return 1 #Se muestra contenido de derecha

def R2(x: float) -> int:
    
    prob_izq = (1-x)/2
    if np.random.random() < prob_izq: 
        return -1 
    else: 
        return 1

def R3(x: float) -> int:
    prob_izq = (1+x)/2
    if np.random.random() < prob_izq: 
        return -1 
    else: 
        return 1
    
def CompromisoBalanceado(x: float) -> int:
    """ Regla de Compromiso Balanceado (R4): 
        - Mayormente contenido alineado
        - Pequeña posibilidad de contenido contrario (mayor para opiniones extremas)
    """
    prob_izq = (1 - x) / 2 + (0.2 * (1 - abs(x))) / 2
    return -1 if np.random.rand() < prob_izq else 1


def main() -> None:

    N = 10000

    abandono(N,CompromisoBalanceado,'S1')
    abandono(N,CompromisoBalanceado,'S2')

    '''
    abandono(N, R1, 'S1')
    abandono(N, R2, 'S1')
    abandono(N, R3, 'S1')
    abandono(N, R1, 'S2')
    abandono(N, R2, 'S2')
    abandono(N, R3, 'S2')
    '''

if __name__ == '__main__':
    main()