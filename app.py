import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Importa as classes e funções necessárias do LangChain e dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Este texto define o comportamento do assistente e como ele deve interagir com o usuário.
template = """Você é um assistente pessoal que ajuda o usuário a gerir sua agenda de horários, lembretes e afazeres diários.
Você faz isso a partir do acesso através de tools a sua agenda.

Histórico de conversa:
{history}

Entrada do usuário:
{input}"""

# Cria um modelo de prompt a partir de uma lista de mensagens
prompt = ChatPromptTemplate.from_messages([
    ("system", template), # Define o contexto inicial do assistente.
    MessagesPlaceholder(variable_name="history"), # Espaço reservado para o histórico de mensagens da conversa.
    ("human", "{input}") # Representa a entrada do usuário.
])

# Inicializa o modelo de linguagem com temperatura e modelo especificados
llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")

# Encadeia o modelo de prompt com o modelo de linguagem (LLM) para criar uma cadeia de execução.
chain = prompt | llm

# Dicionário para armazenar o histórico de sessões
store = {}

# Função para obter o histórico de mensagens de uma sessão específica
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    # Se a sessão não existir no store, cria uma nova
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Cria uma cadeia de execução com histórico de mensagens
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input", # Chave para as mensagens de entrada
    history_messages_key="history" # Chave para o histórico de mensagens
)

# Função para iniciar o agente
def iniciar_agente():
    print("Bem-vindo ao assistente de agenda!")
    while True:
        pergunta_usuario = input("Você: ")

        # Verifica se o usuário deseja sair
        if pergunta_usuario.lower() in ["sair", "exit"]:
            print("Desligando...")
            break

        # Invoca a cadeia de execução com histórico de mensagens
        resposta = chain_with_history.invoke(
            {'input': pergunta_usuario},
            config={'configurable': {'session_id': 'user123'}}
        )

        # Exibe a resposta do assistente
        print("Assistente: ", resposta.content)

# Ponto de entrada do script
if __name__ == "__main__":
    iniciar_agente()
