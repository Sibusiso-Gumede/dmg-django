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
    statistics = models.JSONField(default=dict, 
                help_text="The total number of stores per province.")

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "supermarkets"
        db_table = "Supermarkets"

class Category(models.Model):
    """A product category entity."""
    id = models.CharField(primary_key=True,
                            unique=True,
                            max_length=20,
                            help_text="The category ID")
    name = models.CharField(max_length=30, unique=True,
                            help_text="Category name")
    num_of_products = models.PositiveIntegerField(
                        help_text="Number of products in the category")

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"
        db_table = "Categories"

class Product(models.Model):
    """A product entity.""" 
    id = models.PositiveIntegerField(primary_key=True,
        unique=True, help_text="Product ID")
    name = models.CharField(max_length=100, help_text="The name of each product.")
    price = models.CharField(max_length=50, default="R0.00")
    discounted_price = models.CharField(max_length=10, default=None)
    promotion = models.CharField(max_length=100, default=None)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}\t{self.price}\t{self.discounted_price}"
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "products"
        db_table = "Products"