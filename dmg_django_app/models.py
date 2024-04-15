from django.db import models

class Supermarket(models.Model):
    """A supermarket entity."""
    id = models.PositiveIntegerField(primary_key=True,
                                         unique=True,
                                         help_text="The supermarket id")
    name = models.CharField(unique=True,
                                        max_length=50,
                                        help_text="The supermarket name")
    num_of_products = models.PositiveIntegerField(
        help_text="The total number of different products sold")

    def __str__(self) -> str:
        return f"{self.supermarket_name}"
    
    class Meta:
        ordering = ["name"]
    
class Category(models.Model):
    """A product category entity."""
    category_id = models.CharField(primary_key=True,
                                unique=True,
                                max_length=20,
                                help_text="The category ID")
    category_name = models.CharField(max_length=30, unique=True,
                                help_text="Category name")
    num_of_products = models.PositiveIntegerField(
                        help_text="Number of products in the category")

    def __str__(self) -> str:
        return f"{self.category_name}"
    
    class Meta:
        ordering = ["category_name"]

class Product(models.Model):
    """A product entity.""" 
    id = models.PositiveIntegerField(primary_key=True,
        unique=True, help_text="Product ID")
    name = models.CharField(max_length=100, help_text="The name of each product.")
    price = models.CharField(max_length=15, default="R 000.00")
    promotion = models.CharField(max_length=100, default="None")
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        ordering = ["name"]