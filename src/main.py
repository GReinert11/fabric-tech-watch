from rss_collector import collect_articles
from newsletter import generate_newsletter
from email_sender import send_newsletter


def main():
    print("Démarrage Fabric Tech Watch")

    collect_articles()
    generate_newsletter()
    send_newsletter()

    print("Pipeline terminé")


if __name__ == "__main__":
    main()