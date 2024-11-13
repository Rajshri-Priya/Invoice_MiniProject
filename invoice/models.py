from django.db import models


# Create your models here.
class Invoice(models.Model):
    class Meta:
        db_table = "invoice"

    id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer_name}"


class InvoiceDetail(models.Model):
    class Meta:
        db_table = "invoice_detail"

    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='details')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.line_total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.quantity} x {self.price}"
