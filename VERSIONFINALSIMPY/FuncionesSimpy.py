"""     HDT5 ESTRUCTURA DE DATOS - Algoritmos y Estructuras de datos
Paula Camila Gonzalez Ortega  Carnet: 18398   -     Maria Ines Vasquez Figueroa   Carnet: 18250
Este archivo contiene las operaciones estadisitcas necesarias para calcular el promedio de tiempo
que un proceso esta en la computadora y la desviacion estandar de dicho tiempo"""

import statistics as stats

def promedio(lista):
    return stats.mean(lista)

def desvest(lista):
    return stats.pstdev(lista)
