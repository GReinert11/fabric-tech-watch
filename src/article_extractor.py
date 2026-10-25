import trafilatura

def extract_article_content(url):

    downloaded = trafilatura.fetch_url(url)

    if downloaded is None:
        return None

    content = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=True
    )

    return content