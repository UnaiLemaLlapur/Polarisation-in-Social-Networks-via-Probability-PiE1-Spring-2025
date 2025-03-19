import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from yogi import read
from typing import Callable

def r1(x:float)->float:
    """Devuelve la probabilidad de exponer a contenido politico de izquierda según la regla 'reinforcement'"""
    return (1-x)**2/((1+x)**2+(1-x)**2)

def r2(x:float)->float:
    """Devuelve la probabilidad de exponer a contenido politico de izquierda según la regla 'fair'"""
    return (1-x)/2

def r3(x:float)->float:
    """Devuelve la probabilidad de exponer a contenido politico de izquierda según la regla 'opposite'"""
    return (1+x)/2

def establecer_modelo_regla(n:int)->tuple[np.ndarray,Callable,str,str]:
    """Permite elegir el modelo Xt (S1 o S2) y la regla (R1,R2 o R3)"""
    print("Escriba el modelo de Xt a elegir: S1 o S2")
    modelo=read(str)
    if modelo=="S1":
        xt=np.random.uniform(-1,1,n)
        print("Modelo S1 elegido: Xt~U[-1,1]")
    else:
        xt=np.random.normal(0,sqrt(1/13),n) #en numpy el modelo normal coge como parámetros N(u,sigma) y no sigma**2
        print("Modelo S2 elegido: Xt~N(0,sigma**2=1/13))")
    
    print("Escriba la regla a elegir: R1, R2 o R3")
    nom_regla=read(str)
    if nom_regla=="R1":
        regla=r1
        print("Regla R1 elegida: Reinforcement Rule")
    elif nom_regla=="R2":
        regla=r2
        print("Regla R2 elegida: Fair Rule")
    else:
        regla=r3
        print("Regla R3 elegida: Opposite Rule")
    return (xt,regla,modelo,nom_regla)

def siguiente_opinion(xt:np.ndarray,regla:Callable)->None:
    """Calcula xt+1"""
    for i in range(len(xt)):
        if np.random.random()<=regla(xt[i]): #Contenido de izquierdas
            xt[i]=xt[i]-(1+xt[i])/4
        else:                   #Contenido de derechas
            xt[i]=xt[i]+(1-xt[i])/4

def dibujar_histograma(xt:np.ndarray,modelo:str,nom_regla:str)->None:
    """Dibuja el histograma de las opiniones politicas"""
    columnas:list[float]=[-1,-0.7,-0.2,0,0.2,0.7,1] #define los intervalos de las columnas del histograma
    plt.hist(xt,bins=columnas,edgecolor='black') #Define el histograma con las opiniones finales xt

    plt.title(f'Histograma de las opiniones políticas finales Xt siguiendo el modelo {modelo} y la regla {nom_regla}')
    plt.xlabel('Opiniones políticas')
    plt.ylabel('Número de personas')
    plt.show()


def main()->None:
    n=10000
    t=15
    xt,regla,modelo,nom_regla=establecer_modelo_regla(n)    #regla funcionará com una de las funciones r1, r2 o r3 según la selección
    for i in range(t):
        siguiente_opinion(xt,regla)
    dibujar_histograma(xt,modelo,nom_regla)
main()