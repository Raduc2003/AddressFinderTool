from adress_finder import *
from output_potential_addresses import output_potential_addresses
from output_real_locations import output_real_locations
def main():
    # url = 'https://www.brunelcare.org.uk'  edge : many pages with numbers
    # url = 'https://mycasting.ro'  edge case: romanian address
    # url = 'https://yendis.co.uk' edge case:  just : Birmingham, UK
    # url = 'https://southamptoncruisecentre.com' many addresses

    url = 'https://www.aiwoodwork.com' 
    addresses = find_address_list(url)
    # Remove duplicates
    addresses = list(set(addresses))

    # print(addresses)
    # export potential addresses to a csv file
    output_potential_addresses(addresses,url)

    # Validate addresses
    validate_addresses = []
    for address in addresses:
        #a request per second
        # time.sleep(1)
        is_valid, details = validate_address(address)
        if is_valid:
            validate_addresses.append((address, details))


    # Output to CSV in an easy-to-read format
    output_real_locations(validate_addresses, url)
    # print(validate_addresses)

main()
