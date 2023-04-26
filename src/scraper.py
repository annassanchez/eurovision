from datetime import date
import json

def link_generator():
    """
    The link_generator() function generates a dictionary of Eurovision song contest URLs for each year from 1956 to the current year. 
    The URLs are stored in a dictionary called dict_urls which has two keys, year and url, with empty lists as their values.
    A loop is used to iterate through years from 1956 up to but not including the current year. 
    For each year, a URL is generated using an f-string that includes the year in the URL. 
    The year and the corresponding URL are then added as a key-value pair to the dictionary dict_urls.

    After generating all the URLs, the json.dump() function is used to write the contents of the dict_urls dictionary to a file named "sample.json" in JSON format.
    Finally, the dict_urls dictionary is returned by the function.
    """
    dict_urls = {
        'year':[], 
        'url':[]
    }
    for year in range(1956, int(date.today().year)):
        url = f'https://eurovisionworld.com/eurovision/{year}'
        dict_urls['year'].append(year)
        dict_urls['url'].append(url)
    with open("../eurovision_crawler/link.json", "w") as outfile:
        json.dump(dict_urls, outfile)
    return dict_urls