import time
import psutil
import pandas as pd
from itertools import permutations
from threading import Thread

class AlocadorTarefas:
    '''
    Classe responsável por encontrar a melhor alocação de tarefas em servidores.
    '''

    def __init__(self, tarefas, servidores):
        '''
        Inicializa o alocador com uma lista de tarefas e uma lista de servidores.
        :param tarefas: Lista de objetos Tarefa.
        :param servidores: Lista de objetos Servidor.
        '''
        self.tarefas = tarefas
        self.servidores = servidores
        self._monitorando = False 

    def alocar_exaustivo(self, nome_arquivo = "padrao"):
        '''
        Método que realiza a alocação exaustiva de tarefas nos servidores.
        :return: Melhor alocação de tarefas e o tempo total mínimo de execução.
        '''
        start_time = time.time()
        self.memoria_registros = []
        self.memoria_maxima = 0
        self.iteracoes = 0
        
        self._monitorando = True
        monitor_thread = Thread(target=self._monitorar_memoria(nome_arquivo))
        monitor_thread.start()

        melhor_tempo = float('inf')
        melhor_alocacao = None

        for tentativa in permutations(self.tarefas):
            self.iteracoes += 1
            for servidor in self.servidores:
                servidor.tarefas.clear()

            for i, tarefa in enumerate(tentativa):
                self.servidores[i % len(self.servidores)].adicionar_tarefa(tarefa)

            tempo_atual = max(servidor.tempo_total_execucao() for servidor in self.servidores)

            if tempo_atual < melhor_tempo:
                melhor_tempo = tempo_atual
                melhor_alocacao = [[tarefa.id for tarefa in servidor.tarefas] for servidor in self.servidores]

        self.tempo_total_execucao = time.time() - start_time
        self._monitorando = False
        monitor_thread.join()  
        self._salvar_resultados(nome_arquivo=nome_arquivo)

        print(f"Melhor tempo de execução: {melhor_tempo}")
        print(f"Melhor alocação: {melhor_alocacao}")

        return melhor_alocacao, melhor_tempo

    def _monitorar_memoria(self, nome_arquivo = "padrao"):
        '''
        Método que monitora o consumo de memória a cada 50 ms.
        '''
        while self._monitorando:
            memoria_atual = psutil.Process().memory_info().rss / (1024 * 1024)  # Convertendo para MB
            self.memoria_registros.append(memoria_atual)
            self.memoria_maxima = max(self.memoria_maxima, memoria_atual)
            time.sleep(0.05)

        df = pd.DataFrame({
            'timestamp': pd.date_range(start=pd.Timestamp.now(), periods=len(self.memoria_registros), freq='50L'),
            'memoria_mb': self.memoria_registros
        })
        df.to_csv(f'{nome_arquivo}.csv', index=False)

    def _salvar_resultados(self, nome_arquivo = "padrao"):
        '''
        Método que salva os resultados do monitoramento em um arquivo CSV.
        '''
        media_memoria = sum(self.memoria_registros) / len(self.memoria_registros) if self.memoria_registros else 0
        dados = {
            'numero_iteracoes': self.iteracoes,
            'tempo_total': self.tempo_total_execucao,
            'qtd_media_memoria': media_memoria,
            'qtd_memoria_maxima': self.memoria_maxima,
        }
        df = pd.DataFrame([dados])
        df.to_csv(f'{nome_arquivo}.csv', index=False, sep=',')
