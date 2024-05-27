import csv

def output_potential_addresses(addresses, url, filename='addresses.csv'):
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Writing potential addresses
        for address in addresses:
            writer.writerow(["Potential Address", address, url])

