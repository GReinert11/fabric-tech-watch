import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from database import init_database, insert_articles


url = "https://blog.fabric.microsoft.com/en-gb/blog/feed/"
feed = feedparser.parse(url)

articles = []

# Récupérer que les 7 derniers jours 
date_limit = datetime.now(timezone.utc) - timedelta(days=7)


for article in feed.entries:

    # Nettoyage du résumé HTML
    summary_html = article.get("summary", "")
    soup = BeautifulSoup(summary_html, "html.parser")
    summary_clean = soup.get_text(separator=" ", strip=True)

    # Conversion de la date
    date_raw = article.get("published") or article.get("updated")

    if not date_raw:
        continue

    try:
        date_article = parsedate_to_datetime(date_raw)
    except (TypeError, ValueError, IndexError):
        continue

    if date_article.tzinfo is None:
        date_article = date_article.replace(tzinfo=timezone.utc)

    # Filtre sur les 7 derniers jours
    if not date_limit <= date_article <= datetime.now(timezone.utc):
        continue

    article_dict = {
        "title": article.get("title", "Titre inconnu"),
        "date": date_article.strftime("%Y-%m-%d"),
        "url": article.get("link", ""),
        "summary": summary_clean
    }

    articles.append(article_dict)

print(f"Nombre d'articles récents : {len(articles)}")

for article in articles:
    print(article["date"], "-", article["title"])



# Initialisation du stockage
init_database()

# Sauvegarde des articles
insert_articles(articles)

print("Articles enregistrés dans SQLite.")