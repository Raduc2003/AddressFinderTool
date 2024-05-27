from adress_finder import *
from photo_text import *
from ai_check import *
import pandas as pd
from output_potential_addresses import output_potential_addresses
from output_real_locations import output_real_locations
def main(url, real=False, photo=False, ai_chk=False):
    addresses = find_address_list(url)
    addresses = list(set(addresses))  # Remove duplicates

    # Export potential addresses to a CSV file
    output_potential_addresses(addresses, url)

    if real:
        if ai_chk:
            # Use AI to check the addresses
            addresses = ai_check(addresses)
            print("AI check done", addresses)
        
        # Validate addresses
        validate_addresses = []
        for address in addresses:
            is_valid, details = validate_address(address)
            if is_valid:
                validate_addresses.append((address, details))
        
        # Output real locations to a CSV file
        output_real_locations(validate_addresses, url)

    if photo:
        process_text_from_images(url, addresses)
        output_potential_addresses(addresses, url)


# get websites from file
def get_websites_from_file(parquet_file_path):
   
    try:
        # Read the parquet file into a DataFrame
        df = pd.read_parquet(parquet_file_path)
        
        # Ensure there is a column named 'url'
        if 'domain' not in df.columns:
            raise ValueError("The Parquet file does not contain a 'url' column.")
        
        # Extract the 'url' column and convert it to a list
        urls =[ 'https://www.'+domain for domain in df['domain'].tolist()]
        
        return urls
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
# urls = get_websites_from_file('veridion/data.snappy.parquet')
urls =['https://www.andersrice.com']
def process_all_websites(urls):
    for url in urls[:500]:
        print(f"Processing {url}","index",urls.index(url))
        main(url)
    return
# print("Starting Address checking tool...")
# main()
process_all_websites(urls)