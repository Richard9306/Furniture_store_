from django.contrib import admin
from my_store import models
# Register your models here.
admin.site.register(models.Customers)
admin.site.register(models.Categories)
admin.site.register(models.Producers)
admin.site.register(models.Furniture)
admin.site.register(models.Suppliers)
admin.site.register(models.OrderStatus)
admin.site.register(models.DeliveryDetails)
admin.site.register(models.PaymentMethods)
admin.site.register(models.PaymentStatus)
admin.site.register(models.Payments)
admin.site.register(models.Orders)