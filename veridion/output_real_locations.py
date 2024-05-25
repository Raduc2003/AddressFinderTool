import csv

def output_real_locations(addresses, url):
    # Output to CSV in an easy-to-read format type, address,details
    with open('real_locations.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Writing headers for better clarity
        writer.writerow(["Type", "Address", "Country", "Region", "City", "Postcode","Road","Road Number", "Latitude", "Longitude"])
        
        # Writing potential addresses
        for address in addresses:
            writer.writerow(["Real Location", address[0],address[1]['country'],address[1]['region'],address[1]['city'],address[1]['postcode'],address[1]['road'],address[1]['road_number'],address[1]['latitude'],address[1]['longitude']])
        
        # Writing the URL
        writer.writerow(["URL", url])

    return

