from django.db import models

# Create your models here.
class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(unique=True)
    price = models.IntegerField(default=0)


class Order(models.Model):
    user_id = models.IntegerField()
    service_id = models.ForeignKey(Service, on_delete=models.PROTECT, to_field='id')
    order_date = models.DateTimeField(auto_now_add=True, db_index=True)
