##HDT5 SIMULACION DE SISTEMA OPERATIVO CON SIMPY
##CAMILA GONZALES CARNE:
##MARIA INES VASQUEZ CARNE: 18250
import random
import simpy
import math
from math import sqrt
from FuncionesSimpy import promedio, desvest

RANDOM_SEED = 300
PROCESOS_A_REALIZAR = 100  # numero total de procesos y se puede editar para la experimentacion
INTERVALO = 1  # Generate new customers roughly every x seconds
CANTIDAD_RAM_CPU = 100  # cantidad ram cpu
CANTIDAD_INSTRUCCIONES_PROCESO = random.randint(1, 10)  # contiene cantidad de instrucciones de un proceso
ESPERAR_HABER_RAM = 300
LISTA_TIEMPOS =[]


def proceso(env, number, interval, counter, cpu_ram_total, waiting):
    """Source generates customers randomly"""

    for i in range(number):
        tiempo = env.now
        c = new(env, 'Proceso %02d' % i, cpu_ram_total, waiting)  # crea proceso
        env.process(c)
        t = random.expovariate(1.0 / interval)  # crear un numero randon distribucion exponencial
        yield env.timeout(t)  # espera un tiempo


# llega a start, donde decide si hay cantidad de ram suficiente para ser ejecutado
def new(env, name, cpu_ram_total, waiting):
    ram_proceso = random.randint(1, 10)  # conteiene la ram a utilizar de un proceso
    instruccion_proceso = random.randint(1, 10)  # instrucciones a ejectuar de nu proceso
    with cpu_ram_total.get(ram_proceso) as req:  # pide utilizar cierta cantidad de ram al cpu
        yield req  # espera
        start = env.now
        print('%s necesita cantidad de ram: %s  cantidad de instrucciones: %s camtidad de RAM actual : %.1f' % (
            name, ram_proceso, instruccion_proceso, cpu_ram_total.level))
    r = running(env, ram_proceso, cpu_ram_total, instruccion_proceso,
                waiting, LISTA_TIEMPOS)  # crea un proceso llamado runnig
    env.process(r)


def running(env, ram_proceso, cpu_ram_total, instruccion_proceso, waiting, LISTA_TIEMPOS):
    global tiempofinal
    global tiempo2
    global totalwait
    global suma
    suma = 0

    # se ejecuta mientras hayan instrucciones
    while instruccion_proceso > 0:
        siguiente = random.choice([1, 2])  # paso para escoger el random si se ejecuta el proceso o no
        arrive = env.now  # toma el tiempo
        with cpu.request() as reqcpu:  # entra a cpu a ejecutar procesos
            yield reqcpu
            yield env.timeout(1)
            if instruccion_proceso > 3:  # si hay mas de 3 instrucciones que le reste 3
                instruccion_proceso = instruccion_proceso - 3

                yield env.timeout(1)

                if siguiente == 2:  # si despues de ejecutar sale esperar , le toca esperar al proceso hasta que salga siguiente
                    with waiting.request() as reqwait:
                        yield reqwait
                        yield env.timeout(10)


            else:
                instruccion_proceso = 0

    # si no hay ram, liberar mas ram , cantidad de procesos utilizados
    with cpu_ram_total.put(ram_proceso) as reqmem:
        yield reqmem
    wait = env.now - arrive
    LISTA_TIEMPOS.append(wait)
    totalwait = totalwait + wait  # calcular tiempo total


print("Inicia simulacion de Sistema Operativo")
random.seed(RANDOM_SEED)
env = simpy.Environment()
cpu_ram_total = simpy.Container(env, init=100, capacity=100)
waiting = simpy.Resource(env, capacity=1)

# Start processes and run
counter = simpy.Resource(env, capacity=1)  # recurso Resource de solo 1 CPU
cpu = simpy.Resource(env, capacity=3)  # CPU con capacidad de ejecutar la cantidad de intrucciones predeterminada por capacoty
totalwait = 0
env.process(proceso(env, PROCESOS_A_REALIZAR, INTERVALO, counter, cpu_ram_total, waiting))
env.run()
print("Tiempo total de: " + str(totalwait))
print("Promedio de tiempo por proceso : " + str(promedio(LISTA_TIEMPOS)))
print("Desviacion estandar: "+str(desvest(LISTA_TIEMPOS)))

