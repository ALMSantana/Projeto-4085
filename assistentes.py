from openai import OpenAI
from helper_modelos import MODELO_GPT
from helper_io import salvar_script
from dotenv import load_dotenv
from ai_tools_descricoes import minhas_ferramentas, mapa_ferramentas
import os
import json #novo

load_dotenv()

class Assistente:
    def __init__(self, nome, instrucoes, eh_ferramenta = False):
        CHAVE_API = os.getenv("OPENAI_API_KEY")

        self.cliente = OpenAI(api_key=CHAVE_API)
        self.nome = nome
        self.instrucoes = instrucoes
        self._criar_agente(eh_ferramenta)
        self.thread = None
        self.arquivo = None

    def associar_arquivo(self, caminho_arquivo):
        if self.arquivo is None:
            self.arquivo = self.cliente.files.create(
                file=open(caminho_arquivo, "rb"),
                purpose="assistants"
            )
    
    def _criar_agente(self, eh_ferramenta):
        ferramentas_agente = minhas_ferramentas if not eh_ferramenta else [{"type":"code_interpreter"}]

        self.agente = self.cliente.beta.assistants.create(
            name=self.nome,
            instructions=self.instrucoes,
            model=MODELO_GPT,
            tools=ferramentas_agente,
            tool_resources={
                "code_interpreter":{
                    "file_ids": []
                }
            }
        )

    def construir_resposta_completa(self, lista_mensagens):
        colecao_respostas = []
        for uma_mensagem in lista_mensagens.data[0].content:
            id_arquivo = None

            if hasattr(uma_mensagem, "text") and uma_mensagem.text:
                colecao_respostas.append(uma_mensagem.text.value)               
                anotacoes = getattr(uma_mensagem.text, "annotations", None)
                if anotacoes:
                    caminho_arquivo_resposta = getattr(anotacoes[0], "file_path", None)
                    if caminho_arquivo_resposta:
                        id_arquivo = getattr(caminho_arquivo_resposta, "file_id", None)
                        conteudo_binario = self.cliente.files.content(id_arquivo)

                        arquivo = salvar_script("script_adaptado.py", conteudo_binario.text)
                        colecao_respostas.append(f"\n\n::Código Gerado::\n\n{arquivo}")
        
        return "".join(colecao_respostas)

    def perguntar(self, pergunta, caminho_arquivo = None, continuacao_conversa = False):
        self._criar_thread(pergunta=pergunta, caminho_arquivo=caminho_arquivo)
        respostas_ferramentas = []
        resposta_completa = ""

        if continuacao_conversa and self.thread:
            self.cliente.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=pergunta
            )

        run = self.cliente.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.agente.id
        )

        print(f"Run status: {run.status}")
        
        if run.status == "requires_action":

            for tool in run.required_action.submit_tool_outputs.tool_calls:
                print(f"Tool call name: {tool.function.name}")
                argumentos = json.loads(tool.function.arguments)
                resposta_uma_ferramenta = {
                    "tool_call_id": tool.id,
                    "output" : mapa_ferramentas[tool.function.name](argumentos)
                }
                respostas_ferramentas.append(resposta_uma_ferramenta)

            if respostas_ferramentas:
                try:
                    run = self.cliente.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=self.thread.id,
                        run_id=run.id,
                        tool_outputs=respostas_ferramentas
                    )
                    print("Tool outputs submitted successfully.")
                except Exception as e:
                    print("Failed to submit tool outputs:", e)
                else:
                    print("No tool outputs to submit.")
            
        if run.status == 'completed':
            lista_mensagens = self.cliente.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            
            resposta_completa += self.construir_resposta_completa(lista_mensagens)

        else:
            print(run.status)                

        return resposta_completa

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