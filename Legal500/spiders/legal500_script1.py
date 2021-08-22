import scrapy

def stripNotNone(text):
    """ Strips text if text is a string and not None
    param: text: string with leading/ trailing spaces
    return: stripped string
    """
    if text is None:
        return text

    return text.strip()

class Legal500Spider(scrapy.Spider):
    """
    A Scrapy Spider class to scrap the Legal500 directory website
    """
    name = 'legal500_spider1'
    allowed_domains = ['legal500.com']

    def __init__(self, directory_url=None):
        # Initializes the start_urls with the passed in directory_url
        self.start_urls = [directory_url]

    def parse(self, response):
        # Get a list of all the firms
        firms = response.xpath("//ul[@id='directoryUL']/li").extract()

        # Iterate through each firm and scrape the required information
        for firm in firms:
            # Build a scrapy selector object from the firm's html
            response_selector = scrapy.Selector(text=firm)

            firm_name = stripNotNone(response_selector.css('a > strong::text').get()) if response_selector.css('li::attr(class)').get() == 'single-office' else ''.join([name for name in response_selector.css('li::text').getall() if name and name != ', ']).strip()

            locations = [location.strip() for location in response_selector.css('a::text').getall() if location.strip() and location != ',']

            firm_urls = ["https://www.legal500.com" + url for url in response_selector.css('a::attr(href)').getall()]

            yield dict(
                firm_name=firm_name,
                locations=locations,
                firm_urls=firm_urls,
            )

            