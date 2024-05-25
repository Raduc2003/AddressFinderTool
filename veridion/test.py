import requests
from bs4 import BeautifulSoup
import pyap
import re

def extract_text_from_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check if the request was successful
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all text from the HTML
    text = soup.get_text(separator=' ')
    return text

def extract_address_pyap(text):
    # Use pyap to parse addresses from the text for all supported countries
    countries = countries = ['US', 'CA', 'GB']  # Add other supported country codes as pyap supports more in the future
    addresses = []
    for country in countries:
        addresses += pyap.parse(text, country=country)
    
    # Convert pyap address objects to strings
    addresses = [str(address) for address in addresses]
    
    return addresses

def extract_address_regex(text):
    # Enhanced regex patterns for various address formats, including Romanian format
    address_patterns = [
        r'\d{1,5}\s\w+\.?\s\w+\.?,?\s\w+,\s\w{2}\s\d{5}',  # US address format (e.g., 123 Main St, City, ST 12345)
        r'\d{1,5}\s[\w\s]+,\s\w+,\s[A-Z]{2}\s\d{5}',  # Another US address format (e.g., 123 Main Street, Springfield, IL 62704)
        r'\d{5}\s\w+\s\w+',  # German address format (e.g., 12345 City)
        r'\d+\s[\w\s]+,\s[\w\s]+,\s\d+',  # Generic pattern (e.g., 123 Main Street, City, 12345)
        r'\d{1,5}\s[\w\s]+,\s?\w+,\s?\d{4,6},?\s?\w+',  # Another generic pattern
        r'[\w\s]+,\s?\d{4,6}\s\w+',  # Address with postal code in the middle
        r'\d{1,5}\s[\w\s]+,\s\d{5}\s[\w\s]+',  # Address with postal code before city (common in Europe)
        r'\d{1,5}\s[\w\s]+,?\s?\w+,?\s?\w+\s\d{5}',  # Generic pattern (e.g., 1610 Chiefs Way Wayne, NE 68787)
        r'Strada\s[\w\s]+nr\.\s\d+-\d+,\sEtaj\s\d+,\s[\w\s]+',  # Romanian address format (e.g., Strada Splaiul Unirii nr. 80-82, Etaj 1, Bucuresti)
        r'\d{1,5}\s\w+,\s\w+,\s\w{2}\s\d{5}',  # Additional US format (e.g., 123 Elm, City, ST 12345)
        r'\d+\s\w+\s\w+,\s\w+,\s\d+',  # Another generic format (e.g., 123 Main St, City, 12345)
        r'\d{1,5}\s\w+\s\w+\s\w+,\s\w+,\s\w+\s\d+',  # Extended generic pattern
        r'\d{4,5}\s\w+\s\w+',  # European postal code followed by city
        r'\d{1,5}\s[\w\s]+,\s?\w+,?\s\w+\s\d{4,5}',  # Another European format
        r'\d{1,5}\s[\w\s]+,\s?\d{4,6}\s\w+',  # Address with city and postal code at the end
        r'[\w\s]+,\s\d{4,5}\s\w+',  # Address with city first followed by postal code
    ]
    
    addresses = []
    for pattern in address_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            addresses.append(match)
    
    return addresses

def extract_addresses(text):
    # Extract addresses using pyap
    addresses_pyap = extract_address_pyap(text)
    
    # Extract addresses using regex
    addresses_regex = extract_address_regex(text)
    
    # Combine both results and remove duplicates
    addresses = list(set(addresses_pyap + addresses_regex))
    
    return addresses


