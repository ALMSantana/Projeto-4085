from assistentes import Assistente

def avaliar_codigo():
    nome_assistente = "Avaliador de Código"
    instrucoes_assistente = """
    Você receberá um script em Python que resolve um problema computacional.
    Seu objetivo é avaliar a complexidade de algoritmo desta solução e dar um parecer ao final do processo.
    
    # Para isso:
    
    1. Faça uma leitura do Script, analisando seu propósito e associando ao pedido do usuário
    2. Faça uma análise da complexidade do algoritmo implementado, considerando o pior caso
    3. Faça uma análise da eficiência do algoritmo, considerando o uso de memória e processamento
    4. Dê um parecer final sobre a solução, indicando se é adequada para o problema proposto
    5. Caso identifique oportunidades de melhoria, sugira alterações ou otimizações
    """

    return Assistente(nome = nome_assistente, instrucoes = instrucoes_assistente)
    
    
def pergunta_assistente_monitoramento(pergunta, caminho_script):
    assistente = avaliar_codigo()

    while pergunta != "fim":
        resposta = assistente.perguntar(pergunta=pergunta, caminho_arquivo=caminho_script, continuacao_conversa=True)
        print(resposta) 
        pergunta = input("\n~Digite sua próxima pergunta ao assistente (ou 'fim' para encerrar): ")

    assistente.apagar_agente()

def main():
    #caminho_script = alocador.py
    #pergunta_inciial = Faça uma avaliação do script abaixo e dê um aparecer para o método alocacao_exaustiva.
    caminho_script = input("Digite o nome do script que você enviará ao assistente: ")
    pergunta_inicial = input("Digite sua primeira pergunta ao assistente: ")
    print("\n")

    pergunta_assistente_monitoramento(pergunta=pergunta_inicial, caminho_script=caminho_script)
    

if __name__ == "__main__":
    main()