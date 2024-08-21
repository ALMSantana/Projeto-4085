from openai import OpenAI
from helper_modelos import MODELO_GPT
from helper_io import salvar_script
from dotenv import load_dotenv
import os

load_dotenv()

class Assistente:
    def __init__(self, nome, instrucoes):
        CHAVE_API = os.getenv("OPENAI_API_KEY")

        self.cliente = OpenAI(api_key=CHAVE_API)
        self.nome = nome
        self.instrucoes = instrucoes
        self._criar_agente()
        self.thread = None
        self.arquivo = None

    def associar_arquivo(self, caminho_arquivo):
        if self.arquivo is None:
            self.arquivo = self.cliente.files.create(
                file=open(caminho_arquivo, "rb"),
                purpose="assistants"
            )
    
    def _criar_agente(self):
        self.agente = self.cliente.beta.assistants.create(
            name=self.nome,
            instructions=self.instrucoes,
            model=MODELO_GPT,
            tools=[
                {
                    "type":"code_interpreter"
                }
            ],
            tool_resources={
                "code_interpreter":{
                    "file_ids": []
                }
            }
        )

    # Novo
    def perguntar(self, pergunta, caminho_arquivo = None):
        self._criar_thread(pergunta=pergunta, caminho_arquivo=caminho_arquivo)

        run = self.cliente.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.agente.id
        )

        if run.status == "completed":
            resposta_completa = []
            mensagens_resposta = self.cliente.beta.threads.messages.list(
                thread_id=self.thread.id
            )

            for uma_mensagem in mensagens_resposta.data[0].content:
                id_arquivo = None

                if hasattr(uma_mensagem, "text") and uma_mensagem.text:
                    resposta_completa.append(uma_mensagem.text.value)               
                    anotacoes = getattr(uma_mensagem.text, "annotations", None)
                    if anotacoes:
                        caminho_arquivo_resposta = getattr(anotacoes[0], "file_path", None)
                        if caminho_arquivo_resposta:
                            id_arquivo = getattr(caminho_arquivo_resposta, "file_id", None)
                            conteudo_binario = self.cliente.files.content(id_arquivo)

                            arquivo = salvar_script("script_adaptado.py", conteudo_binario.text)
                            resposta_completa.append(f"\n\n::Código Gerado::\n\n{arquivo}")
            
            return "".join(resposta_completa)

        else:
            print(run.status)

    def _criar_thread(self, pergunta, caminho_arquivo):
        if self.thread is None:
            self.associar_arquivo(caminho_arquivo)
            self.thread = self.cliente.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": pergunta,
                        "attachments": [
                            {
                                "file_id": self.arquivo.id,
                                "tools": [{"type": "code_interpreter"}]
                            }
                        ]
                    }
                ]
            )

    def apagar_agente(self):
        if self.agente:
            self.cliente.beta.assistants.delete(self.agente.id)
            self.agente = None
            self._apagar_thread()
            self._apagar_arquivo()
    
    def _apagar_thread(self):
        if self.thread:
            self.cliente.beta.threads.delete(self.thread.id)
            self.thread = None

    def _apagar_arquivo(self):
        if self.arquivo:
            self.cliente.files.delete(self.arquivo.id)
            self.arquivo = None
            
professor = Assistente("Analisador de Algoritmos", "Você deve analisar a qualidade dos algoritmos, sempre sendo didático e mostrando exemplos claros.")
resposta = professor.perguntar("Qual a complexidade de tempo do método alocar_exaustivo do script alocador.py", "alocador.py")
print(resposta)
professor.apagar_agente()