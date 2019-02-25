"""     HDT5 ESTRUCTURA DE DATOS - Algoritmos y Estructuras de datos
Paula Camila Gonzalez Ortega  Carnet: 18398   -     Maria Ines Vasquez Figueroa   Carnet: 18250
Este programa utiliza simulación y colas de SimPy (DES, Resources y Container) para
simular la corrida de programas en un sistema operativo que funciona bajo la logistica de
 ''proceso a un programa que se ejecuta'' """
import random
import simpy
import math
from math import sqrt
from FuncionesSimpy import promedio, desvest

RANDOM_SEED = 300
PROCESOS_A_REALIZAR = 200 # numero total de procesos que se puede editar para la experimentacion
INTERVALO = 1  # Genera un nuevo proceso cada segundo
CANTIDAD_RAM_CPU = 100 # cantidad de ram cpu
CANTIDAD_INSTRUCCIONES_PROCESO = random.randint(1, 10)  # contiene cantidad de instrucciones de un proceso que será un numero random de 1 a 10
LISTA_TIEMPOS =[]


def proceso(env, number, interval, cpu_ram_total, CPU):
    # Genera Proceso random

    for i in range(number):
        p = new(env, 'Proceso %02d' % (i+1), cpu_ram_total, CPU)  # crea proceso
        env.process(p)
        t = random.expovariate(1.0 / interval)  # creación de proceso con una distribución exponencial
        yield env.timeout(t)  # espera una unidad de tiempo


# Se determina la cantidad de ram necesaria para el proceso
def new(env, name, cpu_ram_total, CPU):
    min = 1  # Minimo de espacio en RAM necesario y de instrucciones por proceso
    max = 10  # Maximo de espacio en RAM necesario y de instrucciones por proceso
    p_ram = random.randint(min, max)  # cantidad de ram a utilizar por el proceso
    instruccion_proceso = random.randint(min, max)  # cantidad de instrucciones que contiene el proceso
    with cpu_ram_total.get(p_ram) as req:  # pide utilizar cierta cantidad de ram al CPU
        yield req  # espera la respuesta
        start = env.now
        print('%s    RAM necesaria: %s    Instrucciones del proceso: %s   Cantidad de RAM actual: %.1f' % (
            name, p_ram, instruccion_proceso, cpu_ram_total.level))
    r = running(env, p_ram, cpu_ram_total, instruccion_proceso,
                CPU, LISTA_TIEMPOS)  # se crea un proceso running (ver metodo abajo)
    env.process(r)  ## Se efectura el proceso previo

def running(env, p_ram, cpu_ram_total, instruccion_proceso, CPU, LISTA_TIEMPOS):
    global tiempofinal
    global tiempo2
    global totalwait
    global suma
    suma = 0

    # se ejecuta mientras hayan instrucciones a ejecutar en el proceso
    while instruccion_proceso > 0:
        decision = random.choice([1, 2])  # random para determinar si el proceso se ejecuta o se pone en espera
        arrive = env.now  # lleva en control del tiempo
        with cpu.request() as reqcpu:  # entra a cpu a ejecutar procesos
            yield reqcpu
            yield env.timeout(1)
            if instruccion_proceso > 3:  # si el proceso tiene mas de 3 instrucciones, se ejecutan 3
                instruccion_proceso = instruccion_proceso - 3

                yield env.timeout(1)

                if decision == 2:  # si despues de ejecutar sale esperar , el proceso se ejecuta hasta que salga siguiente
                    with CPU.request() as reqwait:
                        yield reqwait
                        yield env.timeout(10)
            else:
                instruccion_proceso = 0

    # si no hay ram disponible, se libera con el numero de procesos utilizados
    with cpu_ram_total.put(p_ram) as reqmem:
        yield reqmem
    wait = env.now - arrive
    LISTA_TIEMPOS.append(wait) #Se agrega el tiempo utilizado a la lista para obtener el promedio
    totalwait = totalwait + wait  # sumatoria del tiempo utilizado


print("Inicia simulacion de Sistema Operativo")
random.seed(RANDOM_SEED)
env = simpy.Environment()
cpu_ram_total = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=1)# Resource de solo 1 CPU o la cantidad que desee

# Se empieza la simulacion
cpu = simpy.Resource(env, capacity=3)  # CPU con capacidad de ejecutar la cantidad de intrucciones predeterminada por capacity
totalwait = 0
env.process(proceso(env, PROCESOS_A_REALIZAR, INTERVALO, cpu_ram_total, CPU))
env.run()
print("\n---------------------------------------------------------------")
print("\n\t                   INFORME FINAL\n")
print("Tiempo total de simulación: " + str(totalwait) + " segundos")
## Se utilizan metodos de FuncionesSimpy.py para obtener datos estadisticos
print("Promedio de tiempo por proceso: " + str(promedio(LISTA_TIEMPOS)) + " segundos")
print("Desviacion estandar: "+str(desvest(LISTA_TIEMPOS)) + " segundos")
print("---------------------------------------------------------------")

