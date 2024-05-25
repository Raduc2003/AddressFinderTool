import requests
from bs4 import BeautifulSoup

def get_sitemap_urls(url):
    sitemap_locations = [
        'sitemap.xml', 'sitemap_index.xml', 'sitemap/sitemap.xml', 'sitemap/sitemap_index.xml', 
        'sitemap.xml.gz', 'sitemap_index.xml.gz', 'sitemap/sitemap.xml.gz', 'sitemap/sitemap_index.xml.gz'
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for location in sitemap_locations:
        response = requests.get(f"{url}/{location}", headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return [loc.text for loc in soup.find_all('loc')]
    
    return []

def get_homepage_urls(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return set()

    soup = BeautifulSoup(response.text, 'html.parser')
    urls = set()
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        if href.startswith('/'):
            full_url = f"{url}{href}"
        elif href.startswith(url):
            full_url = href
        elif href.startswith('http'):
            full_url = href
        else:
            continue
        
        urls.add(full_url)
    
    return urls

def get_all_pages(url):

    #  try adding hhtp or https to the url or www.
    possible_pages = set([url])
    
    # Get all pages from sitemap
    sitemap_urls = get_sitemap_urls(url)
    possible_pages.update(sitemap_urls)

    # Get all pages from homepage
    homepage_urls = get_homepage_urls(url)
    possible_pages.update(homepage_urls)

    print(f"Found {len(possible_pages)} possible pages")
    print(possible_pages)
    
    return list(possible_pages)
