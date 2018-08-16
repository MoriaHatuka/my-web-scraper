import sqlite3

DB_NAME = "web_scraper_db.db"

class DataBase:

	def init_database(self):
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS products
		(_id INTEGER PRIMARY KEY, name TEXT, price INT)''')

	def insert_product(self, product):
		'''
		gets product
		insert product to products table
		'''
		try:
			print("Connecting to DB...")
			conn = sqlite3.connect(DB_NAME)
			print("Connected to DB... insert new product")
			curs = conn.cursor()
			product_to_write = (product.name, product.price)
			query = '''INSERT INTO products (name, price) VALUES (?,?)'''
			curs.execute(query, product_to_write)
			conn.commit()
			result = curs
			curs.close()
			conn.close()
		except Exception as e:
			logging.error(f'Unable to access database {e}')

	def remove_products(self):
		'''
		remove products from products table (used for tests)
		'''
		conn = sqlite3.connect(DB_NAME)
		print("Connected to DB to delete products table...")
		curs = conn.cursor()
		query = '''DELETE from products'''
		curs.execute(query)
		conn.commit()
		curs.close()
		conn.close()

	def get_products(self):
		'''
		return products table (used for tests)
		'''
		print("Connecting to DB to get products table...")
		conn = sqlite3.connect(DB_NAME)
		print("Connected to DB...")
		curs = conn.cursor()
		query = '''SELECT * from products'''
		curs.execute(query)
		products_list = curs.fetchall()
		curs.close()
		conn.close()
		return products_list