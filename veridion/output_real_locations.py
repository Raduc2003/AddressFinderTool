import csv

def output_real_locations(real_locations, url, filename='real_addresses.csv'):
   
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Writing validated addresses
        for address, details in real_locations:
            writer.writerow([
                "Real Address", 
                address, 
                details.get('country', ''), 
                details.get('region', ''), 
                details.get('city', ''), 
                details.get('postcode', ''), 
                details.get('road', ''), 
                details.get('road_number', ''), 
                details.get('latitude', ''), 
                details.get('longitude', ''),
                url
            ])
