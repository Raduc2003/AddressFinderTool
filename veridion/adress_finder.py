import time
from web_scraper import *
from geo_valid import *
import requests
from bs4 import BeautifulSoup
import pyap
import re
import concurrent.futures
from urllib.request import urlopen





def extract_address_pyap(text):
    # Use pyap to parse addresses from the text for all supported countries
    countries = ['US', 'CA', 'GB']  # Add other supported country codes as pyap supports more in the future
    addresses = []
    max_length = 150  # Set a maximum length for addresses

    for country in countries:
        parsed_addresses = pyap.parse(text, country=country)
        for address in parsed_addresses:
            address_str = str(address)
            if len(address_str) <= max_length:
                addresses.append(address_str)
    
    return addresses

def extract_address_regex(text):
    address_patterns = [
        # USA: 123 Main St, City, ST 12345 or 12345-6789
        r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[A-Z]{2}\s\d{5}(-\d{4})?\b',
        
        # USA: 123 Main St, City, 12345
        r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s\d{5}\b',
        
        # UK: 123 High Street, London, W1A 1AA
        r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b',
        
        # Germany: Street Name 123, 12345 City
        r'\b(?:[A-Z][a-z]*\s)*\d{1,5}[-\d]*,\s\d{5}\s[\w\s]+\b',
        
        # France: 123 Rue Example, 75001 Paris
        r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Rue|Avenue|Boulevard|Place|Allée|Chemin)\b,\s\d{5}\s[\w\s]+\b',
        
        # Italy: Via Roma 123, 00100 Rome
        r'\bVia\s(?:[A-Z][a-z]*\s)*\d{1,5}[-\d]*,\s\d{5}\s[\w\s]+\b',
        
        # Spain: Calle Example 123, 28001 Madrid
        r'\bCalle\s(?:[A-Z][a-z]*\s)*\d{1,5}[-\d]*,\s\d{5}\s[\w\s]+\b',
        
        # Generic: Street Name, 12345 City
        r'\b(?:[A-Z][a-z]*\s)+,\s\d{4,6}\s[\w\s]+\b',
        
        # Generic: 123 Main St, City
        r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+\b',
        
        # Romania: Strada Splaiul Unirii nr. 80-82, Etaj 1, Bucuresti
        r'\bStrada\s(?:[A-Z][a-z]*\s)*nr\.\s\d+-\d+,\sEtaj\s\d+,\s[\w\s]+\b',
        
        # General European format: 1234 AB City
        r'\b\d{4,5}\s[A-Z]{2}\s[\w\s]+\b',
        
        # Netherlands: Street Name 123, 1234 AB City
        r'\b(?:[A-Z][a-z]*\s)*\d{1,5}[-\d]*,\s\d{4}\s[A-Z]{2}\s[\w\s]+\b',
        
        # Canada: 123 Main St, Toronto, ON M1A 1A1
        r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[A-Z]{2}\s[A-Z]\d[A-Z]\s?\d[A-Z]\d\b',
        
        # Australia: 123 Main St, Sydney, NSW 2000
        r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[A-Z]{2,3}\s\d{4}\b',
        
        # India: 123 Main Street, Locality, City, 123456
        r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[\w\s]+,\s\d{6}\b',
        
        # Germany: Koppoldstr. 1, 86551 Aichach, DE-EU
        r'\b[A-Z][a-z]*str\.\s\d{1,5}[-\d]*,\s\d{5}\s[\w\s]+,\s[A-Z]{2}-[A-Z]{2}\b',
        
        # Greece: LCG Greece, Kifisias Ave. 16, 11526 Athens, GR-EU
        r'\b[A-Z][a-z]*\s[A-Z][a-z]*,\s[A-Z][a-z]*\sAve\.\s\d{1,5}[-\d]*,\s\d{5}\s[\w\s]+,\s[A-Z]{2}-[A-Z]{2}\b',
    ]

    # Compile regex patterns for better performance
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in address_patterns]

    addresses = []
    for pattern in compiled_patterns:
        matches = pattern.findall(text)
        addresses.extend(matches)
    
    return addresses

