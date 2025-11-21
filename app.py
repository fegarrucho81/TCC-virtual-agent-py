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

# carrega variáveis secretas do .env
load_dotenv()
API_BOT_TOKEN = os.getenv("API_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# template base do assistente para saber seu papel
template = """Você é um assistente pessoal que ajuda o usuário a gerir sua agenda de horários, lembretes e afazeres diários.
Você faz isso a partir do acesso através de tools a sua agenda.

Histórico de conversa:
{history}

Entrada do usuário:
{input}"""

# cria o modelo de prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# inicializa o modelo de linguagem
llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
chain = prompt | llm

# histórico de conversas
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
    bot.send_message(CHAT_ID, text=(
        "Olá, sou Mia!\n"
        "Se precisar de ajuda para gerenciar sua agenda, lembretes ou afazeres, é só me avisar!\n\n"
        "Digite /help para ver os comandos disponíveis."
    ))

    # --- COMANDOS ESPECIAIS ---
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_message(message.chat.id, (
            "Olá, sou Mia!\n"
            "Se precisar de ajuda para gerenciar sua agenda, lembretes ou afazeres, é só me avisar!\n\n"
            "Digite /help para ver os comandos disponíveis."
        ))

    @bot.message_handler(commands=['listar'])
    def handle_listar(message):
        try:
            user_query = message.text.replace("/listar", "").strip().lower()
            
            if not user_query:
                bot.send_message(message.chat.id, "Use assim:\n/listar hoje\n/listar amanhã\n/listar 29/11/2025")
                return
            
            from calendar_app import listar_eventos_do_dia
            resultado = listar_eventos_do_dia(user_query)
            bot.send_message(message.chat.id, resultado)
    
        except Exception as e:
            print(f"Erro no /listar: {e}")
            bot.send_message(message.chat.id, "Erro ao listar eventos.")
    
    @bot.message_handler(commands=['help'])
    def handle_help(message):
        help_text = (
            "*Comandos disponíveis:*\n\n"
            "/marcar [nome do evento] [xx/xx/xxxx] / hoje / amanhã às xxh / xx:yy - Criar lembrete na sua agenda\n"
            "/tempo [cidade] ou [cidade, país] - Previsão do tempo em qualquer lugar do mundo\n"
            "/noticias [assunto] - 5 notícias relevantes sobre o tema\n"
            "/listar [dia ou xx/xx/xxxx] - Mostrar eventos de tal dia\n"
        )
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

    # --- HANDLER DE MENSAGENS NORMAIS ---
    @bot.message_handler(content_types=['text'])
    def handle_message(message):
        try:
            pergunta_usuario = message.text.lower()
            chat_id = message.chat.id
            print("Mensagem recebida:", pergunta_usuario)

            # verifica se o usuário quer marcar algo na agenda
            if "marcar" in pergunta_usuario or "reunião" in pergunta_usuario:
                link = create_event_from_text(pergunta_usuario)
                bot.send_message(CHAT_ID, f"Reunião criada com sucesso!\n{link}")
                return # evita continuar pro chain
            
            # verifica se o usuário quer saber o clima
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
            
            # verifica se o usuário quer saber alguma notícia
            elif pergunta_usuario.startswith("/noticias"):
                parts = pergunta_usuario.split(" ", 1)
                if len(parts) == 1:
                    bot.send_message(chat_id, "Use assim: /noticias são paulo")
                    return
                
                query = parts[1]
                news_result = get_news(query)
                bot.send_message(chat_id, news_result)
                return # evita continuar pro chain

            # chat normal
            resposta = chain_with_history.invoke(
                {'input': pergunta_usuario},
                config={'configurable': {'session_id': 'user123'}}
            )
            bot.send_message(CHAT_ID, text=resposta.content)

        except Exception as e:
            print(f"Erro no handle_message: {e}")
            bot.send_message(CHAT_ID, text="Erro ao processar a mensagem, tente novamente.")

    # loop principal
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Erro no polling: {e}")
            time.sleep(5)
