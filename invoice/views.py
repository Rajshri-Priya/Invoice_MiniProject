from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice
from .serializers import InvoiceSerializer
from .exception_handler import handle_exceptions


class InvoiceCreateUpdateAPIView(APIView):
    @swagger_auto_schema(request_body=InvoiceSerializer)
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new Invoice along with its details.
        """
        serializer = InvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @handle_exceptions
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve invoices (single or all invoices).
        """
        invoice_id = kwargs.get('invoice_id')
        if invoice_id:
            invoice = Invoice.objects.get(id=invoice_id)
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            invoices = Invoice.objects.all()
            serializer = InvoiceSerializer(invoices, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @handle_exceptions
    @swagger_auto_schema(request_body=InvoiceSerializer)
    def put(self, request, *args, **kwargs):
        """
        Handle PUT request to update an existing Invoice and its details.
        """
        invoice = Invoice.objects.get(id=kwargs.get('invoice_id'))  # No try-except here
        serializer = InvoiceSerializer(invoice, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @handle_exceptions
    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE request to delete a specific invoice by its ID.
        """
        invoice_id = kwargs.get('invoice_id', None)

        if invoice_id:
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.delete()  # Delete the invoice
            return Response({"message": "Invoice deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invoice ID is required."}, status=status.HTTP_400_BAD_REQUEST)

# class InvoiceUpdateDeleteAPIView(APIView):
