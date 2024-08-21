
import time
import psutil
import pandas as pd
from itertools import permutations
from threading import Thread

class Servidor:
    '''
    Classe que representa um servidor no qual as tarefas serão alocadas.
    '''

    def __init__(self, id):
        '''
        Inicializa o servidor com um identificador único e uma lista de tarefas vazia.
        :param id: Identificador único do servidor.
        '''
        self.id = id
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        '''
        Adiciona uma tarefa ao servidor.
        :param tarefa: Objeto Tarefa a ser adicionado ao servidor.
        '''
        self.tarefas.append(tarefa)

    def tempo_total_execucao(self):
        '''
        Calcula o tempo total de execução de todas as tarefas alocadas ao servidor.
        :return: Tempo total de execução.
        '''
        return sum(tarefa.tempo_execucao for tarefa in self.tarefas)


class Tarefa:
    '''
    Classe que representa uma tarefa que precisa ser alocada a um servidor.
    '''

    def __init__(self, id, descricao, tempo_execucao, criticidade):
        '''
        Inicializa a tarefa com os parâmetros fornecidos.
        :param id: Identificador único da tarefa.
        :param descricao: Descrição da tarefa.
        :param tempo_execucao: Tempo de execução necessário para a tarefa.
        :param criticidade: Nível de criticidade da tarefa (1 a 5, sendo 5 a mais crítica).
        '''
        self.id = id
        self.descricao = descricao
        self.tempo_execucao = tempo_execucao
        self.criticidade = criticidade

    def __repr__(self):
        '''
        Representação textual da tarefa, usada para exibição e debug.
        '''
        return f"Tarefa(id={self.id}, descricao='{self.descricao}', tempo_execucao={self.tempo_execucao}, criticidade={self.criticidade})"


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
        self._monitorando = False  # Flag para controlar o monitoramento

    def alocar_exaustivo(self):
        '''
        Método que realiza a alocação exaustiva de tarefas nos servidores.
        :return: Melhor alocação de tarefas e o tempo total mínimo de execução.
        '''
        start_time = time.time()
        self.memoria_registros = []
        self.memoria_maxima = 0
        self.iteracoes = 0
        
        # Inicia o monitoramento de memória
        self._monitorando = True
        monitor_thread = Thread(target=self._monitorar_memoria)
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
        monitor_thread.join()  # Aguarda o fim do monitoramento
        self._salvar_resultados()

        print(f"Melhor tempo de execução: {melhor_tempo}")
        print(f"Melhor alocação: {melhor_alocacao}")

        return melhor_alocacao, melhor_tempo

    def _monitorar_memoria(self):
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
        df.to_csv('teste_memoria.csv', index=False)

    def _salvar_resultados(self):
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
        df.to_csv('resumo_teste.csv', index=False, sep=',')

# Código de inicialização ou execução do script pode ser colocado aqui.
