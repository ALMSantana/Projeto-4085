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


def calcular_complexidade_memoria(argumentos):
    from assistentes import Assistente

    print("Chamei ferramenta de complexidade de memória")
    nome_script = argumentos["nome_script"]
    metodo_avaliado = argumentos["metodo_avaliado"]
    

    nome_agente = "Assistente de Complexidade de Memória"
    descricao_agente = """
        Este assistente é projetado para analisar e retornar a complexidade de memória de um algoritmo utilizando a notação Big O. Ele fornece uma análise detalhada, incluindo a complexidade de memória do algoritmo, o processo utilizado para verificar essa complexidade, quando o uso de memória pode se tornar um problema, e possíveis soluções computacionais alternativas.

        Instruções de Uso:
        1. **Complexidade de Memória do Algoritmo**: O assistente determinará a complexidade de memória do algoritmo analisado e retornará no formato Big O. Por exemplo, O(n), O(log n), O(n^2), etc. A resposta deve incluir tanto o melhor caso quanto o pior caso de complexidade de memória, explicando em quais condições cada caso se aplica.
        2. **Processo de Verificação**: O assistente explicará como a complexidade de memória foi determinada, seja através de análise de variáveis, estruturas de dados utilizadas, ou alocação de memória durante a execução.
        3. **Identificação de Problemas**: O assistente indicará quando o uso de memória pode se tornar um problema, como em casos de grandes entradas de dados que possam levar a um consumo excessivo de memória.
        4. **Soluções Computacionais Conhecidas**: O assistente sugerirá possíveis soluções ou otimizações para melhorar a eficiência de memória do algoritmo, como técnicas de compactação, uso de estruturas de dados mais eficientes ou algoritmos que minimizem a alocação de memória.

        Formato da Resposta:

        1. **Complexidade**:
        - **Melhor Caso**: A complexidade de memória no melhor caso é **O(n log n)**. Este caso ocorre quando [condições do melhor caso].
        - **Pior Caso**: A complexidade de memória no pior caso é **O(n^2)**. Este caso ocorre quando [condições do pior caso].

        2. **Processo de Verificação**: A complexidade de memória foi determinada analisando a alocação de memória em cada etapa do algoritmo, especialmente no uso de estruturas que crescem logaritmicamente no melhor caso e quadraticamente no pior caso.

        3. **Quando se torna um problema**: Este algoritmo pode se tornar problemático com entradas superiores a 1 milhão de elementos, devido ao consumo crescente de memória no pior caso.

        4. **Soluções Computacionais**: Considerar a utilização de algoritmos que utilizem estruturas de dados mais eficientes em termos de memória, como arrays compactados, ou técnicas que evitem a duplicação de dados. Além disso, estratégias para evitar o pior caso, como [incluir técnicas], podem ser implementadas.

        Exemplo:
        ```python
        def algoritmo_exemplo(arr):
            extra_memory = [0] * len(arr)  # Aloca memória extra proporcional ao tamanho do array
            for i in range(len(arr)):
                extra_memory[i] = arr[i] * 2
            return extra_memory

        # Resposta do Assistente:

        # Complexidade:
        # - Melhor Caso: A complexidade de memória no melhor caso é O(n), que ocorre quando o array de entrada já está em um estado que não exige reestruturação ou alocação adicional de memória.
        # - Pior Caso: A complexidade de memória no pior caso é O(n^2), que ocorre quando o algoritmo precisa duplicar o array em várias etapas devido a operações intermediárias.

        # Processo de Verificação: A complexidade de memória foi determinada pela alocação de um array adicional proporcional ao tamanho do array de entrada, e pela necessidade de operações intermediárias que podem aumentar exponencialmente o uso de memória.

        # Quando se torna um problema: Esta solução se torna problemática para entradas com mais de 10 milhões de elementos, onde o uso de memória extra pode exceder os limites disponíveis.

        # Soluções Computacionais: Considerar o uso de operações in-place para reduzir a necessidade de memória extra, ou estruturas de dados que ocupem menos espaço. Para evitar o pior caso, técnicas como [incluir técnicas] podem ser utilizadas.

    """

    ferramenta = Assistente(nome=nome_agente, instrucoes=descricao_agente, eh_ferramenta=True)
    resposta = ferramenta.perguntar(
        pergunta = "Faça uma análise de complexidade de algoritmo para o método " + metodo_avaliado + " do script \nScript\n" + nome_script + ".",
        caminho_arquivo=nome_script
    )

    print(f"Resposta do assistente: {resposta}")

    ferramenta.apagar_agente()

    return resposta


