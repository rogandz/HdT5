import random
import simpy

semilla = 42 # semilla para la generacion de randoms
totalProcesos = 25 # procesos que se deben realizar para terminar la simulacion
intervaloProcesos = 10.0 # intervalo en que se generar los procesos

def generarProcesos(env, number, interval, memory, resource): # parametros: enviroment; numero total de procesos a crear; en que intervalo se crean; la memoria que necesita; el recurso que utilizara
	for i in range(number):
		proceso = crearProceso(env, 'PID%d'%i, memory, resource)
		env.process(proceso)
		nuevoProceso = random.expovariate(1.0/interval)
		yield env.timeout(nuevoProceso)

def crearProceso(env, name, memory, resource):

	print('%s'%(name))

	mem = random(1,10,1)
	print('%s necesita %d de RAM'%(name,mem))
	yield memory.get(mem)

	with resource.request() as req:

		ready = yield req

		if req in ready:

			cpu = random(1,10,1)
			print ('%s tiene que %d instrucciones'%(name, cpu))
			yield resource.get(cpu)
			

random.seed(semilla)
env = simpy.Environment()

RAM = simpy.Container(env, init=100, capacity=100) # memoria disponible para realizar los procesos
CPU = simpy.Resource(env, capacity=1) 

env.process(generarProcesos(env,totalProcesos, intervaloProcesos, RAM, CPU))
env.run()
