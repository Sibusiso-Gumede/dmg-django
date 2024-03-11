from django.db import models

class Supermarket(models.Model):
    """A supermarket entity."""
    supermarket_id = models.PositiveIntegerField(primary_key=True,
                                         unique=True,
                                         help_text=f"The supermarket id")
    supermarket_name = models.CharField(unique=True,
                                        max_length=50,
                                        help_text=f"The supermarket name")
    num_of_products = models.PositiveIntegerField(
        help_text=f"The total number of different products sold")
    
    def __str__(self) -> str:
        return f"{self.supermarket_name}"
    
    class Meta:
        ordering = ["supermarket_name"]
    
class Category(models.Model):
    """A product category entity."""
    category_id = models.CharField(primary_key=True,
                                unique=True,
                                max_length=20,
                                help_text=f"The category ID")
    category_name = models.CharField(max_length=30, unique=True,
                                help_text=f"Category name")
    num_of_products = models.PositiveIntegerField(
                        help_text=f"Number of products in the category")

    def __str__(self) -> str:
        return f"{self.category_name}"
    
    class Meta:
        ordering = ["category_name"]

class Product(models.Model):
    """A product entity.""" 
    product_id = models.PositiveIntegerField(primary_key=True,
        unique=True, help_text=f"Product ID")
    product_name = models.CharField(max_length=100, help_text=f"The name of each product.")
    price = models.DecimalField(max_digits=5, decimal_places=2, default=000.00)
    promotion_start_date = models.DateField()
    promotion_end_date = models.DateField()
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product_name}"
    
    class Meta:
        ordering = ["product_name"]