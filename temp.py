
# import os
# import requests
# from bs4 import BeautifulSoup
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# import string
# import re

# # Download NLTK resources (if not already downloaded)
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)
# nltk.download('wordnet', quiet=True)

# def scrape_website(url):
#     try:
#         # Fetch the HTML content from the website
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         html_content = response.content.decode('utf-8', 'ignore')  # Specify the encoding and ignore any decoding errors

#         return html_content

#     except requests.exceptions.RequestException as e:
#         print(f"Error accessing {url}: {e}")
#         return None

# def clean_text(text, dictionary, max_words=500):
#     # Remove non-ASCII characters
#     text = re.sub(r'[^\x00-\x7F]+', ' ', text)
#     # Replace known errors from dictionary
#     for error, correction in dictionary.items():
#         text = text.replace(error, correction)
#     # Tokenize the text
#     tokens = word_tokenize(text)
#     # Remove digits, punctuation, and stop words; convert to lowercase; lemmatization
#     table = str.maketrans('', '', string.punctuation)
#     tokens = [word.translate(table).lower() for word in tokens if word.isalpha() and word.lower() not in set(stopwords.words('english'))]
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(word) for word in tokens]
#     # Limit to max_words
#     tokens = tokens[:max_words]
#     # Join the tokens with space as separator
#     cleaned_text = ' '.join(tokens)

#     return cleaned_text




# def load_dictionary_from_file(file_path):
#     dictionary = {}
#     with open(file_path, 'r') as file:
#         for line in file:
#             if line.strip():  # Skip empty lines
#                 error, correction = line.strip().split(',')
#                 dictionary[error.strip()] = correction.strip()
#     return dictionary

# def scrape_category(category, url_file, dictionary_file):
#     try:
#         # Load dictionary from file
#         dictionary = load_dictionary_from_file(dictionary_file)
#         # Create directories for cleaned content
#         cleaned_content_folder = os.path.join('cleaned_content', category)
#         os.makedirs(cleaned_content_folder, exist_ok=True)
#         # Read URLs from the URL file
#         with open(url_file, 'r') as file:
#             urls = file.readlines()
#         if not urls:
#             print(f"No URLs found in {url_file}. Skipping {category} category.")
#             return
#         # Iterate through each URL
#         for idx, url in enumerate(urls, start=1):
#             url = url.strip()  # Remove leading/trailing whitespace
#             html_content = scrape_website(url)
#             if html_content:
#                 # Parse the HTML content with BeautifulSoup
#                 soup = BeautifulSoup(html_content, 'html.parser')
#                 # Extract paragraph text
#                 paragraphs = [paragraph.text.strip() for paragraph in soup.find_all('p')]
#                 # Initialize total word count
#                 total_words = 0
#                 # Initialize list to store cleaned paragraphs
#                 cleaned_paragraphs = []
#                 # Iterate through each paragraph
#                 for text in paragraphs:
#                     # Clean the text
#                     cleaned_text = clean_text(text, dictionary)
#                     # Calculate the number of words in the cleaned text
#                     words_in_text = len(cleaned_text.split())
#                     # Check if adding this paragraph exceeds the 800-word limit
#                     if total_words + words_in_text <= 500:
#                         # Add the cleaned text to the list
#                         cleaned_paragraphs.append(cleaned_text)
#                         # Update the total word count
#                         total_words += words_in_text
#                     else:
#                         # Stop processing paragraphs if the limit is reached
#                         break
#                 # Join the cleaned paragraphs
#                 cleaned_paragraphs = ' '.join(cleaned_paragraphs)
#                 # Save the cleaned text to a file
#                 cleaned_file_path = os.path.join(cleaned_content_folder, f"url{idx}.txt")
#                 with open(cleaned_file_path, 'w') as cleaned_file:
#                     cleaned_file.write(cleaned_paragraphs)
#                 print(f"Text scraped from {url} and saved to {cleaned_file_path}")
#             else:
#                 print(f"Skipping {url} due to error in fetching content")
#     except FileNotFoundError:
#         print(f"URL file {url_file} or dictionary file {dictionary_file} not found. Skipping {category} category.")


