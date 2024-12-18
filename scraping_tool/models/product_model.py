from pydantic import BaseModel, Field

class ProductModel(BaseModel):
    product_title: str = Field(..., min_length=1, max_length=255, description="Title of the product")
    product_price: float = Field(..., ge=0, description="Price of the product, must be greater than or equal to 0")
    path_to_image: str = Field(None, min_length=1, max_length=1000, description="URL or path to the product image")
