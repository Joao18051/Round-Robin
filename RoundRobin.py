import random
import time

class Process:
    #Os processos são gerados pseudo aleatoriamente
    def __init__(self):
        self.burstTime = random.randint(1, 3000) /1000000 #Microsegundos
        self.awaitTime = 0
        self.remainingTime = self.burstTime
        self.returnTime = 0

class Main:
    def __init__(self, quantum, amountProcess):
        self.quantum = quantum /1000000 #Microsegundos
        self.amountProcess = amountProcess
        self.processes = [0 for _ in range(amountProcess)]
        self.awaitTime = 0
        self.returnTime = 0
        self.vasao = 0
    
    def start(self):
        #Inicia os processos
        for i in range(len(self.processes)):
            self.processes[i] = Process()

        completedProcesses = []
        vasao = 0
        startTime = time.time()

        while len(self.processes) > 0:
            currentWait = time.time()
            current = self.processes.pop(0)
            #print(f"Processo atual: Processo {current.burstTime}") Linha comentada
            executionTime = min(self.quantum, current.remainingTime)
            current.remainingTime -= executionTime
            current.returnTime += executionTime

            if current.remainingTime == 0:
                completedProcesses.append(current)

                endTime = time.time()
                if (endTime - startTime) * 1000000 > 1000: 
                    self.vasao += 1
                
            if current.remainingTime > 0:
                self.processes.append(current)

            for i in range(len(self.processes)):
                #Tempo de espera +tempo de troca de contexto, em microsegundos
                self.processes[i].awaitTime += time.time() -currentWait +(1/1000000)

        endTime = time.time()
        totalTime = (endTime - startTime) * 1000000

        averageWaitTime = 0
        averageReturnTime = 0
        for i in range(len(completedProcesses)):
            averageWaitTime += completedProcesses[i].awaitTime
            averageReturnTime += completedProcesses[i].awaitTime + completedProcesses[i].returnTime

        self.awaitTime = averageWaitTime = (averageWaitTime / self.amountProcess) * 1000
        self.returnTime = averageReturnTime = (averageReturnTime / self.amountProcess) * 1000

quantum = 10000 #Microsegundos
amountProcess = 100

m = 0
espera = 0
retorno = 0
vasao = 0
while m < 100:
    main = Main(quantum, amountProcess)
    main.start()
    m += 1
    espera += main.awaitTime
    retorno += main.returnTime
    vasao += main.vasao

print(f"Tempo médio de espera: {espera/100:.2f} milisegundos")
print(f"Tempo médio de retorno: {retorno/100:.2f} milisegundos")
print(f"Processos por milisegundos: {vasao/100:.2f}")