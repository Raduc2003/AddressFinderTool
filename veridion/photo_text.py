import easyocr
import os
from web_scraper import get_images_from_webpage
from adress_finder import *
def extract_text_from_image(image_path):
    # Initialize the EasyOCR reader with multiple languages and enable GPU (CUDA)
    reader = easyocr.Reader(['en', 'fr', 'de', 'es', 'it', 'pt', 'nl'], gpu=True)  # Add other language codes as needed
    
    # Perform OCR on the image
    results = reader.readtext(image_path)
    
    # Extract and return text
    extracted_text = "\n".join([result[1] for result in results])
    return extracted_text

def process_images(image_folder):
    # Get a list of image files in the folder
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    texts = []
    # Process each image file
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        extracted_text = extract_text_from_image(image_path)
        texts.append(extracted_text)

        print(f"Extracted text from {image_file}:\n{extracted_text}\n")
    #delete the images
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        os.remove(image_path)
    return texts
def process_text_from_images(url,all_addresses):
    # Download images from the webpage
    image_folder = 'images'
    # get_images_from_webpage(url, download_folder=image_folder)
    #extract text from images
    texts = process_images(image_folder)
    # Process the extracted text from the images
    addresses =set([])
    for text in texts:
        # Find potential addresses in the text
        addresses_pyap = extract_address_pyap(text)
        print(addresses_pyap)
        addresses_regex = extract_address_regex(text)
        print(addresses_regex)
        addresses_regex_formatted = extract_valid_addresses(addresses_regex)
        print(addresses_regex_formatted)
        addresses = addresses_pyap + addresses_regex_formatted

        for address in addresses:
            add_address(all_addresses, address)

