from pydantic import ValidationError
from models.product_model import ProductModel

def validate_product(product):
	try:
		validated_product = ProductModel(**product)
		return validated_product
	except ValidationError as e:
		print(f"Validation Error: {e}")
		return None