import os
import requests
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def get_news(query):
    """
    Retorna as 5 principais notícias relacionadas à busca do usuário
    """
    try:
        url = (
            "https://gnews.io/api/v4/search"
            f"?q={query}&lang=pt&country=br&max=5&apikey={GNEWS_API_KEY}"
        )

        response = requests.get(url)
        data = response.json()

        # Verifica se veio erro
        if "errors" in data:
            return f"Erro da API: {data['errors']}"

        # Verifica se 'articles' existe
        articles = data.get("articles")
        if not articles:
            return "Nenhuma notícia encontrada para essa pesquisa."

        mensagens = []
        for art in articles:
            titulo = art.get("title", "Sem título")
            link = art.get("url", "")
            fonte = art.get("source", {}).get("name", "Fonte desconhecida")

            mensagens.append(
                f"📰 *{titulo}*\n"
                f"🔗 {link}\n"
                f"📌 {fonte}\n"
            )

        return "\n".join(mensagens)

    except Exception as e:
        return f"Erro ao buscar notícias: {str(e)}"
