from assistentes import Assistente

def criar_assistente():
    nome_assistente = "Analisador de Código"
    instrucoes_assistente = """
    - Função: Você é um assistente especializado em análise de código e arquivos de dados.
    - Interação: Um usuário enviará um script Python ou um arquivo CSV e fará perguntas específicas sobre o conteúdo.
    - Objetivo: Forneça respostas precisas, objetivas e didáticas, sempre baseadas no conteúdo fornecido. Evite respostas vagas ou subjetivas.
    
    # Procedimentos
    
    1. Verificação de Ferramentas:
    - Antes de iniciar a análise, verifique se alguma ferramenta específica foi chamada no script ou nos dados. Utilize os resultados dessa ferramenta, se aplicável.
    
    2. Análise de Script Python:
    - Leitura Inicial: Realize uma leitura do script para compreender seu propósito principal.
    - Resposta à Pergunta: Analise a pergunta do usuário e relacione-a ao conteúdo do script.
    - Ferramentas e Respostas: Avalie as respostas das ferramentas integradas ao script, se houver.
    - Construção de Parecer: Redija uma resposta objetiva, fornecendo as informações solicitadas pelo usuário.
    3. Análise de Conjunto de Dados (CSV):
    - Carregamento de Dados: Tente carregar os dados utilizando pandas. Use "," como separador padrão, e caso falhe, tente ";".
    - Acesso aos Dados: Verifique se os dados foram carregados corretamente e estão acessíveis.
    - Análise e Resposta: Realize a análise solicitada com base nos dados e entregue uma resposta clara e direta ao usuário.
    """

    return Assistente(nome = nome_assistente, instrucoes = instrucoes_assistente)
    
    
def conversa(pergunta, caminho_arquivo):
    assistente = criar_assistente()

    while pergunta != "fim":
        resposta = assistente.perguntar(pergunta=pergunta, caminho_arquivo=caminho_arquivo, continuacao_conversa=True)
        print(resposta) 
        pergunta = input("\n#Digite sua próxima pergunta ao assistente (ou 'fim' para encerrar): ")

    assistente.apagar_agente()

def main():
    #caminho_script = alocador.py
    #pergunta_inciial = Faça uma avaliação do script abaixo e dê um aparecer para o método alocacao_exaustiva.
    caminho_arquivo = input("Digite o caminho do arquivo que você deseja incluir na análise: ")
    pergunta_inicial = input("Digite sua primeira pergunta ao assistente: ")
    print("\n")

    conversa(pergunta=pergunta_inicial, caminho_arquivo=caminho_arquivo)
    

if __name__ == "__main__":
    main()