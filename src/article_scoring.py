KEYWORDS = {
    "warehouse": 5,
    "lakehouse": 5,
    "direct lake": 5,
    "data pipeline": 4,
    "power bi": 4,
    "pyspark": 3,
    "spark": 3,
    "sql": 3,
    "copilot": 1
}


def calculate_score(article):
    title = article["title"].lower()
    summary = article["summary"].lower()

    score = 0

    for keyword, weight in KEYWORDS.items():
        if keyword in title:
            score += weight * 2 # Multiplication par 2 --> si keyword dans le titre, plus important que dans le texte principal

        elif keyword in summary:
            score += weight

    return score