# # Scrape URLs for different categories
# scrape_category('food', 'foodurls.txt', 'dic.txt')
# scrape_category('fashion', 'fashionurls.txt', 'dic.txt')
# scrape_category('sport', 'sporturls.txt', 'dic.txt')












# import os
# import requests
# from bs4 import BeautifulSoup
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# import string
# import re

# # Download NLTK resources (if not already downloaded)
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)
# nltk.download('wordnet', quiet=True)

# def scrape_website(url):
#     try:
#         # Fetch the HTML content from the website
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         html_content = response.content.decode('utf-8', 'ignore')  # Specify the encoding and ignore any decoding errors

#         return html_content

#     except requests.exceptions.RequestException as e:
#         print(f"Error accessing {url}: {e}")
#         return None

# def clean_text(text, dictionary):
#     # Remove non-ASCII characters
#     text = re.sub(r'[^\x00-\x7F]+', ' ', text)
#     # Replace known errors from dictionary
#     for error, correction in dictionary.items():
#         text = text.replace(error, correction)
#     # Remove periods
#     text = text.replace(".", "")
#     # Tokenize the text
#     tokens = word_tokenize(text)
#     # Remove digits
#     tokens = [word for word in tokens if not word.isdigit()]
#     # Remove punctuation
#     table = str.maketrans('', '', string.punctuation)
#     tokens = [word.translate(table) for word in tokens]
#     # Convert tokens to lowercase
#     tokens = [word.lower() for word in tokens]
#     # Remove stop words
#     stop_words = set(stopwords.words('english'))
#     tokens = [word for word in tokens if word not in stop_words]
#     # Lemmatization
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(word) for word in tokens]
#     # Limit to 500 words
#     tokens = tokens[:500]
#     # Join the tokens with space as separator
#     cleaned_text = ' '.join(tokens)

#     return cleaned_text


# def load_dictionary_from_file(file_path):
#     dictionary = {}
#     with open(file_path, 'r') as file:
#         for line in file:
#             if line.strip():  # Skip empty lines
#                 error, correction = line.strip().split(',')
#                 dictionary[error.strip()] = correction.strip()
#     return dictionary

# def scrape_category(category, url_file, dictionary_file):
#     try:
#         # Load dictionary from file
#         dictionary = load_dictionary_from_file(dictionary_file)
#         # Create directories for cleaned content
#         cleaned_content_folder = os.path.join('cleaned_content', category)
#         os.makedirs(cleaned_content_folder, exist_ok=True)
#         # Read URLs from the URL file
#         with open(url_file, 'r') as file:
#             urls = file.readlines()
#         if not urls:
#             print(f"No URLs found in {url_file}. Skipping {category} category.")
#             return
#         # Iterate through each URL
#         for idx, url in enumerate(urls, start=1):
#             url = url.strip()  # Remove leading/trailing whitespace
#             html_content = scrape_website(url)
#             if html_content:
#                 # Parse the HTML content with BeautifulSoup
#                 soup = BeautifulSoup(html_content, 'html.parser')
#                 # Extract paragraph text
#                 paragraphs = [paragraph.text.strip() for paragraph in soup.find_all('p')]
#                 # Clean the text of each paragraph
#                 cleaned_paragraphs = ' '.join(clean_text(text, dictionary) for text in paragraphs)
#                 # Save the cleaned text to a file
#                 cleaned_file_path = os.path.join(cleaned_content_folder, f"url{idx}.txt")
#                 with open(cleaned_file_path, 'w') as cleaned_file:
#                     cleaned_file.write(cleaned_paragraphs)
#                 print(f"Text scraped from {url} and saved to {cleaned_file_path}")
#             else:
#                 print(f"Skipping {url} due to error in fetching content")
#     except FileNotFoundError:
#         print(f"URL file {url_file} or dictionary file {dictionary_file} not found. Skipping {category} category.")

