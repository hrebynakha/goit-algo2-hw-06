"""
Напишіть Python-скрипт, який завантажує текст із заданої URL-адреси,
аналізує частоту використання слів у тексті
за допомогою парадигми MapReduce і візуалізує
топ-слова з найвищою частотою використання у тексті.
"""

from collections import defaultdict
import argparse
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Get top words from URL")
parser.add_argument(
    "--url",
    default="https://goit.global/ua/",
    type=str,
    required=False,
    help="URL of the page to analyze",
)
args = parser.parse_args()


def map_function(text):
    """Map function"""
    words = text.split()
    return [(word, 1) for word in words]


def shuffle_function(mapped_values):
    """Shuffle function"""
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(shuffled_values):
    """Reduce function"""
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced


def map_reduce(text):
    """MapReduce function"""
    mapped_values = map_function(text)
    shuffled_values = shuffle_function(mapped_values)
    reduced_values = reduce_function(shuffled_values)

    return reduced_values


def visualize_top_words(words, top_n: int = 15):
    """Visualize top words"""
    if not words:
        raise ValueError("Words dictionary is empty")
    sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
    data_values = [word[1] for word in sorted_words[:top_n]]
    names = [word[0] for word in sorted_words[:top_n]]
    _, ax = plt.subplots()
    ax.barh(names, data_values)
    ax.set_xlabel("Count")
    ax.set_ylabel("Words")
    ax.set_title(f"Top {top_n} words on the {args.url}")
    ax.invert_yaxis()
    for bar_ in ax.patches:
        width = bar_.get_width()
        ax.text(
            width + 0.5,
            bar_.get_y() + bar_.get_height() / 2,
            f"{int(width)}",
            va="center",
            fontsize=9,
            color="black",
        )

    plt.tight_layout()
    plt.show()


def get_words_count(url: str) -> dict | None:
    """Get top words from URL"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
    except requests.exceptions.RequestException:
        return None

    return map_reduce(text)


def test_visualize_top_words():
    """Test visualize top words"""
    words = get_words_count("http://localhost:9999/")
    assert words is None
    try:
        visualize_top_words(words)
    except ValueError as e:
        assert str(e) == "Words dictionary is empty"


def main():
    """Main function"""
    test_visualize_top_words()
    words = get_words_count(args.url)
    visualize_top_words(words, 25)


if __name__ == "__main__":
    main()
