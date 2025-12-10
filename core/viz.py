import matplotlib.pyplot as plt
import seaborn as sns
import json
import logging
from pathlib import Path
from collections import Counter
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

FIGS_DIR = Path("figs")
REPORTS_DIR = Path("reports")
DATA_DIR = Path("data")


def load_data():
    with open(DATA_DIR / "processed" / "clean_data.json", "r") as f:
        clean_data = json.load(f)

    with open(DATA_DIR / "processed" / "ml_results.json", "r") as f:
        ml_results = json.load(f)

    with open(DATA_DIR / "raw" / "api_stats.json", "r") as f:
        api_stats = json.load(f)

    return clean_data, ml_results, api_stats


def plot_sources_volume(clean_data):
    FIGS_DIR.mkdir(exist_ok=True)

    sources_count = Counter([doc["source"] for doc in clean_data])
    sources = list(sources_count.keys())
    counts = list(sources_count.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(sources, counts, color=['#3498db', '#e74c3c', '#2ecc71'])

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.xlabel('Sources', fontsize=12, fontweight='bold')
    plt.ylabel('Nombre de documents', fontsize=12, fontweight='bold')
    plt.title('Volume de données par source API', fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "sources_bar.png", dpi=300, bbox_inches='tight')
    plt.close()

    logger.info("sources_bar.png créé")


def plot_top_keywords(clean_data):
    texts = [doc["clean_text"] for doc in clean_data if doc.get("clean_text")]
    all_words = " ".join(texts).split()

    word_counts = Counter(all_words)
    top_20 = word_counts.most_common(20)

    keywords = [w[0] for w in top_20]
    counts = [w[1] for w in top_20]

    plt.figure(figsize=(12, 8))
    bars = plt.barh(keywords[::-1], counts[::-1], color='#9b59b6')

    for i, (bar, count) in enumerate(zip(bars, counts[::-1])):
        plt.text(count + 1, bar.get_y() + bar.get_height()/2,
                str(count), va='center', fontsize=10, fontweight='bold')

    plt.xlabel('Fréquence', fontsize=12, fontweight='bold')
    plt.ylabel('Mots-clés', fontsize=12, fontweight='bold')
    plt.title('Top 20 mots-clés les plus fréquents', fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "top_keywords.png", dpi=300, bbox_inches='tight')
    plt.close()

    logger.info("top_keywords.png créé")


def plot_latency_distribution(api_stats):
    latencies = [l for l in api_stats["latencies"] if l > 0]

    if not latencies:
        latencies = [0.1]

    plt.figure(figsize=(10, 6))

    box_parts = plt.boxplot(latencies, vert=True, patch_artist=True,
                            notch=True, showmeans=True,
                            boxprops=dict(facecolor='#3498db', alpha=0.7),
                            medianprops=dict(color='red', linewidth=2),
                            meanprops=dict(marker='D', markerfacecolor='yellow', markersize=8))

    stats_text = f"Moyenne: {np.mean(latencies):.3f}s\nMédiane: {np.median(latencies):.3f}s\nMin: {np.min(latencies):.3f}s\nMax: {np.max(latencies):.3f}s"
    plt.text(1.15, np.median(latencies), stats_text,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=10)

    plt.ylabel('Latence (secondes)', fontsize=12, fontweight='bold')
    plt.title('Distribution des latences API', fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks([1], ['Tous les appels'])
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "latency_box.png", dpi=300, bbox_inches='tight')
    plt.close()

    logger.info("latency_box.png créé")


def plot_status_codes(api_stats):
    status_codes = api_stats["status_codes"]
    code_counts = Counter(status_codes)

    labels = [f"Code {code}" for code in code_counts.keys()]
    sizes = list(code_counts.values())
    colors = ['#2ecc71' if code == 200 else '#e74c3c' for code in code_counts.keys()]
    explode = [0.1 if code != 200 else 0 for code in code_counts.keys()]

    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        colors=colors, explode=explode,
                                        startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')

    plt.title('Répartition des codes de statut HTTP', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "status_codes.png", dpi=300, bbox_inches='tight')
    plt.close()

    logger.info("status_codes.png créé")


def plot_timeline_activity(clean_data):
    sources = [doc["source"] for doc in clean_data]
    source_counts = Counter(sources)

    sources_list = list(source_counts.keys())
    counts_list = list(source_counts.values())

    plt.figure(figsize=(12, 6))
    plt.plot(range(len(sources_list)), counts_list,
            marker='o', linestyle='-', color='#e67e22', linewidth=2, markersize=10)

    plt.xticks(range(len(sources_list)), sources_list)
    plt.xlabel('Sources API', fontsize=12, fontweight='bold')
    plt.ylabel('Nombre de documents', fontsize=12, fontweight='bold')
    plt.title('Volume de données par source', fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "timeline_activity.png", dpi=300, bbox_inches='tight')
    plt.close()

    logger.info("timeline_activity.png créé")


def plot_ml_clusters(ml_results):
    cluster_analysis = ml_results["cluster_analysis"]

    cluster_ids = []
    cluster_sizes = []
    cluster_labels = []

    for cluster_id, data in cluster_analysis.items():
        cluster_ids.append(int(cluster_id.split('_')[1]))
        cluster_sizes.append(data["size"])
        top_word = data["top_words"][0] if data["top_words"] else "N/A"
        cluster_labels.append(f"Cluster {cluster_id.split('_')[1]}\n({top_word})")

    colors_palette = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    bars = ax1.bar(cluster_labels, cluster_sizes, color=colors_palette[:len(cluster_ids)])
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax1.set_xlabel('Clusters', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Nombre de documents', fontsize=12, fontweight='bold')
    ax1.set_title('Distribution des documents par cluster', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')

    explode = [0.05] * len(cluster_ids)
    ax2.pie(cluster_sizes, labels=cluster_labels, autopct='%1.1f%%',
           colors=colors_palette[:len(cluster_ids)], explode=explode,
           startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax2.set_title('Répartition proportionnelle', fontsize=12, fontweight='bold')

    silhouette = ml_results.get("silhouette_score", 0)
    fig.suptitle(f'Résultats du clustering ML (Silhouette: {silhouette:.3f})',
                fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.savefig(FIGS_DIR / "ml_clusters.png", dpi=300, bbox_inches='tight')
    plt.close()

    logger.info("ml_clusters.png créé")


def create_dashboard_pdf():
    REPORTS_DIR.mkdir(exist_ok=True)

    images = [
        FIGS_DIR / "sources_bar.png",
        FIGS_DIR / "top_keywords.png",
        FIGS_DIR / "latency_box.png",
        FIGS_DIR / "status_codes.png",
        FIGS_DIR / "timeline_activity.png",
        FIGS_DIR / "ml_clusters.png"
    ]

    with PdfPages(REPORTS_DIR / "dashboard.pdf") as pdf:
        for img_path in images:
            if img_path.exists():
                fig = plt.figure(figsize=(11, 8.5))
                img = plt.imread(img_path)
                plt.imshow(img)
                plt.axis('off')
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()

    logger.info("dashboard.pdf créé")


def create_all_figures():
    logger.info("=== Début visualisations ===")

    clean_data, ml_results, api_stats = load_data()

    plot_sources_volume(clean_data)
    plot_top_keywords(clean_data)
    plot_latency_distribution(api_stats)
    plot_status_codes(api_stats)
    plot_timeline_activity(clean_data)
    plot_ml_clusters(ml_results)

    create_dashboard_pdf()

    logger.info("=== Visualisations terminées ===")


def main():
    logging.basicConfig(level=logging.INFO)
    create_all_figures()


if __name__ == "__main__":
    main()
