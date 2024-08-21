import os

def salvar_script(nome_saida, conteudo):
    """
    Salva o conteúdo de um script Python em um arquivo com o nome indicado,
    na pasta 'scripts_gerados_ia', utilizando a codificação UTF-8.

    :param nome_saida: Nome do arquivo de saída (deve incluir a extensão .py).
    :param conteudo: Conteúdo do script a ser salvo.
    """
    
    pasta_saida = "scripts_gerados_ia"
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    caminho_saida = os.path.join(pasta_saida, nome_saida)
    
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(conteudo)
    
    print(f"Script salvo em: {caminho_saida}")
