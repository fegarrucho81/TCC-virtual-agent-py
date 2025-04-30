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
template = """Você é um assistente pessoal que ajuda o usuário a gerir sua agenda de horarios, lembretes e afazeres diarios.
Você faz isso a partir do acesso atraves de tools a sua agenda.

Historico de conversa:
{history}


Entrada do usuário:
{input}"""

# Cria um modelo de prompt a partir de uma lista de mensagens
prompt = ChatPromptTemplate.from_messages([
    ("system", template), # ("system", teamplate): Define o contexto inicial do assistente.
    MessagesPlaceholder(variable_name="history"), # MessagesPlaceholder: Espaço reservado para o histórico de mensagens da conversa.
    ("human", "{input}") # ("human", "{input}"): Representa a entrada do usuário.
])

llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")

chain = prompt | llm # Encadeia o modelo de prompt com o modelo de linguagem (LLM) para criar uma cadeia de execuçãoso.

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
   
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


def iniciar_agente():
    print("Bem-vindo ao assistente de agenda!")
    while True:
        pergunta_usuario = input("Você: ")

        if pergunta_usuario.lower() in ["sair", "exit"]:
            print("Desligando...")
            break

        resposta = chain_with_history.invoke(
            {'input': pergunta_usuario},
            config= {'configurable': {'session_id': 'user123'}}
        )

        print("Assistente: ", resposta.content)


if __name__ == "__main__":
    iniciar_agente()