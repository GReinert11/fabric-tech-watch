from database import get_articles
from article_scoring import calculate_score

articles = get_articles()

for article in articles:
    article["score"] = calculate_score(article)

articles_sorted = sorted(
    articles,
    key=lambda article: article["score"],
    reverse=True
)

for article in articles_sorted[:10]:
    print(f"Score : {article['score']}")
    print(f"Titre : {article['title']}")
    print(f"Date : {article['date']}")
    print("-" * 50)