def preprocess_text(text):
    # Normalize spaces and remove unnecessary newlines and tabs
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def extract_valid_addresses(potential_addresses):
    # Improved regex patterns for various global and European address formats
    # address_patterns = [
    #     r'\d{1,5}\s\w+\.?\s\w+\.?,?\s\w+,\s\w{2}\s\d{5}',  # US: 123 Main St, City, ST 12345
    #     r'\d{1,5}\s[\w\s]+,\s\w+,\s[A-Z]{2}\s\d{5}',  # US: 123 Main Street, Springfield, IL 62704
    #     r'\d{5}\s\w+\s\w+',  # Germany: 12345 City
    #     r'\d+\s[\w\s]+,\s[\w\s]+,\s\d+',  # Generic: 123 Main Street, City, 12345
    #     r'\d{1,5}\s[\w\s]+,\s?\w+,\s?\d{4,6},?\s?\w+',  # Generic: 123 Main Street, City, 123456 Country
    #     r'[\w\s]+,\s?\d{4,6}\s\w+',  # Generic: Street, 12345 City
    #     r'\d{1,5}\s[\w\s]+,\s\d{5}\s[\w\s]+',  # Europe: 123 Main Street, 12345 City
    #     r'\d{1,5}\s[\w\s]+,?\s?\w+,?\s?\w+\s\d{5}',  # Generic: 123 Main Street City, State 12345
    #     r'Strada\s[\w\s]+nr\.\s\d+-\d+,\sEtaj\s\d+,\s[\w\s]+',  # Romania: Strada Splaiul Unirii nr. 80-82, Etaj 1, Bucuresti
    #     r'\d{1,5}\s\w+,\s\w+,\s\w{2}\s\d{5}',  # US: 123 Elm, City, ST 12345
    #     r'\d+\s\w+\s\w+,\s\w+,\s\d+',  # Generic: 123 Main St, City, 12345
    #     r'\d{1,5}\s\w+\s\w+\s\w+,\s\w+,\s\w+\s\d+',  # Extended: 123 Main St City, State 12345
    #     r'\d{4,5}\s\w+\s\w+',  # Europe: 12345 City
    #     r'\d{1,5}\s[\w\s]+,\s?\w+,?\s\w+\s\d{4,5}',  # Europe: 123 Main Street, City 12345
    #     r'\d{1,5}\s[\w\s]+,\s?\d{4,6}\s\w+',  # Generic: 123 Main Street, 12345 City
    #     r'[\w\s]+,\s\d{4,5}\s\w+',  # Generic: Street, 12345 City
    #     r'\d{1,5}\s[\w\s]+,\s\w{2}\s\d{3,4}\s[\w\s]+',  # Canada: 123 Main St, ON K1A 0B1
    #     r'\d{1,5}\s[\w\s]+,\s\w+,\s\d{3,6}',  # Australia: 123 Main St, Sydney, 2000
    #     r'\d{1,5}\s[\w\s]+,\s\d{3,6}\s\w+',  # Generic: 123 Main Street, 12345 City
    #     r'\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[A-Z]{1,3}\s\d{1,5}',  # UK: 123 High Street, London, W1A 1AA
    #     r'\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[\w\s]+,\s[A-Z]{1,3}\s\d{1,5}',  # UK: 123 High Street, District, London, W1A 1AA
    #     r'\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[\w\s]+,\s\d{4,5}',  # India: 123 Main Street, Locality, City, 123456
    # ]
    address_patterns = [
    # USA: 123 Main St, City, ST 12345 or 12345-6789
    r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[A-Z]{2}\s\d{5}(-\d{4})?\b',
    
    # USA: 123 Main St, City, 12345
    r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s\d{5}\b',
    
    # UK: 123 High Street, London, W1A 1AA
    r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b',
    
    # Germany: Street Name 123, 12345 City
    r'\b(?:[A-Z][a-z]*\s)+\d{1,5}[-\d]*,\s\d{5}\s[\w\s]+?\b',
    
    # France: 123 Rue Example, 75001 Paris
    r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Rue|Avenue|Boulevard|Place|Allée|Chemin)\b,\s\d{5}\s[\w\s]+?\b',
    
    # Italy: Via Roma 123, 00100 Rome
    r'\bVia\s(?:[A-Z][a-z]*\s)+\d{1,5}[-\d]*,\s\d{5}\s[\w\s]+?\b',
    
    # Spain: Calle Example 123, 28001 Madrid
    r'\bCalle\s(?:[A-Z][a-z]*\s)+\d{1,5}[-\d]*,\s\d{5}\s[\w\s]+?\b',
    
    # Generic: Street Name, 12345 City
    r'\b(?:[A-Z][a-z]*\s)+,\s\d{4,6}\s[\w\s]+?\b',
    
    # Generic: 123 Main St, City
    r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+?\b',
    
    # Romania: Strada Splaiul Unirii nr. 80-82, Etaj 1, Bucuresti
    r'\bStrada\s(?:[A-Z][a-z]*\s)+nr\.\s\d+-\d+,\sEtaj\s\d+,\s[\w\s]+?\b',
    
    # General European format: 1234 AB City
    r'\b\d{4,5}\s[A-Z]{2}\s[\w\s]+?\b',
    
    # Netherlands: Street Name 123, 1234 AB City
    r'\b(?:[A-Z][a-z]*\s)+\d{1,5}[-\d]*,\s\d{4}\s[A-Z]{2}\s[\w\s]+?\b',
    
    # Canada: 123 Main St, Toronto, ON M1A 1A1
    r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[A-Z]{2}\s[A-Z]\d[A-Z]\s?\d[A-Z]\d\b',
    
    # Australia: 123 Main St, Sydney, NSW 2000
    r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[A-Z]{2,3}\s\d{4}\b',
    
    # India: 123 Main Street, Locality, City, 123456
    r'\b\d{1,5}[-\d]*\s(?:[A-Z][a-z]*\s)*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons|Cmns)\b,\s[\w\s]+,\s[\w\s]+,\s\d{6}\b',
]




    # Compile regex patterns for better performance
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in address_patterns]

    valid_addresses = []
    for address in potential_addresses:
        preprocessed_address = preprocess_text(address)
        for pattern in compiled_patterns:
            if pattern.search(preprocessed_address):
                valid_addresses.append(preprocessed_address)
                break  # Once a match is found, no need to check other patterns for this address
    
    return valid_addresses

