#array string to real array
def to_Array(array):
    array = array.replace("[", "")
    array = array.replace("]", "")
    array = array.replace(" ", "")
    array = array.split(",")
    return array
a= to_Array("['2024 to receive', 'And France 24th May 2026 7 nights View Details Enquire Now MSC', 'Hurtigruten20Ex', 're looking to cruise from Southampton in 2024, 2025 or 2026', '2026 2 nights View Details Enquire Now MSC', 'and Cruises from Southampton Cruise Centre, BANK HOLID', '2024 17 nights View Details Enquire Now MSC', 'Riverside20Lu', '2024 5 nights View Details Enquire Now MSC', '2024 to 30th', '2025 13 nights View Details Enquire Now MSC', 'Five Nights 24th May 2025 5 nights View Details Enquire Now MSC', 'And Portugal 2nd May 2026 7 nights View Details Enquire Now MSC', 'and the vibrant Pacific shores of California', '2024 15 nights View Details Enquire Now MSC', '2025 9 nights View Details Enquire Now MSC', '2024 to 28', '2024 to 5th', '2024 on selected', '2024 19 nights View Details Enquire Now MSC', '2023 we launched', '2025 33 nights View Details Enquire Now MSC', '2025 7 nights View Details Enquire Now MSC', '2025 12 nights View Details Enquire Now MSC', '2024 18 nights View Details Enquire Now MSC', 'TEN PHILIPSBURG, ST. THOMAS USVI', 'Five Nights 23rd May 2026 5 nights View Details Enquire Now MSC', '298 Highfield Road, Blackpool, Lancashire, FY4 3JU', '2026 13 nights View Details Enquire Now MSC', '2 8DD. The Travel Village Group is a member of AB', 'Warwick Technology Park, Gallows Hill, Warwick, CV34 6DA', '2025 11 nights View Details Enquire Now MSC', '2023 at 8pm', '2025 15 nights View Details Enquire Now MSC', '2026 22 nights View Details Enquire Now MSC', '2026 21 nights View Details Enquire Now MSC', '2025 to 12', '2026 14 nights View Details Enquire Now MSC', 'Eastern Docks, Southampton, SO14 3QN', '2021 to destinations', 'Solent Road, Western Docks, Southampton, SO15 1AJ', '414 per person price is based on MSC', 'and 19th August 2025 10 nights View Details Enquire Now MSC', '2025 4 nights View Details Enquire Now MSC', '2026 12 nights View Details Enquire Now MSC', '2024 to 15', '2024 to 07', 'and 15th June 2024 12 nights View Details Enquire Now MSC', '2024 10 nights View Details Enquire Now MSC', '2024 at 8pm', 'and 29th June 2024 14 nights View Details Enquire Now MS', '2025 to 10th', '2010 US Coast', '2025 to 06', 'Jebsen House, Ruislip, Middx, HA4 7BD', '2025 35 nights View Details Enquire Now MSC', '2025 we have', '2024 to 31st', '2024 28 nights View Details Enquire Now MSC', '1873 as the', '1914 by 80', '62 Wolverhampton Street, Walsall WS2 8DD', '2024 to take', '16 Nights 11th July 2025 16 nights View Details Enquire Now MSC', '2024 4 nights View Details Enquire Now MSC', '2025 17 nights View Details Enquire Now MS', '2024 13 nights View Details Enquire Now MSC', 'and 3rd January 2025 41 nights View Details Enquire Now MSC', '2024 to 12', '2024 to 21st', '2024 3 nights View Details Enquire Now MSC', 'and 26th September 2024 7 nights View Details Enquire Now MSC', '2024 21 nights View Details Enquire Now MSC', '2024 14 nights View Details Enquire Now MSC', '1989 by Swedish', '39 Test Road, Eastern Docks, Southampton, SO14 3GG', '2022 on Channel', '2026 On A', '2025 29 nights View Details Enquire Now MSC', 'and France 18th April 2025 7 nights View Details Enquire Now MS', '2025 28 nights View Details Enquire Now MSC', '2025 21 nights View Details Enquire Now MSC', '1959 in Blackpool', '2024 to 4', 'cunard175ny', '2024 on sailings', '2026 10 nights View Details Enquire Now MSC', 'and guests citizenship is other than US, CA', '2025 14 nights View Details Enquire Now MSC', '2022 in certain', '2024 or 2025', '2024 9 nights View Details Enquire Now MS', 'Herbert Walker Avenue, Western Docks, Southampton, SO15 1HJ', 'Logo20Na', '2024 on applicable', '2024 to 06', '2026 19 nights View Details Enquire Now MSC', '2024 11 nights View Details Enquire Now MSC', '2024 on an', 'and May 31, 2024 on select', '2024 8 nights View Details Enquire Now MSC']")
b= to_Array("['and 15th June 2024 12 nights View Details Enquire Now MSC', '298 Highfield Road, Blackpool, Lancashire, FY4 3JU', '2024 4 nights View Details Enquire Now MSC', '2025 to 10th', '2021 to destinations', 'and the vibrant Pacific shores of California', '2024 8 nights View Details Enquire Now MSC', '2024 15 nights View Details Enquire Now MSC', '2024 10 nights View Details Enquire Now MSC', '2024 19 nights View Details Enquire Now MSC', '2024 to 21st', 'and 3rd January 2025 41 nights View Details Enquire Now MSC', 'Eastern Docks, Southampton, SO14 3QN', '2022 in certain', '1959 in Blackpool', '2025 to 06', 'and France 18th April 2025 7 nights View Details Enquire Now MS', '2024 to 4', '2024 to receive', 'and 26th September 2024 7 nights View Details Enquire Now MSC', '2024 5 nights View Details Enquire Now MSC', '2026 22 nights View Details Enquire Now MSC', '2024 to 5th', '2024 18 nights View Details Enquire Now MSC', '2025 11 nights View Details Enquire Now MSC', '2023 we launched', '2024 to 30th', '2024 to 06', '2026 14 nights View Details Enquire Now MSC', '2024 21 nights View Details Enquire Now MSC', 'and 19th August 2025 10 nights View Details Enquire Now MSC', '2026 10 nights View Details Enquire Now MSC', 'TEN PHILIPSBURG, ST. THOMAS USVI', 'and Cruises from Southampton Cruise Centre, BANK HOLID', '2024 13 nights View Details Enquire Now MSC', '2024 to 31st', '2025 33 nights View Details Enquire Now MSC', '2024 to take', '1989 by Swedish', '2025 12 nights View Details Enquire Now MSC', 'and guests citizenship is other than US, CA', '2 8DD. The Travel Village Group is a member of AB', '39 Test Road, Eastern Docks, Southampton, SO14 3GG', '2024 14 nights View Details Enquire Now MSC', 'Solent Road, Western Docks, Southampton, SO15 1AJ', '2024 17 nights View Details Enquire Now MSC', '2024 28 nights View Details Enquire Now MSC', 'and 29th June 2024 14 nights View Details Enquire Now MS', '2022 on Channel', '2026 12 nights View Details Enquire Now MSC', 'And Portugal 2nd May 2026 7 nights View Details Enquire Now MSC', '2026 On A', '2025 13 nights View Details Enquire Now MSC', '2024 or 2025', '62 Wolverhampton Street, Walsall WS2 8DD', '2023 at 8pm', '2025 9 nights View Details Enquire Now MSC', '2024 11 nights View Details Enquire Now MSC', '2024 9 nights View Details Enquire Now MS', '2025 we have', 'And France 24th May 2026 7 nights View Details Enquire Now MSC', '2025 to 12', '2024 to 07', '2024 to 12', '2025 35 nights View Details Enquire Now MSC', '2025 28 nights View Details Enquire Now MSC', '2024 on an', 'Logo20Na', '2025 17 nights View Details Enquire Now MS', '2025 7 nights View Details Enquire Now MSC', '2024 on applicable', 'cunard175ny', '2010 US Coast', '2024 on selected', '2025 15 nights View Details Enquire Now MSC', '2026 19 nights View Details Enquire Now MSC', '2024 to 28', '2025 14 nights View Details Enquire Now MSC', '2025 21 nights View Details Enquire Now MSC', 'Five Nights 23rd May 2026 5 nights View Details Enquire Now MSC', 'Herbert Walker Avenue, Western Docks, Southampton, SO15 1HJ', 'and May 31, 2024 on select', 'Hurtigruten20Ex', '16 Nights 11th July 2025 16 nights View Details Enquire Now MSC', '2026 21 nights View Details Enquire Now MSC', 'Riverside20Lu', '2024 at 8pm', '2026 13 nights View Details Enquire Now MSC', '2024 on sailings', '2024 3 nights View Details Enquire Now MSC', 'Five Nights 24th May 2025 5 nights View Details Enquire Now MSC', 're looking to cruise from Southampton in 2024, 2025 or 2026', '2025 29 nights View Details Enquire Now MSC', '2026 2 nights View Details Enquire Now MSC', '2024 to 15', 'Warwick Technology Park, Gallows Hill, Warwick, CV34 6DA', '2025 4 nights View Details Enquire Now MSC', '1914 by 80', '1873 as the', 'Jebsen House, Ruislip, Middx, HA4 7BD', '414 per person price is based on MSC']")
#check if the two arrays have the same content
def check(a,b):
    if len(a)!=len(b):
        return False
    for i in range(len(a)):
        if a[i] not in b:
            return False
    return True
print(check(a,b))