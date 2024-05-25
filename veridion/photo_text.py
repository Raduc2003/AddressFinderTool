import easyocr

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    extracted_text = "\n".join([result[1] for result in results])
    return extracted_text

# Path to your image file
image_path = 'path_to_your_image_file.jpg'

# Extract text
extracted_text = extract_text_from_image(image_path)
print(extracted_text)
