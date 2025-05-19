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
    - 0.1: Conexão com a OpenAPI via terminal de comando.
    - 0.2: Envio e recebimento de mensagens via Telegram.

---
## Tecnologias Ultilizadas:
1. Python
2. LangChain
3. OpenAI API
4. Telegram API
5. LLM

## Funcionalidades:
- **Recebimento de mensagens via Telegram:** O bot escuta mensagens enviadas pelo usuário em um chat específico.
- **Respostas inteligentes:** Utiliza modelos de linguagem da OpenAI para interpretar e responder perguntas.
- **Gerenciamento de histórico de conversas:** Mantém o contexto das conversas para respostas mais precisas.
- **Mais em breve**
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


## Autores e Agradecimentos:
- Weslley da Costa Sebastião
- Felipe de Oliveira Garrucho
- João Victor Alves dos Santos


