import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import sys
import time 

from product import Product
from database import DataBase

NA = -1
OK = 200
AMAZON = 'amazon'
EBAY = 'ebay'


class WebScraper:

	def __init__(self):
		self.db = DataBase()

	def start(self, urls_file_name):
		'''
		gets urls' file name, read the urls to list,
		execute thread pool of 4 workers for scraping amazon and ebay products
		'''
		urls = self.get_urls_list(urls_file_name)
		with ThreadPoolExecutor(max_workers=4) as executor:
			for url in urls:
				if self.check_website_type_by_url(url) == AMAZON:
					executor.submit(self.extract_amazon_product, url)					
				else:
					executor.submit(self.extract_ebay_product, url)
	
	def get_urls_list(self, file_name):
		urls_list = []
		f = open(file_name, 'r')
		my_file_data = f.read()
		f.close()
		urls_list = my_file_data.split('\n')
		return urls_list

	def check_website_type_by_url(self, url):
		if url.find(AMAZON, 12) != NA:
			return AMAZON
		else:
			return EBAY

	def extract_amazon_product(self, url):
		url_content_res = self.download_url_content(url)
		if url_content_res != NA:
			soup = BeautifulSoup(url_content_res.text, "lxml")
			price = soup.find(id="priceblock_ourprice").get_text()
			str_name = soup.find(id="productTitle").get_text()
			name = str_name.strip()
			amazon_product = Product(name, price)
			self.insert_product(amazon_product)
		else:
			print("URL content is NOT avaliable")

	def extract_ebay_product(self, url):
		url_content_res = self.download_url_content(url)
		if url_content_res != NA:
			soup = BeautifulSoup(url_content_res.text, "lxml")
			str_price = soup.find(id = "prcIsum").get_text()
			price = str_price[4:]
			str_name = soup.find(id="itemTitle").get_text()
			name = str_name[16:]
			ebay_product = Product(name, price)
			self.insert_product(ebay_product)
		else:
			print("URL content is NOT avaliable")

	def download_url_content(self, url):
		ua = {"User-Agent":"Mozilla/5.0"}
		res = requests.get(url, headers=ua)
		if res.status_code == OK:
			return res
		else:
			print("requests NOT OK!")
			return NA

	def insert_product(self, product):
		self.db.insert_product(product)


def main(urls_file_name):
	db = DataBase()
	db.init_database()

	web_scraper = WebScraper()
	web_scraper.start(urls_file_name)


if __name__ == "__main__":
	main(sys.argv[1])