# # Scrape URLs for different categories
# scrape_category('food', 'foodurls.txt', 'dic.txt')
# scrape_category('fashion', 'fashionurls.txt', 'dic.txt')
# scrape_category('sport', 'sporturls.txt', 'dic.txt')




# import os
# import requests
# from bs4 import BeautifulSoup
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# import string
# import re

# # Download NLTK resources (if not already downloaded)
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)
# nltk.download('wordnet', quiet=True)

# def scrape_website(url):
#     try:
#         # Fetch the HTML content from the website
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         html_content = response.content.decode('utf-8', 'ignore')  # Specify the encoding and ignore any decoding errors

#         return html_content

#     except requests.exceptions.RequestException as e:
#         print(f"Error accessing {url}: {e}")
#         return None


# def clean_text(text):
#     # Remove non-ASCII characters
#     text = re.sub(r'[^\x00-\x7F]+', ' ', text)
#     # Tokenize the text
#     tokens = word_tokenize(text)

#     # Remove punctuation except full stop
#     table = str.maketrans('', '', string.punctuation.replace('.', ''))
#     tokens = [word.translate(table) for word in tokens]

#     # Convert tokens to lowercase
#     tokens = [word.lower() for word in tokens]

#     # Remove stop words
#     stop_words = set(stopwords.words('english'))
#     tokens = [word for word in tokens if word not in stop_words]

#     # Lemmatization
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(word) for word in tokens]

#     # Join the tokens with space as separator
#     cleaned_text = ' '.join(tokens)

#     return cleaned_text


# def scrape_category(category, url_file):
#     try:
#         # Create directories for raw and cleaned content
#         raw_content_folder = os.path.join('raw_content', category)
#         cleaned_content_folder = os.path.join('cleaned_content', category)
#         os.makedirs(raw_content_folder, exist_ok=True)
#         os.makedirs(cleaned_content_folder, exist_ok=True)

#         # Read URLs from the URL file
#         with open(url_file, 'r') as file:
#             urls = file.readlines()

#         if not urls:
#             print(f"No URLs found in {url_file}. Skipping {category} category.")
#             return

#         # Iterate through each URL
#         for idx, url in enumerate(urls, start=1):
#             url = url.strip()  # Remove leading/trailing whitespace
#             html_content = scrape_website(url)

#             if html_content:
#                 # Save the raw HTML content to a file
#                 raw_file_path = os.path.join(raw_content_folder, f"url{idx}.html")
#                 with open(raw_file_path, 'w', encoding='utf-8') as raw_file:
#                     raw_file.write(html_content)

#                 # Parse the HTML content with BeautifulSoup
#                 soup = BeautifulSoup(html_content, 'html.parser')

#                 # Extract paragraph text, heading text, and link text
#                 paragraphs = [paragraph.text.strip() for paragraph in soup.find_all('p')]
#                 headings = [heading.text.strip() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
#                 links = [link.text.strip() for link in soup.find_all('a', href=True)]

#                 # Clean the text of each section
#                 cleaned_paragraphs = ' '.join(clean_text(text) for text in paragraphs)
#                 cleaned_headings = ' '.join(clean_text(text) for text in headings)
#                 cleaned_links = ' '.join(clean_text(text) for text in links)

#                 # Concatenate all cleaned text with separators
#                 cleaned_text = f"{cleaned_headings} ### {cleaned_links} ### {cleaned_paragraphs}"

#                 # Save the cleaned text to a file
#                 cleaned_file_path = os.path.join(cleaned_content_folder, f"{category}{idx}.txt")
#                 with open(cleaned_file_path, 'w') as cleaned_file:
#                     cleaned_file.write(cleaned_text)

#                 print(f"Text scraped from {url} and saved to {raw_file_path} and {cleaned_file_path}")
#             else:
#                 print(f"Skipping {url} due to error in fetching content")

