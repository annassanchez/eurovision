import scrapy
import pandas as pd

class EurovisionSpider(scrapy.Spider):
    # The name of the spider
    name = 'eurovision_world'

    # These are the domains that we will scrape
    allowed_domains = ['eurovisionworld.com']

    # We will get the URLs from the JSON file passed to the spider using the -a option
    def __init__(self, json=None, *args, **kwargs):
        super(EurovisionSpider, self).__init__(*args, **kwargs)
        self.df = pd.read_json(json)
        self.start_urls = list(self.df['url'])  # Use all URLs in the dataframe

    def parse(self, response):
        prod_name = 'h1.mm'
        prod_table = 'table.v_table.v_table_main.table_sort.table_first.table_last.table_sort_added'

        # Put the data returned into the format we want to output for our csv or json file
        url = response.request.url
        yield {
            'name_raw': response.css(f'{prod_name}').get(),
            'table_raw': response.css(f'{prod_table}').get(),
            'url' : url,
        }

        # Get the next page URL from the dataframe and follow it
        next_page = self.df.loc[self.df['url'] == url, 'next_url'].iloc[0]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)