from ai_tools_logica import calcular_complexidade_tempo, calcular_complexidade_memoria

minhas_ferramentas = [
    {
        "type":"code_interpreter"
    },
    {
      "type": "function",
      "function": {
        "name": "calcular_complexidade_tempo",
        "description": "Utilize esta ferramenta para analisar a complexidade de algoritmos em scripts Python, com foco na avaliação do tempo de execução. A ferramenta requer o caminho do script e o nome do método a ser analisado. Ela irá medir e reportar a eficiência temporal do algoritmo, auxiliando na identificação de possíveis otimizações.",
        "parameters": {
          "type": "object",
          "properties": {
            "nome_script": {
              "type": "string",
              "description": "Por favor, forneça o nome do script em vez de usar o ID associado. O nome deve ser extraído diretamente da pergunta, por exemplo: 'script.py'."
            },
            "metodo_avaliado": {
              "type": "string",
              "description": "Nome do método que deve ser análisado. Exemplo: busca()"
            },
            "id_arquivo": {
              "type": "string",
              "description": "Id do Script associado na OpenAI. Exemplo: file-v7X0bimuK8b3R9T242gfD2iY"
            }
          },
          "required": ["nome_script", "metodo_avaliado", "id_arquivo"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calcular_complexidade_memoria",
        "description": "Utilize esta ferramenta para analisar a complexidade de memória de algoritmos em scripts Python, com foco na avaliação do consumo de memória. A ferramenta requer o caminho do script e o nome do método a ser analisado. Ela irá medir e reportar a eficiência no uso de memória do algoritmo, auxiliando na identificação de possíveis otimizações.",
        "parameters": {
          "type": "object",
          "properties": {
            "nome_script": {
              "type": "string",
              "description": "Por favor, forneça o nome do script em vez de usar o ID associado. O nome deve ser extraído diretamente da pergunta, por exemplo: 'script.py'."
            },
            "metodo_avaliado": {
              "type": "string",
              "description": "Nome do método que deve ser análisado. Exemplo: busca()"
            },
            "id_arquivo": {
              "type": "string",
              "description": "Id do Script associado na OpenAI. Exemplo: file-v7X0bimuK8b3R9T242gfD2iY"
            }
          },
          "required": ["nome_script", "metodo_avaliado", "id_arquivo"]
        }
      }
    }
]

mapa_ferramentas = {
    "calcular_complexidade_tempo": calcular_complexidade_tempo,
    "calcular_complexidade_memoria" : calcular_complexidade_memoria
}