import os
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import re
import time

# Download NLTK resources (if not already downloaded)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def scrape_website_with_retry(url, max_retries=3, delay=2):
    retries = 0
    while retries < max_retries:
        try:
            # Fetch the HTML content from the website
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            html_content = response.content.decode('utf-8', 'ignore')  # Specify the encoding and ignore any decoding errors

            return html_content

        except requests.exceptions.RequestException as e:
            print(f"Error accessing {url}: {e}")
            retries += 1
            print(f"Retrying ({retries}/{max_retries})...")
            time.sleep(delay)
    
    print(f"Max retries ({max_retries}) exceeded. Skipping {url}")
    return None

def clean_text(text, dictionary, max_words=500):
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Replace known errors from dictionary
    for error, correction in dictionary.items():
        text = text.replace(error, correction)
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove digits, punctuation, and stop words; convert to lowercase; lemmatization
    table = str.maketrans('', '', string.punctuation)
    tokens = [word.translate(table).lower() for word in tokens if word.isalpha() and word.lower() not in set(stopwords.words('english'))]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # Limit to max_words
    tokens = tokens[:max_words]
    # Join the tokens with space as separator
    cleaned_text = ' '.join(tokens)

    return cleaned_text

def load_dictionary_from_file(file_path):
    dictionary = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                error, correction = line.strip().split(',')
                dictionary[error.strip()] = correction.strip()
    return dictionary

def scrape_category(category, url_file, dictionary_file):
    try:
        # Load dictionary from file
        dictionary = load_dictionary_from_file(dictionary_file)
        # Create directories for cleaned content
        cleaned_content_folder = os.path.join('cleaned_content', category)
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
            html_content = scrape_website_with_retry(url)
            if html_content:
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                # Extract paragraph text
                paragraphs = [paragraph.text.strip() for paragraph in soup.find_all('p')]
                # Initialize total word count
                total_words = 0
                # Initialize list to store cleaned paragraphs
                cleaned_paragraphs = []
                # Iterate through each paragraph
                for text in paragraphs:
                    # Clean the text
                    cleaned_text = clean_text(text, dictionary)
                    # Calculate the number of words in the cleaned text
                    words_in_text = len(cleaned_text.split())
                    # Check if adding this paragraph exceeds the 800-word limit
                    if total_words + words_in_text <= 500:
                        # Add the cleaned text to the list
                        cleaned_paragraphs.append(cleaned_text)
                        # Update the total word count
                        total_words += words_in_text
                    else:
                        # Stop processing paragraphs if the limit is reached
                        break
                # Join the cleaned paragraphs
                cleaned_paragraphs = ' '.join(cleaned_paragraphs)
                # Save the cleaned text to a file
                cleaned_file_path = os.path.join(cleaned_content_folder, f"url{idx}.txt")
                with open(cleaned_file_path, 'w') as cleaned_file:
                    cleaned_file.write(cleaned_paragraphs)
                print(f"Text scraped from {url} and saved to {cleaned_file_path}")
            else:
                print(f"Skipping {url} due to error in fetching content")
    except FileNotFoundError:
        print(f"URL file {url_file} or dictionary file {dictionary_file} not found. Skipping {category} category.")

# Scrape URLs for different categories
scrape_category('food', 'foodurls.txt', 'dic.txt')
scrape_category('fashion', 'fashionurls.txt', 'dic.txt')
scrape_category('sport', 'sporturls.txt', 'dic.txt')
