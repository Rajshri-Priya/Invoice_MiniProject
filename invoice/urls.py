from django.urls import path
from .views import InvoiceCreateUpdateAPIView

urlpatterns = [
    path('api/invoices/', InvoiceCreateUpdateAPIView.as_view(), name='invoice-create'),
    path('api/invoices/', InvoiceCreateUpdateAPIView.as_view(), name='get-invoice'),
    path('api/invoices/<int:invoice_id>/', InvoiceCreateUpdateAPIView.as_view(), name='invoice-update'),
    path('api/invoices/<int:invoice_id>/', InvoiceCreateUpdateAPIView.as_view(), name='get-invoice'),
    path('api/invoices/<int:invoice_id>/', InvoiceCreateUpdateAPIView.as_view(), name='invoice-delete'),

]
