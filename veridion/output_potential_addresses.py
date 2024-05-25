import csv

def output_potential_addresses(addresses, url):
    # Output to CSV in an easy-to-read format
    with open('potential_addresses.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Writing headers for better clarity
        writer.writerow(["Type", "Address"])
        
        # Writing potential addresses
        for address in addresses:
            writer.writerow(["Potential Address", address])
        
        # Writing the URL
        writer.writerow(["URL", url])

    return

