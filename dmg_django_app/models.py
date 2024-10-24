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
        return f"{self.name}"
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "supermarkets"
        db_table = "Supermarkets"

class Product(models.Model):
    """A product entity.""" 
    id = models.PositiveIntegerField(primary_key=True,
        unique=True, help_text="Product ID")
    name = models.CharField(max_length=500, help_text="The name of each product.")
    price = models.CharField(max_length=50, default=None)
    discounted_price = models.CharField(max_length=10, default=None, null=True)
    promotion = models.CharField(max_length=100, default=None, null=True)
    image = models.TextField(max_length=1000, default=None, null=True)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}\t{self.price}\t{self.discounted_price}"
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "products"
        db_table = "Products"

class Common(models.Model):
    """A data type used for general purposes."""
    name = models.CharField(max_length=50)
    value = models.TextField(max_length=1000)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = "Commons"
        verbose_name_plural = "commons"
        ordering = ["name"]