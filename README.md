# WEB_HW_9

pip install lxml
pip install requests
pip install beautifulsoup4

# practical example

poetry add beautifulsoup4
poetry add requests
poetry add sqlalchemy
poetry add Scrapy

# set path to config file
export CONFIG_PATH=config.ini

# scrappy

# in current dir
scrapy startproject test_spyder
# in created dir
scrapy genspider authors quotes.toscrape.com
# start some spider
scrapy crawl name_of_spider
