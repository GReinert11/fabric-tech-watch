from datetime import datetime, timedelta, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from database import get_articles
from article_scoring import calculate_score
from llm_summarizer import summarize_article


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / "templates"
REPORT_DIR = BASE_DIR / "reports"


def generate_newsletter():

    # 1. Récupérer les articles stockés
    articles = get_articles()
    print(f"Articles en base : {len(articles)}")

    # 2. Filtrer les articles publiés ces 7 derniers jours
    today = datetime.now(timezone.utc).date()
    date_limit = today - timedelta(days=7)

    recent_articles = [
        article for article in articles
        if article["date"]
        and date_limit.isoformat() <= article["date"] <= today.isoformat()
    ]

    TEST_MODE = False

    if TEST_MODE and not recent_articles:
        print("Mode test : aucun article récent, utilisation des derniers articles disponibles.")
        recent_articles = articles

    # 3. Calculer le score de chaque article
    for article in recent_articles:
        article["score"] = calculate_score(article)

    # 4. Sélectionner les 5 articles les plus pertinents
    top_articles = sorted(
        recent_articles,
        key=lambda article: article["score"],
        reverse=True
    )[:5]

    # 5. Générer un résumé IA pour chaque article
    summarized_articles = []

    for article in top_articles:

        print(f"Analyse : {article['title']}")

        try:
            result = summarize_article(article)

            # L'URL est issue de notre base, pas du LLM
            result["url"] = article["url"]
            result["date"] = article["date"]

            summarized_articles.append(result)

        except Exception as error:
            print(f"Erreur sur cet article : {error}")

    print(f"Articles résumés : {len(summarized_articles)}")

    # 6. Charger le template Jinja2
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("newsletter.html")

    # 7. Générer le HTML
    html = template.render(
        articles=summarized_articles,
        generation_date=today.strftime("%d/%m/%Y")
    )

    # 8. Sauvegarder le résultat
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = REPORT_DIR / "newsletter.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"Newsletter générée : {output_path}")


if __name__ == "__main__":
    generate_newsletter()