import os
import re
import datetime
import dateparser
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# -------------------------------------------------------------------
# CONFIGS
# -------------------------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TIMEZONE = "America/Sao_Paulo"
TZ = pytz.timezone(TIMEZONE)


# -------------------------------------------------------------------
# AUTENTICAÇÃO
# -------------------------------------------------------------------
def authenticate_google():
    """autentica com o google agenda.
       caso token já exista, o reutiliza
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


# -------------------------------------------------------------------
# PARSER PARA DATA E HORA
# -------------------------------------------------------------------
def parse_datetime(texto_raw: str):
    """vai retornar datetime timezone-aware a partir de texto PT-BR."""
    texto = texto_raw.lower()
    now = datetime.datetime.now(TZ)

    # palavras relativas
    dia_hoje = "hoje" in texto
    dia_amanha = "amanhã" in texto or "amanha" in texto

    # regra de expressão regular para data e hora
    date_regex = re.compile(
        r"(\d{1,2}/\d{1,2}/\d{2,4}|"
        r"\d{1,2}-\d{1,2}-\d{2,4}|"
        r"\d{1,2}\s+de\s+[a-zçãéíóú]+(?:\s+de\s+\d{4})?|"
        r"\b\d{1,2}/\d{1,2}\b)",
        flags=re.IGNORECASE,
    )

    time_regex = re.compile(
        r"(\d{1,2}:\d{2}|\d{1,2}h\d{0,2}|\b\d{1,2}h\b)",
        flags=re.IGNORECASE,
    )

    date_match = date_regex.search(texto)
    time_match = time_regex.search(texto)

    data_hora = None

    # --------------------------
    # CASO TENHA DATA EXPLÍCITA
    # --------------------------
    if date_match:
        data_str = date_match.group(0).replace("-", "/")

        # caso "12/10" sem ano, assume ano atual
        if re.match(r"^\d{1,2}/\d{1,2}$", data_str):
            d, m = map(int, data_str.split("/"))
            data_str = f"{d:02d}/{m:02d}/{datetime.datetime.now().year}"

        # hora
        if time_match:
            hora_raw = time_match.group(0).lower().replace("h", ":")
            if ":" not in hora_raw:
                hora_raw += ":00"
            hora_str = hora_raw
        else:
            hora_str = "09:00"

        try:
            d, m, a = map(int, data_str.split("/"))
            h, mn = map(int, hora_str.split(":"))

            # utilizando "localize" ao invés de tzinfo (como anteriormente) para evitar bug
            data_hora = TZ.localize(datetime.datetime(a, m, d, h, mn))

            return data_hora
        except:
            pass

    # --------------------------
    # CASO SOMENTE HORA
    # --------------------------
    if time_match and not data_hora:
        hora_raw = time_match.group(0).replace("h", ":")
        if ":" not in hora_raw:
            hora_raw += ":00"

        try:
            h, mn = map(int, hora_raw.split(":"))
            candidato = now.replace(hour=h, minute=mn, second=0, microsecond=0)

            if candidato < now and dia_amanha:
                candidato += datetime.timedelta(days=1)

            data_hora = candidato
        except:
            pass

    # fallback dateparser
    if data_hora is None:
        settings = {
            "DATE_ORDER": "DMY",
            "PREFER_DATES_FROM": "future",
            "TIMEZONE": TIMEZONE,
            "RETURN_AS_TIMEZONE_AWARE": True,
            "RELATIVE_BASE": now,
        }
        data_hora = dateparser.parse(texto, languages=["pt"], settings=settings)

    if not data_hora:
        return None

    if data_hora.tzinfo is None:
        data_hora = TZ.localize(data_hora)

    if data_hora < now and not dia_hoje:
        data_hora += datetime.timedelta(days=1)

    return data_hora


# -------------------------------------------------------------------
# LÓGICA DE CRIAÇÃO DO EVENTO
# -------------------------------------------------------------------
def create_event_from_text(texto):
    """Cria um evento no google calendar com título limpo e horário correto."""
    service = authenticate_google()

    dt = parse_datetime(texto)
    if dt is None:
        raise ValueError(
            "Não consegui entender a data/hora. Tente algo como '10/12/2025 às 15h'."
        )

    # ajusta horário exatamente
    dt = dt.replace(second=0, microsecond=0)
    start_time = dt
    end_time = dt + datetime.timedelta(minutes=30)

    # ---------------------------------------------------------
    # EXTRAI O TÍTULO (apenas nome, sem datas/horas)
    # ---------------------------------------------------------
    texto_limpo = re.sub(r"[\/,.:;@#\n]", " ", texto).strip()
    palavras = texto_limpo.split()

    palavras_ignoradas = {
        "marcar", "marque", "marcação", "marcacao",
        "reunião", "reuniao", "agenda", "evento",
        "às", "as", "a", "o", "hoje", "amanhã", "amanha",
        "de", "do", "da", "para", "pro", "às",
    }

    titulo_tokens = [
        p for p in palavras
        if p.lower() not in palavras_ignoradas
        # remove datas tipo 10/12/2025 ou 10/12
        and not re.match(r"^\d{1,2}([:/-]\d{1,2}([:/-]\d{2,4})?)?$", p)
        # remove horas tipo 15h, 15h30, 15:30
        and not re.match(r"^\d{1,2}h\d{0,2}$", p)
        and not re.match(r"^\d{1,2}:\d{2}$", p)
        # remove ANO puro (2025, 2026, 24)
        and not re.match(r"^\d{2,4}$", p)
]

    titulo = " ".join(titulo_tokens).strip()
    if not titulo:
        titulo = "Evento"

    titulo = titulo.capitalize()

    # ---------------------------------------------------------
    # MONTAR EVENTO
    # ---------------------------------------------------------
    event_body = {
        "summary": titulo,
        "start": {"dateTime": start_time.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end_time.isoformat(), "timeZone": TIMEZONE},
    }

    created = service.events().insert(calendarId="primary", body=event_body).execute()

    print(f"Evento criado: {created.get('htmlLink')} — start: {start_time}")
    return created.get("htmlLink")

def listar_eventos_do_dia(texto):
    service = authenticate_google()

    # tenta parsear data usando a mesma função usada para criar eventos
    dt = parse_datetime(texto)
    if dt is None:
        return "Não consegui entender a data. Tente: 'hoje', 'amanhã' ou '29/11/2025'."

    # início do dia
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    # fim do dia
    end = dt.replace(hour=23, minute=59, second=59, microsecond=0)

    # query no calendar
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    # nenhuma reunião encontrada
    if not events:
        return f"Você não tem eventos em {dt.strftime('%d/%m/%Y')}."

    # monta resposta
    resposta = f"Eventos em {dt.strftime('%d/%m/%Y')}:\n\n"
    for ev in events:
        inicio = ev["start"].get("dateTime", ev["start"].get("date"))
        inicio_dt = dateparser.parse(inicio)
        hora_formatada = inicio_dt.strftime("%H:%M")
        resposta += f"- {ev.get('summary', 'Sem título')} às {hora_formatada}\n"

    return resposta
