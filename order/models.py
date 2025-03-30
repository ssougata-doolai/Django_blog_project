from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length = 100, unique=True)
    price = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id