def add_address(address_set, new_address):
    to_remove = set()
    for address in address_set:
        if new_address in address and new_address != address:
            return  # A more complete address is already present
        elif address in new_address and address != new_address:
            to_remove.add(address)  # Mark the partial address for removal
    
    address_set -= to_remove  # Remove the partial addresses
    address_set.add(new_address)  # Add the new address

def process_url(url, all_addresses):
    t1 = time.time()
    text = extract_text_from_html(url)
    addresses_pyap = extract_address_pyap(text)
    print(addresses_pyap)
    addresses_regex = extract_address_regex(text)
    print(addresses_regex)
    addresses_regex_formatted = extract_valid_addresses(addresses_regex)
    print(addresses_regex_formatted)
    addresses = addresses_pyap + addresses_regex_formatted

    for address in addresses:
        add_address(all_addresses, address)
    
    t2 = time.time()
    print(f"Time for processing {url}: {t2 - t1} seconds")

def find_address_list(url):
    all_addresses = set()
    urls = get_all_pages(url)
    t = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_url, url, all_addresses) for url in urls]

        for future in concurrent.futures.as_completed(futures):
            future.result()  # wait for all threads to complete
    
    t2 = time.time()
    print("Time for all pages:", t2 - t)
    
    return list(all_addresses)




