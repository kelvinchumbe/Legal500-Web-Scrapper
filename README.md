# Legal500-Web-Scrapper

This is a Scrapy Web Spider that scraps information about companies listed on the Legal500 directory site.

### How to run the script
1. cd to the directory where the requirements.txt file is located
2. **run:** *pip install -r requirements.txt* in your shell to install the required dependencies
3. **run:** *scrapy crawl legal500_spider1 -a directory_url="name_of_legal500_directory"  -O "filepath_to_save_output.json"*

    The -a command allows you to pass an argument to the directory_url parameter
    
    The -O command allows you to define the location and file to store the output
    
**NB:** Wait for the script to finish running

4. **run:**  *scrapy crawl legal500_spider2 -a filename="filepath_to_saved_output_from_spider1" -O "filepath_to_save_output.json"*

### Some commands to get you started
**To run the first script:**
scrapy crawl legal500_spider1 -a directory_url="https://www.legal500.com/c/germany/directory/"  -O "../scrapped_data/firm_urls.json"

**To run the second script:**
scrapy crawl legal500_spider2 -a filename="../scrapped_data/firm_urls.json" -O "../scrapped_data/firm_details.json"
