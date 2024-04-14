import os
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import re

# Download NLTK resources (if not already downloaded)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def scrape_website(url):
    try:
        # Fetch the HTML content from the website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        html_content = response.content.decode('utf-8', 'ignore')  # Specify the encoding and ignore any decoding errors

        return html_content

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None


def clean_text(text):
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove punctuation
    table = str.maketrans('', '', string.punctuation)
    tokens = [word.translate(table) for word in tokens]

    # Convert tokens to lowercase
    tokens = [word.lower() for word in tokens]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return ' '.join(tokens)


def scrape_category(category, url_file):
    try:
        # Create directories for raw and cleaned content
        raw_content_folder = os.path.join('raw_content', category)
        cleaned_content_folder = os.path.join('cleaned_content', category)
        os.makedirs(raw_content_folder, exist_ok=True)
        os.makedirs(cleaned_content_folder, exist_ok=True)

        # Read URLs from the URL file
        with open(url_file, 'r') as file:
            urls = file.readlines()

        if not urls:
            print(f"No URLs found in {url_file}. Skipping {category} category.")
            return

        # Iterate through each URL
        for idx, url in enumerate(urls, start=1):
            url = url.strip()  # Remove leading/trailing whitespace
            html_content = scrape_website(url)

            if html_content:
                # Save the raw HTML content to a file
                raw_file_path = os.path.join(raw_content_folder, f"url{idx}.html")
                with open(raw_file_path, 'w', encoding='utf-8') as raw_file:
                    raw_file.write(html_content)

                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Extract paragraph text, heading text, and span text
                paragraphs = [paragraph.text.strip() for paragraph in soup.find_all('p')]
                headings = [heading.text.strip() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
                # spans = []#since the span is giving unwanted content therefore not including its content.

                # Clean and concatenate the text of all paragraphs, headings, and spans
                cleaned_text = ''
                for text_list in [headings, paragraphs]:
                    for text in text_list:
                        cleaned_text += clean_text(text) + '\n'

                # Save the cleaned text to a file
                cleaned_file_path = os.path.join(cleaned_content_folder, f"{category}{idx}.txt")
                with open(cleaned_file_path, 'w') as cleaned_file:
                    cleaned_file.write(cleaned_text)

                print(f"Text scraped from {url} and saved to {raw_file_path} and {cleaned_file_path}")
            else:
                print(f"Skipping {url} due to error in fetching content")

    except FileNotFoundError:
        print(f"URL file {url_file} not found. Skipping {category} category.")


# Scrape URLs for different categories
scrape_category('food', 'foodurls.txt')
scrape_category('fashion', 'fashionurls.txt')
scrape_category('sport', 'sporturls.txt')
