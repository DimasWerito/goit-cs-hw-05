import requests
import re
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor
from functools import reduce

def download_text(url):
    """Download text content from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading text: {e}")
        return None

def map_words(text):
    """Map phase of MapReduce: tokenize the text into words and count each word."""
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

def reduce_counts(counts_list):
    """Reduce phase of MapReduce: combine word counts from all partial results."""
    total_counts = reduce(lambda x, y: x + y, counts_list)
    return total_counts

def mapreduce_word_count(text, num_threads=4):
    """Perform MapReduce word count with multithreading."""
    words_per_thread = len(text) // num_threads
    text_chunks = [text[i:i + words_per_thread] for i in range(0, len(text), words_per_thread)]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        partial_counts = list(executor.map(map_words, text_chunks))

    total_counts = reduce_counts(partial_counts)
    return total_counts

def visualize_top_words(word_counts, top_n=10):
    """Visualize the top N words in a bar chart."""
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title(f"Top {top_n} Words by Frequency")
    plt.xticks(rotation=45)
    plt.show()

def main(url, top_n=10):
    # Download text from URL
    text = download_text(url)
    if text is None:
        return
    
    # Perform word count using MapReduce
    word_counts = mapreduce_word_count(text)
    
    # Visualize the top words
    visualize_top_words(word_counts, top_n)

if __name__ == "__main__":
    url = input("Enter the URL of the text: ")
    main(url)
