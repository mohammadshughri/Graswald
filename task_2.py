import requests
import re
from collections import Counter
from wordcloud import WordCloud
import base64
from io import BytesIO

import matplotlib.pyplot as plt
import concurrent.futures


def get_posts(n):
    # Function to get n number of posts from the API
    url = "https://jsonplaceholder.typicode.com/posts/"
    response = requests.get(url)
    return response.json()[:n]


def process_text(text):
    # Function to process the text and count the occurrences of each word
    return Counter(re.findall(r"\w+", text.lower()))


def analyze_post(post):
    # Function to analyze a single post
    title_words = process_text(post["title"])
    body_words = process_text(post["body"])
    unique_title = set(title_words.keys()) - set(body_words.keys())
    unique_body = set(body_words.keys()) - set(title_words.keys())
    common = set(title_words.keys()) & set(body_words.keys())
    all_words = title_words + body_words
    return {
        "id": post["id"],
        "unique_title": unique_title,
        "unique_body": unique_body,
        "common": common,
        "all_words": all_words,
    }


def generate_wordcloud(words):
    # Function to generate a word cloud image from the given words
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(words)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()


def generate_bar_chart(words):
    # Function to generate a bar chart from the given words
    top_words = dict(sorted(words.items(), key=lambda x: x[1], reverse=True)[:10])
    plt.figure(figsize=(10, 5))
    plt.bar(top_words.keys(), top_words.values())
    plt.title("Top 10 Words")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()


def generate_html_report(results):
    # Function to generate an HTML report from the analysis results
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Post Analysis Report</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 1200px; margin: 0 auto; }
            h1 { color: #333; text-align: center; }
            h2 { color: #444; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
            .post { background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 5px; padding: 20px; margin-bottom: 20px; }
            .word-list { columns: 3; }
            .chart-container { display: flex; justify-content: space-between; margin-top: 20px; }
            .chart { width: 48%; }
            img { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>Post Analysis Report</h1>
    """

    for result in results:
        html += f"""
        <div class="post">
            <h2>Post {result['id']}</h2>
            <h3>Unique words in title:</h3>
            <div class="word-list">{', '.join(result['unique_title'])}</div>
            <h3>Unique words in body:</h3>
            <div class="word-list">{', '.join(result['unique_body'])}</div>
            <h3>Common words:</h3>
            <div class="word-list">{', '.join(result['common'])}</div>
            <div class="chart-container">
                <div class="chart">
                    <h3>Word Cloud</h3>
                    <img src='data:image/png;base64,{generate_wordcloud(result['all_words'])}' alt='Word Cloud'>
                </div>
                <div class="chart">
                    <h3>Top 10 Words</h3>
                    <img src='data:image/png;base64,{generate_bar_chart(result['all_words'])}' alt='Bar Chart'>
                </div>
            </div>
        </div>
        """

    html += """
    </body>
    </html>
    """

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)


def main(n):
    # Main function to analyze the posts and generate the HTML report
    posts = get_posts(n)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(analyze_post, posts))
    generate_html_report(results)


if __name__ == "__main__":
    main(5)  # Change this number to analyze a different number of posts
