import requests
from bs4 import BeautifulSoup
import os
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
        # add case ends with .html or .htm
       
        
        if href.startswith('/'):
            full_url = f"{url}{href}"
        elif href.startswith(url):
            full_url = href
        elif href.startswith('http'):
            full_url = href
        elif href.startswith('www'):
            full_url = f"https://{href}"
        elif href.endswith('.html') or href.endswith('.htm'):
            full_url = f"{url}/{href}"
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

def extract_text_from_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
    except:
        return ''
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all text from the HTML
    text = soup.get_text(separator=' ')
    return text


def get_images_from_webpage(url, download_folder='images'):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all image tags
    img_tags = soup.find_all('img')
    
    # Create a folder to save the images if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Download and save each image with sequential naming
    for idx, img_tag in enumerate(img_tags, start=1):
        img_url = img_tag.get('src')
        if img_url:
            try:
                # Handle relative URLs
                if not img_url.startswith(('http://', 'https://')):
                    img_url = requests.compat.urljoin(url, img_url)
                
                # Get the image content
                img_response = requests.get(img_url)
                
                # Create the image file name
                img_name = os.path.join(download_folder, f'{idx}.jpg')
                
                # Save the image
                with open(img_name, 'wb') as img_file:
                    img_file.write(img_response.content)
                
                print(f'Successfully downloaded {img_name}')
            except Exception as e:
                print(f'Failed to download {img_url}: {e}')

