from rest_framework.test import APITestCase
from rest_framework import status
from .models import Invoice, InvoiceDetail
from django.urls import reverse


class InvoiceAPITestCase(APITestCase):

    def setUp(self):
        """
        Set up the necessary data for the tests.
        """
        # Creating a test invoice
        self.invoice_data = {
            "invoice_number": "INV001",
            "customer_name": "Rajshri",
            "date": "2024-11-12",
            "details": [
                {
                    "description": "teddy",
                    "quantity": 1,
                    "price": 500.00,
                    "line_total": 500.00
                },
                {
                    "description": "micky-mouse",
                    "quantity": 2,
                    "price": 200.00,
                    "line_total": 400.00

                }
            ]
        }

        self.create_url = reverse('invoice-create')
        self.update_url = reverse('invoice-update', kwargs={'invoice_id': 1})
        # self.delete_url = reverse('invoice-delete', kwargs={'invoice_id': 1})

    def test_create_invoice(self):
        """
        Test creating a new invoice with details.
        """
        response = self.client.post(self.create_url, self.invoice_data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        #
        invoice = Invoice.objects.first()
        self.assertEqual(invoice.invoice_number, "INV001")
        self.assertEqual(invoice.customer_name, "Rajshri")
        self.assertEqual(str(invoice.date), "2024-11-12")

        details = invoice.details.all()
        self.assertEqual(details.count(), 2)
        self.assertEqual(details[0].description, "teddy")
        self.assertEqual(details[1].description, "micky-mouse")

    def test_update_invoice(self):
        """
        Test updating an existing invoice and its details.
        """
        invoice = Invoice.objects.create(
            invoice_number="INV002",
            customer_name="Jane Doe",
            date="2024-11-13"
        )

        InvoiceDetail.objects.create(
            invoice=invoice,
            description="Product A",
            quantity=2,
            price=50.00,
            line_total=100.00
        )

        updated_invoice_data = {
            "invoice_number": "INV003",
            "customer_name": "Jane Smith",
            "date": "2024-11-14",
            "details": [
                {"description": "Product X", "quantity": 3, "price": 30.00, "line_total": 90.00},
                {"description": "Product Y", "quantity": 1, "price": 60.00, "line_total": 60.00}
            ]
        }

        response = self.client.put(reverse('invoice-update', kwargs={'invoice_id': invoice.id}), updated_invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        invoice.refresh_from_db()
        self.assertEqual(invoice.invoice_number, "INV003")
        self.assertEqual(invoice.customer_name, "Jane Smith")
        self.assertEqual(str(invoice.date), "2024-11-14")

        details = invoice.details.all()
        self.assertEqual(details.count(), 2)
        self.assertEqual(details[0].description, "Product X")
        self.assertEqual(details[1].description, "Product Y")

    def test_create_invoice_invalid_data(self):
        """
        Test creating an invoice with invalid data (e.g., missing required fields).
        """
        invalid_data = {
            "customer_name": "John Doe",
            "date": "2024-11-12",
            "details": [
                {"description": "Product A", "quantity": 2, "price": 50.00, "line_total": 100.00}
            ]
        }

        response = self.client.post(self.create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_update_invoice_not_found(self):
        """
        Test trying to update an invoice that doesn't exist.
        """
        response = self.client.put(reverse('invoice-update', kwargs={'pk': 999}), self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_create_invoice_duplicate_invoice_number(self):
        """
        Test creating an invoice with a duplicate invoice number.
        """
        self.client.post(self.create_url, self.invoice_data, format='json')
        duplicate_data = self.invoice_data.copy()
        duplicate_data['invoice_number'] = 'INV001'
        response = self.client.post(self.create_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_delete_invoice(self):
        """
        Test deleting an existing invoice.
        """
        invoice = Invoice.objects.create(
            id=1,
            invoice_number="INV002",
            customer_name="Jane Doe",
            date="2024-11-13"
        )

        response = self.client.delete(reverse('invoice-delete', kwargs={'invoice_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)