#     except FileNotFoundError:
#         print(f"URL file {url_file} not found. Skipping {category} category.")


# # Scrape URLs for different categories
# scrape_category('food', 'foodurls.txt')
# scrape_category('fashion', 'fashionurls.txt')
# scrape_category('sport', 'sporturls.txt')


# import os
# import requests
# from bs4 import BeautifulSoup
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# import string
# import re

# # Download NLTK resources (if not already downloaded)
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)
# nltk.download('wordnet', quiet=True)

# def scrape_website(url):
#     try:
#         # Fetch the HTML content from the website
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         html_content = response.content.decode('utf-8', 'ignore')  # Specify the encoding and ignore any decoding errors

#         return html_content

#     except requests.exceptions.RequestException as e:
#         print(f"Error accessing {url}: {e}")
#         return None


# def clean_text(text):
#     # Remove non-ASCII characters
#     text = re.sub(r'[^\x00-\x7F]+', ' ', text)
#     # Tokenize the text
#     tokens = word_tokenize(text)

#     # Remove punctuation
#     table = str.maketrans('', '', string.punctuation)
#     tokens = [word.translate(table) for word in tokens]

#     # Convert tokens to lowercase
#     tokens = [word.lower() for word in tokens]

#     # Remove stop words
#     stop_words = set(stopwords.words('english'))
#     tokens = [word for word in tokens if word not in stop_words]

#     # Lemmatization
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(word) for word in tokens]

#     return ' '.join(tokens)


# def scrape_category(category, url_file):
#     try:
#         # Create directories for raw and cleaned content
#         raw_content_folder = os.path.join('raw_content', category)
#         cleaned_content_folder = os.path.join('cleaned_content', category)
#         os.makedirs(raw_content_folder, exist_ok=True)
#         os.makedirs(cleaned_content_folder, exist_ok=True)

#         # Read URLs from the URL file
#         with open(url_file, 'r') as file:
#             urls = file.readlines()

#         if not urls:
#             print(f"No URLs found in {url_file}. Skipping {category} category.")
#             return

#         # Iterate through each URL
#         for idx, url in enumerate(urls, start=1):
#             url = url.strip()  # Remove leading/trailing whitespace
#             html_content = scrape_website(url)

#             if html_content:
#                 # Save the raw HTML content to a file
#                 raw_file_path = os.path.join(raw_content_folder, f"url{idx}.html")
#                 with open(raw_file_path, 'w', encoding='utf-8') as raw_file:
#                     raw_file.write(html_content)

#                 # Parse the HTML content with BeautifulSoup
#                 soup = BeautifulSoup(html_content, 'html.parser')

#                 # Extract paragraph text, heading text, and span text
#                 paragraphs = [paragraph.text.strip() for paragraph in soup.find_all('p')]
#                 headings = [heading.text.strip() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
#                 # spans = []#since the span is giving unwanted content therefore not including its content.

#                 # Clean and concatenate the text of all paragraphs, headings, and spans
#                 cleaned_text = ''
#                 for text_list in [headings, paragraphs]:
#                     for text in text_list:
#                         cleaned_text += clean_text(text) + '\n'

#                 # Save the cleaned text to a file
#                 cleaned_file_path = os.path.join(cleaned_content_folder, f"{category}{idx}.txt")
#                 with open(cleaned_file_path, 'w') as cleaned_file:
#                     cleaned_file.write(cleaned_text)

#                 print(f"Text scraped from {url} and saved to {raw_file_path} and {cleaned_file_path}")
#             else:
#                 print(f"Skipping {url} due to error in fetching content")

#     except FileNotFoundError:
#         print(f"URL file {url_file} not found. Skipping {category} category.")


# # Scrape URLs for different categories
# scrape_category('food', 'foodurls.txt')
# scrape_category('fashion', 'fashionurls.txt')
# scrape_category('sport', 'sporturls.txt')
