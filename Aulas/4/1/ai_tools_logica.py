def calcular_complexidade_tempo(argumentos):
    from assistentes import Assistente

    print("Chamei ferramenta de complexidade de tempo")
    nome_script = argumentos["nome_script"]
    metodo_avaliado = argumentos["metodo_avaliado"]
    

    nome_agente = "Assistente de Complexidade de Tempo"
    descricao_agente = """
        Este assistente é projetado para analisar e retornar a complexidade de um algoritmo utilizando a notação Big O. Ele fornece uma análise detalhada, incluindo a complexidade do algoritmo, o processo utilizado para verificar essa complexidade, quando a solução pode se tornar um problema, e possíveis soluções computacionais alternativas
        Instruções de Uso:
        1. **Complexidade do Algoritmo**: O assistente determinará a complexidade do algoritmo analisado e retornará no formato Big O. Por exemplo, O(n), O(log n), O(n^2), etc.
        2. **Processo de Verificação**: O assistente explicará como a complexidade foi determinada, seja através de análise de loops, recursões, ou outras estruturas algorítmicas.
        3. **Identificação de Problemas**: O assistente indicará quando a solução pode se tornar um problema em termos de desempenho, como em casos de grandes entradas de dados, limitações de tempo ou espaço.
        4. **Soluções Computacionais Conhecidas**: O assistente sugerirá possíveis soluções ou otimizações para melhorar a eficiência do algoritmo, como técnicas de memoização, uso de algoritmos alternativos ou melhorias na estrutura de dados.

        Formato da Resposta:

        1. **Complexidade**: A complexidade do algoritmo é **O(n log n)**.
        2. **Processo de Verificação**: A complexidade foi determinada analisando o loop principal que faz uma operação logarítmica dentro de um loop linear, resultando em O(n log n).
        3. **Quando se torna um problema**: Esta solução pode se tornar ineficiente com entradas superiores a 1 milhão de elementos, devido ao aumento exponencial do tempo de execução.
        4. **Soluções Computacionais**: Considerar a utilização de algoritmos de ordenação mais eficientes, como QuickSort ou MergeSort, ou técnicas de paralelização para grandes volumes de dados.

        Exemplo:
        ```python
        def algoritmo_exemplo(arr):
            for i in range(len(arr)):
                for j in range(1, len(arr)):
                    if arr[j] < arr[i]:
                        arr[i], arr[j] = arr[j], arr[i]
            return arr

        # Resposta do Assistente:

        # Complexidade: A complexidade do algoritmo é O(n^2).
        # Processo de Verificação: A complexidade foi determinada pela presença de dois loops aninhados que iteram sobre o array.
        # Quando se torna um problema: Esta solução se torna um problema para entradas com mais de 10 mil elementos, onde o tempo de execução aumenta significativamente.
        # Soluções Computacionais: Considerar a utilização de algoritmos de ordenação mais eficientes, como QuickSort ou MergeSort.
    """

    ferramenta = Assistente(nome=nome_agente, instrucoes=descricao_agente, eh_ferramenta=True)
    resposta = ferramenta.perguntar(
        pergunta = "Faça uma análise de complexidade de algoritmo para o método " + metodo_avaliado + " do script \nScript\n" + nome_script + ".",
        caminho_arquivo=nome_script
    )

    print(f"Resposta do assistente: {resposta}")

    ferramenta.apagar_agente()

    return resposta

