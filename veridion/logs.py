def log_error_from_fetch(url):
    f= open("fetch.log","a")
    f.write(url + ": " + "Error fetching URL\n")
def  log_status(url,address_list):
    f= open("fetch.log","a")
    f.write(url + ": " + str(len(address_list)) + " addresses fetched\n")