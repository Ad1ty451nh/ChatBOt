import requests
from bs4 import BeautifulSoup
import json
import re  # Import regex for cleaning

# URL of the documentation
URLS = {
    "segment": "https://segment.com/docs/?ref=nav",
    "mparticle": "https://docs.mparticle.com/",
    "lytics": "https://docs.lytics.com/",
    "zeotap": "https://docs.zeotap.com/home/en-us/"
}

def clean_text(text):
    """Clean extracted text by removing extra spaces, newlines, and irrelevant content."""
    text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a single space
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    # Remove common unwanted phrases (modify as needed)
    remove_phrases = ["Contact Support", "Privacy Policy", "Terms of Service", "© 2025"]
    for phrase in remove_phrases:
        text = text.replace(phrase, "")
    return text

def scrape_docs():
    data = {}
    
    for platform, url in URLS.items():
        print(f"Scraping {platform} docs...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        text_content = "\n".join([p.text for p in paragraphs if p.text.strip() != ""])

        # Clean extracted text
        cleaned_text = clean_text(text_content)
        
        data[platform] = cleaned_text
    
    # Save cleaned data to a file
    with open('data/documentation.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

    print("Scraping complete! Data saved in data/documentation.json")

if __name__ == '__main__':
    scrape_docs()
