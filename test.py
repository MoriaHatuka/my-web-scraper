from webScraper import WebScraper
from database import DataBase


class WebScraperTests:
	def setUp(self):
		self.web_scraper = WebScraper()
		self.db = DataBase()

	def test_start(self):
		self.db.remove_products()
		self.web_scraper.start("URLsList.txt")
		products = self.db.get_products()
		if len(products) > 0:
			print(f'OK {len(products)}')
		else:
			print(f'NOT OK {len(products)}')


web_scraper_test = WebScraperTests()
web_scraper_test.setUp()
web_scraper_test.test_start()