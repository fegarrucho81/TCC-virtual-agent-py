import os
import time
from dotenv import load_dotenv
from calendar_app import create_event_from_text  
from weather import get_weather
from news import get_news

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import telebot

# Carrega variáveis do .env
load_dotenv()
API_BOT_TOKEN = os.getenv("API_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Template base do assistente
template = """Você é um assistente pessoal que ajuda o usuário a gerir sua agenda de horários, lembretes e afazeres diários.
Você faz isso a partir do acesso através de tools a sua agenda.

Histórico de conversa:
{history}

Entrada do usuário:
{input}"""

# Cria o modelo de prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Inicializa o modelo de linguagem
llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
chain = prompt | llm

# Histórico de conversas
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

# --- BOT PRINCIPAL ---
if __name__ == "__main__":
    print("SYSTEM_VERIFY: EXECUTANDO")
    bot = telebot.TeleBot(API_BOT_TOKEN)
    print("SYSTEM_VERIFY: CONECTADO NO TELEGRAM")
    bot.send_message(CHAT_ID, text="PARA MANDAR MENSAGENS PARA O AGENTE ADICIONE / ANTES DA MENSAGEM")

    # Novo bloco que substitui o antigo:
    @bot.message_handler(content_types=['text'])
    def handle_message(message):
        try:
            pergunta_usuario = message.text.lower()
            chat_id = message.chat.id
            print("Mensagem recebida:", pergunta_usuario)

            # Verifica se o usuário quer marcar algo na agenda
            if "marcar" in pergunta_usuario or "reunião" in pergunta_usuario:
                link = create_event_from_text(pergunta_usuario)
                bot.send_message(CHAT_ID, f"Reunião criada com sucesso!\n{link}")
                return # evita continuar pro chain
            
            # Verifica se o usuário quer saber o clima
            elif "tempo" in pergunta_usuario.lower() or "clima" in pergunta_usuario.lower():
                # Tenta extrair o nome da cidade
                parts = pergunta_usuario.split()
                if len(parts) > 1:
                    city = " ".join(parts[1:])
                    weather_info = get_weather(city)
                    bot.send_message(chat_id, weather_info)
                else:
                    bot.send_message(chat_id, "Por favor, diga o nome da cidade. Exemplo: '/clima São Paulo'")
                return # evita continuar pro chain
            
            elif pergunta_usuario.startswith("/noticias"):
                parts = pergunta_usuario.split(" ", 1)
                if len(parts) == 1:
                    bot.send_message(chat_id, "Use assim: /noticias são paulo")
                    return
                
                query = parts[1]
                news_result = get_news(query)
                bot.send_message(chat_id, news_result)
                return # evita continuar pro chain

            # Chat normal
            resposta = chain_with_history.invoke(
                {'input': pergunta_usuario},
                config={'configurable': {'session_id': 'user123'}}
            )
            bot.send_message(CHAT_ID, text=resposta.content)

        except Exception as e:
            print(f"Erro no handle_message: {e}")
            bot.send_message(CHAT_ID, text="Erro ao processar a mensagem, tente novamente.")

    # Loop principal
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Erro no polling: {e}")
            time.sleep(5)
