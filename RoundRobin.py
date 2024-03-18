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
    
    def start(self):
        #Inicia os processos
        for i in range(len(self.processes)):
            self.processes[i] = Process()

        completedProcesses = []
        startTime = time.time()

        while len(self.processes) > 0:
            currentWait = time.time()
            current = self.processes.pop(0)

            executionTime = min(self.quantum, current.remainingTime)
            current.remainingTime -= executionTime
            current.returnTime += executionTime

            if current.remainingTime == 0:
                completedProcesses.append(current)
            
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

        averageWaitTime = (averageWaitTime / self.amountProcess) * 1000
        averageReturnTime = (averageReturnTime / self.amountProcess) * 1000
        #Calcula o tempo médio de execução por processo
        averageProcessTime = totalTime / self.amountProcess
        #Estima a quantidade de processos por milisegundo
        processesPerSecond = 1 / (averageProcessTime / 1000)

        print(f"Tempo médio de espera: {averageWaitTime:.2f} milisegundos")
        print(f"Tempo médio de retorno: {averageReturnTime:.2f} milisegundos")
        print(f"Processos por milisegundo: {processesPerSecond:.2f}")
        

quantum = 10 #Microsegundos
amountProcess = 100 

main = Main(quantum, amountProcess)
main.start()