from django.db import models
from django.contrib.auth.models import User

class Customers(models.Model):
    birth_date = models.DateField(blank=False)
    phone_nr = models.CharField(max_length=15, blank=False)
    country = models.CharField(max_length=60, default="Polska", blank=False)
    city = models.CharField(max_length=45, blank=False)
    postal_code = models.CharField(max_length=6, blank=False)
    street = models.CharField(max_length=75, blank=False)
    house_nr = models.CharField(max_length=10, blank=False)
    flat_nr = models.PositiveIntegerField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    def __str__(self):
        return f"Klient: {self.user}"

class Categories(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"Kategoria: {self.name}"

class Producers(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return f"Producent: {self.name}"


class Furniture(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    availability = models.IntegerField()
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f"Mebel: {self.name}"


class Suppliers(models.Model):
    name = models.CharField(max_length=45)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2)
    max_weight = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"Dostawca: {self.name}"


class OrderStatus(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return f"Status zamówienia: {self.name}"


class DeliveryDetails(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=60)
    phone_nr = models.CharField(max_length=9)
    email = models.CharField(max_length=60)
    country = models.CharField(max_length=60, default="Polska")
    city = models.CharField(max_length=45)
    postal_code = models.CharField(max_length=5)
    street = models.CharField(max_length=75)
    house_nr = models.CharField(max_length=10)
    flat_nr = models.IntegerField()

    def __str__(self):
        return f"Dostawa do: {self.first_name, self.last_name}"


class PaymentMethods(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return f"Sposób płatności: {self.name}"


class PaymentStatus(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)

    def __str__(self):
        return f"Status płatności: {self.name}"


class Payments(models.Model):
    payment_method = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f"Płatność: {self.payment_method}"


class Orders(models.Model):
    total_cost_with_delivery = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_ordered = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    ordered_items = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    delivery_details = models.ForeignKey(DeliveryDetails, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f"Zamówienie nr: {self.id}"
