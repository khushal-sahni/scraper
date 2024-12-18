import json
from .cache_layer import cache_price, get_cached_price, check_product_in_cache
from enum import Enum

DB_FILE = "db.json"

class OperationType(Enum):
	UPDATE = 1
	APPEND = 2
	NO_OP = 3

def find_product(product_title: str):
	try:
		with open(DB_FILE, "r") as f:
			db_data = json.load(f)
		for product in db_data:
			if product.get("product_title") == product_title:
				return product
		return None
	except FileNotFoundError:
		print(f"Database file {DB_FILE} not found")
		return None
	except json.JSONDecodeError:
		print(f"Error decoding JSON from file {DB_FILE}")
		return None
	
def update_product(product_title: str, updated_data: dict) -> bool:
	try:
		with open(DB_FILE, "r") as f:
			db_data = json.load(f)
		for product in db_data:
			if product.get("product_title") == product_title:
				product.update(updated_data)

				with open(DB_FILE, "w") as f:
					json.dump(db_data, f, indent=4)
					cache_price(product_title, updated_data.get("product_price"))
				print(f"Product {product_title} updated successfully")
				return True
		print(f"Product {product_title} not found in the database")
		return False
	except FileNotFoundError:
		print(f"Database file {DB_FILE} not found")
		return False
	except json.JSONDecodeError:
		print(f"Error decoding JSON from file {DB_FILE}")
		return False
	except Exception as e:
		print(f"An Unexpected error occured: {e}")
		return False
	
def insert_product(updated_data: dict) -> bool:
	try:
		with open(DB_FILE, "r") as f:
			db_data = json.load(f)
	except Exception as e:
		db_data = []
	db_data.append(updated_data)
	with open(DB_FILE, "w") as f:
		json.dump(db_data, f, indent=4)
		cache_price(updated_data.get("product_title"), updated_data.get("product_price"))
	
def find_and_update_product(product_title: str, updated_data: dict) -> OperationType:
	operation_type: OperationType = get_operation_type(product_title, updated_data)
	if operation_type == OperationType.UPDATE:
		update_product(product_title, updated_data)
	elif operation_type == OperationType.APPEND:
		insert_product(updated_data)
	else:
		print(f"No price changed for product {product_title}")
	return operation_type

			
def get_operation_type(product_title: str, updated_data: dict) -> OperationType:
	product_price = updated_data.get("product_price")
	if check_product_in_cache(product_title):
		old_price = get_cached_price(product_title)
		if product_price != old_price:
			return OperationType.UPDATE
		return OperationType.NO_OP
	
	old_product_data = find_product(product_title)
	if old_product_data:
		if old_product_data.get("product_price") != product_price:
			return OperationType.UPDATE
		return OperationType.NO_OP
	return OperationType.APPEND