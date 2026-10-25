from groq import Groq
from dotenv import load_dotenv
from database import get_articles
from article_extractor import extract_article_content
import json

# Chargement de la clé API
load_dotenv()

# Initialisation du client Groq
client = Groq()


def summarize_article(article):

    content = extract_article_content(article["url"])
    if not content:
        content = article["summary"]

    prompt = f"""
        Tu es un expert Microsoft Fabric et Data Engineering.
        Analyse l'article suivant :

        Titre : {article['title']}
        Contenu : {content[:15000]}

        Tu dois répondre UNIQUEMENT au format JSON valide.

        Utilise OBLIGATOIREMENT les noms de clés suivants,
        en anglais et sans les modifier :

        {{
            "summary": "Résumé en français de 3 à 5 phrases",
            "key_points": [
                "Nouveauté technique 1",
                "Nouveauté technique 2"
            ],
            "impact": "Impact concret pour un Data Engineer",
            "relevance_score": 8
        }}

        Règles :
        - Les valeurs doivent être rédigées en français.
        - Les noms des clés doivent rester en anglais.
        - relevance_score doit être un nombre entre 0 et 10.
        - N'invente aucune information absente de l'article.
        - Ne retourne aucun texte en dehors du JSON.
        """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un assistant spécialisé dans Microsoft Fabric."
                    "Tu dois obligatoirement répondre au format JSON valide,"
                    "sans texte supplémentaire ni balises Markdown."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=2500,
        reasoning_effort="low",
        response_format={"type":"json_object"}
    )

    print("Finish reason : ", response.choices[0].finish_reason)
    print("Tokens entrée : ", response.usage.prompt_tokens) 
    print("Tokens sortie : ", response.usage.completion_tokens)
    print("Total token : ", response.usage.total_tokens)

    choice = response.choices[0] 
    if choice.finish_reason != "stop":
        raise ValueError("Réponse LLM incomplète")
    result = json.loads(choice.message.content)
    print("champs retournés : ", result.keys())
    print(json.dumps(result,indent=2,ensure_ascii=False))

    required_fields = [
        "summary",
        "key_points",
        "impact",
        "relevance_score"
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(f"Champ manquant dans la réponse : {field}")
    result["title"] = article["title"]
    result["url"] = article["url"]
    result["date"] = article["date"]

    return result
    #return response.choices[0].message.content


# Premier test sur un seul article
if __name__ == "__main__":

    articles = get_articles()

    if articles:
        summary = summarize_article(articles[0])
        print(summary)
    else:
        print("Aucun article disponible.")