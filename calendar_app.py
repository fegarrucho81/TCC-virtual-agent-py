import os
import re
import datetime
import dateparser
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# escopo do google calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TIMEZONE = "America/Sao_Paulo"
TZ = pytz.timezone(TIMEZONE)


# -----------------------------------------
# autenticação com a API do google 
# -----------------------------------------
def authenticate_google():
    """
    Autentica com o Google Calendar usando credentials.json + token.json (InstalledAppFlow).
    Retorna o service do Google Calendar.
    """
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


# -----------------------------------------
# parser inteligente de data e hora com o padrão pt-br
# -----------------------------------------
def parse_datetime(texto_raw: str):
    """
    Retorna datetime timezone-aware (America/Sao_Paulo) a partir de texto livre em português.
    Lida com:
      - hoje, amanhã, depois de amanhã
      - 19h, 19:30, 19h30
      - 10/12/2025, 10/12, 10 de dezembro, 10 de dezembro de 2025
      - combinações: '10/12/2025 às 15h', 'amanhã às 10:30'
    Retorna None se não conseguiu parsear.
    """
    texto = texto_raw.lower()
    now = datetime.datetime.now(TZ)

    # detectores
    dia_hoje = bool(re.search(r"\bhoje\b", texto))
    dia_amanha = bool(re.search(r"\bamanh[ãa]\b", texto))
    dia_depois = bool(re.search(r"depois de amanh[ãa]|depois de amanhã", texto))

    # regex para datas explícitas (vários formatos)
    date_regex = re.compile(
        r"(\d{1,2}/\d{1,2}/\d{2,4}|"         # 10/12/2025
        r"\d{1,2}-\d{1,2}-\d{2,4}|"         # 10-12-2025
        r"\d{1,2}\s+de\s+[a-zçãéíóú]+(?:\s+de\s+\d{4})?|"  # 10 de dezembro (de 2025)
        r"\b\d{1,2}/\d{1,2}\b)",            # 10/12
        flags=re.IGNORECASE
    )

    # regex para hora
    time_regex = re.compile(r"(\d{1,2}:\d{2}|\d{1,2}h\d{0,2}|\b\d{1,2}h\b)", flags=re.IGNORECASE)

    date_match = date_regex.search(texto)
    time_match = time_regex.search(texto)

    data_hora = None
    trecho_tempo = ""

    # se encontrou data explícita, junta com hora se houver
    if date_match:
        data_str = date_match.group(0)

        # normaliza datas tipo 12-10-2025 → 12/10/2025
        data_str = data_str.replace("-", "/")

        # normaliza datas sem ano → 10/12 → 10/12/(ano atual)
        if re.match(r"^\d{1,2}/\d{1,2}$", data_str):
            dia, mes = map(int, data_str.split("/"))
            ano = datetime.datetime.now().year
            data_str = f"{dia:02d}/{mes:02d}/{ano}"

        # extrai hora
        if time_match:
            hora_raw = time_match.group(0).lower().replace("h", ":")
            if ":" not in hora_raw:
                hora_raw += ":00"
            hora_str = hora_raw
        else:
            hora_str = "09:00"   # fallback seguro

        # parse manual, sem usar dateparser
        try:
            dia, mes, ano = map(int, data_str.split("/"))
            h, m = map(int, hora_str.split(":"))
            data_hora = datetime.datetime(ano, mes, dia, h, m, tzinfo=TZ)
            return data_hora
        except:
            pass  # se der erro, deixa o dateparser tentar

    # se não encontrou data mas encontrou hora -> assume hoje (ou amanhã se especificado)
    elif time_match:
        raw_time = time_match.group(0)
        tm = raw_time.replace("h", ":").strip()
        if tm.endswith(":"):
            tm = tm + "00"
        if ":" not in tm:
            tm = f"{tm}:00"
        try:
            hora, minuto = map(int, tm.split(":")[:2])
            candidato = now.replace(hour=hora, minute=minuto, second=0, microsecond=0)

            # se já passou e usuário disse "amanhã", ajusta
            if candidato < now and dia_amanha:
                candidato = candidato + datetime.timedelta(days=1)

            # por padrão, se passou e não disse "hoje", mantemos hoje (você pode mudar para agendar amanhã)
            data_hora = candidato
            if data_hora.tzinfo is None:
                data_hora = TZ.localize(data_hora)
        except Exception:
            data_hora = None

    # se encontrou palavras relativas (hoje/amanhã/depois) mas sem hora, tenta juntar com hora se houver
    if not data_hora and not trecho_tempo:
        if dia_hoje:
            trecho_tempo = "hoje"
            if time_match:
                trecho_tempo += " " + time_match.group(0)
        elif dia_amanha:
            trecho_tempo = "amanhã"
            if time_match:
                trecho_tempo += " " + time_match.group(0)
        elif dia_depois:
            trecho_tempo = "depois de amanhã"
            if time_match:
                trecho_tempo += " " + time_match.group(0)

    # fallback: tenta pegar qualquer trecho que pareça data/hora
    if not data_hora and not trecho_tempo:
        m = re.search(r"(hoje|amanh[aã]|depois de amanh[aã]|\d{1,2}:\d{2}|\d{1,2}h\d{0,2}|\d{1,2}\s+de\s+\w+|\d{1,2}/\d{1,2}(?:/\d{2,4})?)", texto)
        if m:
            trecho_tempo = m.group(0)

    # usa dateparser se ainda não tivermos data_hora construída
    if data_hora is None:
        if not trecho_tempo:
            return None

        settings = {
            "DATE_ORDER": "DMY",
            "PREFER_DATES_FROM": "future",
            "TIMEZONE": TIMEZONE,
            "RETURN_AS_TIMEZONE_AWARE": True,
            "RELATIVE_BASE": now
        }

        try:
            # passar languages=['pt'] para ser mais confiável em pt-br
            data_hora = dateparser.parse(trecho_tempo, languages=['pt'], settings=settings)
        except Exception:
            data_hora = None

    # valida
    if not data_hora:
        return None

    # se não for timezone-aware, localiza
    if data_hora.tzinfo is None:
        data_hora = TZ.localize(data_hora)

    # se a data ficar no passado e usuário não falou "hoje", tenta avançar 1 dia
    now = datetime.datetime.now(TZ)
    if data_hora < now and not dia_hoje:
        data_hora = data_hora + datetime.timedelta(days=1)

    return data_hora


