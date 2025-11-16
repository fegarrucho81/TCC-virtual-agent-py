# Virtual Assistant

## Índice:
* [Descrição do Projeto](#descrição-do-projeto)
* [Status](#status)
* [Funcionalidades](#funcionalidades)
* [Uso](#uso)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Autores e Agradecimentos](#autores-e-agradecimentos)

---

## Descrição do Projeto:
O **Virtual Agent** é parte do TCC que consiste na criação de assistente pessoal inteligente desenvolvido em Python, que utiliza inteligência artificial para ajudar o usuário a gerenciar sua agenda, lembretes e afazeres diários. Ele funciona integrado ao Telegram, permitindo que o usuário interaja com o agente por meio de mensagens no aplicativo. O agente utiliza a API da OpenAI (via LangChain) para interpretar comandos, manter o histórico de conversas e responder de forma contextualizada, tornando a experiência mais natural e eficiente.

---

## Status:
- **Em desenvolvimento**
    - 0.0.1: Conexão com a OpenAPI via terminal de comando e lógica do arquivo main.
    - 0.0.2: Integração, envio e recebimento de mensagens via Telegram.
    - 0.0.3: Uso de Polling e tratamento de erros refinado para evitar crash da aplicação.
    - 0.0.4: Conexão com o Google Calendar API para marcar eventos na agenda do usuário.
    - 0.0.4.1: Refinamento do título do evento.
    - 0.0.4.2: Refinamento do regex, para compreender diferentes padrões de horários.
    - 0.0.5: Conexão com a OpenWeather API para ter previsões de tempo em tempo real.
    - 0.0.5.1: Refatoração do código para retornar a previsão do tempo em diferentes cidades do mundo.
    - 0.0.6: Refatoração do código seguindo boas práticas de desenvolvimento e POO.
    - 0.0.7: Integração com a GNews API para retorno de notícias relevantes sobre determinado tema.
    - 0.1.0: Versão estável de testes, pronta para deploy, com bot 100% operante no Google Agenda.
    - 0.1.1: Melhorada a mensagem de boas-vindas, e adicionado um /help para auxiliar e guiar o usuário.

---
## Tecnologias Ultilizadas:
1. Python 3.11+
2. LangChain
3. OpenAI API (Modelo de Linguagem - LLM)
4. Telegram API
5. Google Calendar API
6. OpeanWeather API
7. GNews API

## Funcionalidades:
- **Recebimento de mensagens via Telegram:** O bot recebe mensagens enviadas pelo usuário em um chat específico.
- **Respostas inteligentes:** Utiliza modelos de linguagem da OpenAI para interpretar e responder perguntas.
- **Gerenciamento de histórico de conversas:** Mantém o contexto das conversas para respostas mais precisas.
- **Criação de eventos na agenda:** Cria lembretes personalizados na agenda com um simples comando.
- **Notícias atualizadas:** Pesquisa e exibe notícias atualizadas sobre determinado tema selecionado.
- **Previsão do tempo:** Retorna o clima atual de inúmeras cidades pelo globo.
---

## Uso:
**Atenção:** Este guia é **apenas para testes locais e desenvolvedores**. Usuários finais não precisam configurar APIs nem arquivos locais.

---

## Tecnologias Utilizadas
- Python 3.11+
- LangChain
- OpenAI API
- Telegram API
- Google Calendar API
- OpenWeather API
- GNews API
- LLM (modelo de linguagem)

---

## Pré-requisitos para desenvolvimento/teste local
1. Conta e chave de API da OpenAI ([obtenha aqui](https://platform.openai.com/)).
2. Token do bot do Telegram (via BotFather).
3. ID do chat do Telegram (pode ser pessoal ou de grupo).
4. Chave da OpenWeather API. ([obtenha aqui](https://openweathermap.org/appid)).
5. Chave da GNews API. ([obtenha aqui](https://gnews.io/)).
6. Chave do Google Calendar ([obtenha aqui](https://cloud.google.com/apis))
7. Credenciais do Google Calendar (`credentials.json`).
8. Python 3.11+ instalado ([download](https://www.python.org/downloads/)).
9. Git instalado ([download](https://git-scm.com/downloads)).
10. Editor de código (VS Code recomendado) ([download](https://code.visualstudio.com/)).

---

## Passo a passo para testes locais

1. **Criar o bot no Telegram:**
   - Abra o Telegram Web ou app.
   - Procure por **BotFather** e inicie conversa.
   - Digite `/start` e depois `/newbot`.
   - Escolha um nome para o bot.
   - Escolha um username (precisa terminar com `bot`).
   - Copie o **token** que o BotFather fornecer.

2. **Criar grupo de teste (opcional):**
   - Crie um grupo no Telegram e adicione seu bot.
   - Pegue o **ID do chat** usando métodos como [@userinfobot](https://t.me/userinfobot).

3. **Obter APIs:**
   - OpenAI: [https://platform.openai.com/](https://platform.openai.com/)
   - OpenWeather: [https://openweathermap.org/api](https://openweathermap.org/api)
   - GNews: [https://gnews.io/](https://gnews.io/)
   - Google Calendar API: siga [este tutorial](https://developers.google.com/calendar/quickstart/python) para gerar `credentials.json`.

4. **Clonar o repositório e preparar ambiente:**
   ```bash
   git clone https://github.com/fegarrucho81/TCC-virtual-agent-py
   cd TCC-virtual-agent-py
   python -m venv venv
   # Ativar venv:
   # Windows: venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   pip install -r requirements.txt

5. **Configurar .env na raiz do projeto:**
   ```bash 
   ## API Keys
    OPENAI_API_KEY="sua_openai_api_key"
    OPENWEATHER_API_KEY="sua_openweather_api_key"
    GNEWS_API_KEY="sua_gnews_api_key"
    
    ## Telegram
    API_BOT_TOKEN="seu_token_bot"
    CHAT_ID="id_do_chat"

   ## Google Calendar
   (coloque seu credentials.json na raiz)

6. **Rodar o bot localmente:**
   ```bash
   python app.py
   
7. **O bot mandará sua mensagem de saudação:**
   > "Olá, sou Mia! Se precisar de ajuda para gerenciar sua agenda, lembretes ou afazeres, é só me avisar!
Digite /help para ver os comandos."

8. **Testar comandos:**
    ```bash
    /help → lista de comandos.
    /marcar [nome] [data/horário] → cria evento na agenda.
    /tempo [cidade] → previsão do tempo.
    /noticias [assunto] → 5 notícias relevantes.

---

## Este setup é apenas para desenvolvimento local e testes. Para usuários finais, o bot será hospedado na nuvem e não será necessário configurar nada manualmente.

---

## Autores e Agradecimentos:
- Felipe de Oliveira Garrucho
- João Victor Alves dos Santos
- Weslley da Costa Sebastião
