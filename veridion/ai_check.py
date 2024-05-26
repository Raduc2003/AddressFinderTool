import requests
import json
import os
def list_to_string(addresses):
    addresses = ['"'+address+'"' for address in addresses]
    return '\n'.join(addresses)
def string_to_list(addresses):
    # parse a string like a list into a list
    addresses = [address for address in  addresses.replace(',','').replace('"',',').split(',') if address != '' and address != ' ' and address != '\n'  and address!= '<|end_of_turn|>']
    return addresses
    

text = ["4014 Tanglewood Trail, Chesapeake, VA 23325", "2555 or email us","5555 Tanglewood Trail, Chesapeake, VA 23325"]

def ai_check(addresses):
    addresses_string = list_to_string(addresses)
    url = "http://127.0.0.1:1337"
    url2 = "http://123123:1133"
    header = {
        "Content-Type": "application/json"
    }
    prompt = addresses_string
    context = "You are a highly intelligent assistant trained to recognize and extract complete, real-world addresses from a list of strings. Addresses may include street names, building numbers, city names, states, and postal codes. Some of the strings may not be addresses at all, and some may be partial addresses or incorrect. Your task is to identify which strings are real. format: \"address1\",\"address2\", ...\"addressN\"."
    payload = {
        "messages": [
            {
        "content": context,
        "role": "system"
            },
            
            {
            "content": prompt,
            "role": "user"
            }
        ],
        "model": "starling-7b",
        "stream": False,
        "max_tokens": 2048,
        "stop": [
            "hello"
        ],
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "temperature": 0.7,
        "top_p": 0.95
        }
    # Send the POST request to the API
    #try both urls
    try:
        response = requests.post(url=f'{url}/v1/chat/completions', headers=header, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Request failed with exception: {e}")
        try:
            response = requests.post(url=f'{url2}/v1/chat/completions', headers=header, json=payload)
        except requests.exceptions.RequestException as e:
            print(f"Request failed with exception: {e}")
            return None
    # Proceed with JSON decoding and handling
    if response.status_code == 200:
        try:
            result = response.json()

            resp = result['choices'][0]['message']['content']
        except KeyError:
            print("The expected keys were not found in the response.")
        
    else:
        print(f"Request failed with status code: {response.status_code}")
    return string_to_list(resp)

text2 =ai_check(text)
print(text2)

    