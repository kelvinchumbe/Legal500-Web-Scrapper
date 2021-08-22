import scrapy
import json

def stripNotNone(text):
    """ Strips text if text is a string and not None
    param: text: string with leading/ trailing spaces
    return: stripped string
    """
    if text is None:
        return text

    return text.strip()

class Legal500Spider_2(scrapy.Spider):
    """
    A Scrapy Spider class to scrap the Legal500 firm details website
    """
    name="legal500_spider2"
    allowed_domains = ['legal500.com']

    def __init__(self, filename=None):
        # Open json file with urls to company directories and load the urls as the start_urls
        with open(filename, 'r', encoding='latin1') as file:
            data = json.load(file)
            self.start_urls = [firm_url for firm in data for firm_url in firm['firm_urls']]

    def parse(self, response):
        # Get the source of the logo image and build a url to the image
        firm_logo = "https://www.legal500.com" + response.xpath("//div[@id='left-col']/img/@data-lazy-src").get() if response.xpath("//div[@id='left-col']/img/@data-lazy-src").get() is not None else None

        firm_address = ' '.join([paragraph.strip() for paragraph in response.xpath("//div[@id='left-col']/div[@class='address-box']/address//text()").extract()])

        firm_website = response.xpath("//div[@id='left-col']/div[contains(@class,'contact-box')]/div/span[2]/a/@href").get()

        firm_phone_no = stripNotNone(response.xpath("//div[@id='left-col']/div[contains(@class,'contact-box')]/div/span[3]/text()").get())

        firm_email = response.xpath("//div[@id='left-col']/div[contains(@class,'contact-box')]/div/span[1]/a/@href").get()
        
        firm_email = firm_email.split('?')[0].split(':')[1] if firm_email is not None else None

        practice_heads = [name for list in response.xpath("//div[@class='extra_info']/div[@class='practice-heads']/div/p//text()").extract() for name in list.strip().split('; ') if name != ';']

        key_clients = response.xpath("//div[@class='extra_info']/div[contains(@class,'key-clients')]/div/p/text()").extract()

        membership = [member.strip() for item in response.css('div#memberships_section::text').getall() for member in item.strip().split('\n') if member.strip()]

        # Get the list of lawyers
        lawyers_list = [lawyer.strip() for lawyer in response.xpath("//table[@id='lawyer-profiles-list']/tbody/tr/td[@class='profile-name']/text()").extract()]

        # If unavailable, create a set using the lawyers from the main contacts section
        if lawyers_list == []:
            lawyers_list = set([name.strip() for name in response.xpath("//table[@class='main-contacts']/tbody/tr/td[2]/text()").extract() if name.strip()])

        # If the firm has a logo image, scrap the required information and download the logo else just scrap the required information
        if firm_logo is not None:
            yield dict(
                image_urls = [firm_logo],
                firm_address=firm_address,
                firm_website=firm_website,
                firm_phone_no=firm_phone_no,
                firm_email=firm_email,
                practice_heads=practice_heads,
                key_clients=key_clients,
                membership=membership,
                lawyers_list=lawyers_list
            )
        else:
            yield dict(
                firm_address=firm_address,
                firm_website=firm_website,
                firm_phone_no=firm_phone_no,
                firm_email=firm_email,
                practice_heads=practice_heads,
                key_clients=key_clients,
                membership=membership,
                lawyers_list=lawyers_list
            )
