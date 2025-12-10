from core.fetcher import setup_logger, run_all_fetchers
from core.cleaner import run_cleaning
from core.analyzer import run_analysis


def main() -> None:
    setup_logger()

    # 1) Collecte des données brutes
    run_all_fetchers()

    # 2) Nettoyage + fusion
    run_cleaning()

    # 3) Analyse & KPIs
    run_analysis()

if __name__ == "__main__":
    main()
