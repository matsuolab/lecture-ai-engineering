import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import chardet
import time

visited_urls = set()
processed_texts = set()
max_depth = 5  # Set a maximum depth for recursion

def clean_text(text):
    # Remove links
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    
    # Replace special characters with a space
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def is_informative(text):
    common_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i'}
    words = text.split()
    
    # Check minimum length
    if len(words) < 50:
        return False
    
    # Check for common words
    common_word_count = sum(1 for word in words if word in common_words)
    if common_word_count < 5:
        return False
    
    return True

def extract_main_content(soup):
    # Find the main content div
    main_content = soup.find('div', id='main')
    if not main_content:
        return ""

    # Remove non-content elements by class
    for non_content_class in ['boxContact02', 'contact', 'footer', 'nav', 'sidebar']:
        for element in main_content.find_all(class_=non_content_class):
            element.decompose()

    # Extract text from specific content-related tags within the main content
    texts = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'article', 'section'])
    visible_texts = [t.get_text(separator=' ', strip=True) for t in texts]
    text = ' '.join(visible_texts)
    return text

def is_valid_link(link_url, base_url):
    # Check if the link is valid and should be processed
    parsed_link = urlparse(link_url)
    if parsed_link.netloc and parsed_link.netloc != urlparse(base_url).netloc:
        return False  # Skip external links
    
    if not parsed_link.scheme.startswith('http'):
        return False  # Skip non-http links
    
    # Allow links with no extension or with .html extension
    if '.' not in parsed_link.path.split('/')[-1] or parsed_link.path.lower().endswith('.html'):
        return True
    
    return False

def get_all_text_from_url(url, file, depth=0):
    if url in visited_urls or depth > max_depth:
        return
    visited_urls.add(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Detect encoding
        encoding = chardet.detect(response.content)['encoding']
        if encoding is None:
            encoding = 'utf-8'  # Default to 'utf-8' if encoding detection fails

        try:
            decoded_content = response.content.decode(encoding)
        except UnicodeDecodeError:
            # Fallback to ISO-8859-1 if UTF-8 decoding fails
            decoded_content = response.content.decode('ISO-8859-1')

        soup = BeautifulSoup(decoded_content, 'html.parser')

        # Extract and clean text from the current page
        text = extract_main_content(soup)
        cleaned_text = clean_text(text)
        
        if cleaned_text not in processed_texts and is_informative(cleaned_text):
            file.write(cleaned_text + "\n")
            processed_texts.add(cleaned_text)
            # Print status message
            print(f"Successfully saved text from {url}")

        # Find all links on the current page
        links = soup.find_all('a', href=True)

        # Filter and get full URLs of the links
        for link in links:
            link_url = urljoin(url, link['href'])
            if is_valid_link(link_url, url):
                get_all_text_from_url(link_url, file, depth + 1)

        time.sleep(1)  # To be polite and avoid getting banned
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")

def save_text_from_website(starting_url, filename="text.txt"):
    # Clear the file by opening it in write mode
    with open(filename, "w", encoding="utf-8") as file:
        file.write("")  # Optional: Explicitly write an empty string to clear the file

    # Reopen the file in append mode to start writing
    with open(filename, "a", encoding="utf-8") as file:
        get_all_text_from_url(starting_url, file)

# Replace with the URL of the English version of the website you want to scrape
starting_url = 'https://www.titech.ac.jp/english'
save_text_from_website(starting_url)

print("Text from website saved successfully.")