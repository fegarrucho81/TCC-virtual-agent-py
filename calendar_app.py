import os
import re
import datetime
import dateparser
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# escopo de acesso à agenda
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate_google():
    """autentica com o Calendar e retorna o serviço."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("calendar", "v3", credentials=creds)
    return service


def create_event_from_text(texto):
    """
    Cria um evento no Google Calendar a partir de uma mensagem do usuário,
    como 'marque reunião com Felipe Garrucho, João Victor e Weslley às 15h hoje'.
    """
    
    service = authenticate_google()

    # Remove barra inicial e espaços
    texto = texto.lstrip("/").strip()

    # Regex melhor para capturar data e hora
    padrao_tempo = re.search(
        r"(hoje|amanhã|depois de amanhã|(?:às\s*)?\d{1,2}(?:h\d{0,2}|:\d{2})?)",
        texto,
        re.IGNORECASE
    )

    if padrao_tempo:
        trecho_tempo = padrao_tempo.group()
        # Limpa e padroniza o formato para o dateparser
        trecho_tempo = trecho_tempo.replace("às", "").strip()
        trecho_tempo = trecho_tempo.replace("h", ":")
    else:
        trecho_tempo = texto  # fallback se não achar

    data_hora = dateparser.parse(
        trecho_tempo,
        languages=["pt"],
        settings={"RELATIVE_BASE": datetime.datetime.now()}
    )

    if not data_hora:
        raise ValueError("Não consegui entender a data e hora do evento.")

    # Garante pelo menos 30 minutos de duração
    start_time = data_hora
    end_time = start_time + datetime.timedelta(minutes=30)

    # Gera título limpo
    palavras_ignoradas = ["marque", "marcar", "reunião", "às", "as", "hoje", "amanhã"]
    titulo = " ".join([p for p in texto.split() if p.lower() not in palavras_ignoradas])
    if not titulo:
        titulo = "Reunião"

    event = {
        "summary": titulo.capitalize().strip(),
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "America/Sao_Paulo",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "America/Sao_Paulo",
        },
    }

    # Cria o evento
    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Evento criado: {event.get('htmlLink')}")
    return event.get("htmlLink")