# -----------------------------------------
# criar o evento
# -----------------------------------------
def create_event_from_text(texto):
    """
    Cria um evento no Google Calendar a partir do texto do usuário.
    Retorna o link do evento ou lança ValueError em caso de parse inválido.
    """
    service = authenticate_google()

    # parse
    dt = parse_datetime(texto)
    if dt is None:
        # levantamos ValueError para o chamador tratar (ou retornamos mensagem)
        raise ValueError("Não consegui entender a data/hora. Use 'hoje às 19h' ou '10/12/2025 às 15h'.")

    # duração padrão 30 minutos
    start_time = dt
    end_time = start_time + datetime.timedelta(minutes=30)

    # gerar título limpo
    texto_limpo = re.sub(r"[\/,.:;@#\n]", " ", texto).strip()
    palavras = texto_limpo.split()
    palavras_ignoradas = {
        "marcar", "marque", "marcação", "marcar:", "marque:", "reunião", "reuniao",
        "reuniao:", "reunião:", "às", "as", "a", "o", "com", "hoje", "amanhã", "amanha",
        "depois", "de", "amanhã,", "amanha,", "às,", "as,", "às.", "as."
    }
    titulo_tokens = [p for p in palavras if p.lower() not in palavras_ignoradas and not re.match(r"^\d{1,2}[:/h-]", p)]
    titulo = " ".join(titulo_tokens).strip()
    if not titulo:
        titulo = "Reunião"

    event_body = {
        "summary": titulo.capitalize(),
        "start": {"dateTime": start_time.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end_time.isoformat(), "timeZone": TIMEZONE},
    }

    created = service.events().insert(calendarId="primary", body=event_body).execute()
    # debug print
    print(f"Evento criado: {created.get('htmlLink')} — start: {start_time.isoformat()}")
    return created.get("htmlLink")
