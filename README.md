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
    - 0.0.5.1.2: Refatoração do código.
    - 0.0.6: Integração com a GNews API para retorno de notícias relevantes sobre determinado tema.
    - 0.1.0: Versão estável de testes pronta para deploy, com bot 100% operante no Google Agenda.

---
## Tecnologias Ultilizadas:
1. Python
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
Antes de rodar o projeto, no arquivo `.env`, na raiz do projeto, preencha com seus próprios dados:
- **OPENAI_API_KEY:** Chave de API da OpenAI (obtenha em https://platform.openai.com/).
- **API_BOT_TOKEN:** Token do seu bot do Telegram (obtenha com o BotFather).
- **CHAT_ID:** ID do chat onde o bot irá interagir (pode ser seu ID pessoal ou de um grupo).

### Pré-requisitos:
- Python 3.11+
- Conta e chave de API da OpenAI
- Token de bot do Telegram
- ID do chat do Telegram


## Autores e Agradecimentos:
- Felipe de Oliveira Garrucho
- João Victor Alves dos Santos
- Weslley da Costa Sebastião
