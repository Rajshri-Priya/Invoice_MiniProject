# Django Invoice API

This project implements a simple API to manage invoices and their details using Django and Django REST Framework (DRF). The API allows users to create, update, retrieve, and delete invoices along with their associated details in a single API call. Swagger UI is used for API documentation, unit testing used for testing and exception handling is implemented with a custom decorator.

## Features

- **Models:**
  - `Invoice`: A model that represents an invoice with fields for invoice number, customer name, and date.
  - `InvoiceDetail`: A model that represents the line items of the invoice with fields for description, quantity, price, and line total.
  
- **API Endpoints:**
  - `POST /api/invoices/`: Create a new invoice with its details.
  - `PUT /api/invoices/{id}`: Update an existing invoice and its details.
  - `GET /api/invoices/`: Retrieve a list of all invoices.
  - `GET /api/invoices/{id}/`: Retrieve details of a specific invoice by ID.
  - `DELETE /api/invoices/{id}/`: Delete an invoice by ID.
  
- **Swagger UI**: Automatically generated API documentation using Swagger for easy interaction with the API.

- **Exception Handling**: A custom decorator is used to handle various exceptions (e.g., `ValidationError`, `IntegrityError`, `KeyError`).

- **Unit Testing**: The application includes unit tests to verify the functionality of models, serializers, and views.


## Models

### Invoice Model
- `id`: Auto-incremented primary key.
- `invoice_number`: CharField (unique).
- `customer_name`: CharField.
- `date`: DateField.

### InvoiceDetail Model
- `id`: Auto-incremented primary key.
- `invoice`: ForeignKey to `Invoice`.
- `description`: CharField.
- `quantity`: IntegerField.
- `price`: DecimalField.
- `line_total`: DecimalField.

## Setup Instructions

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL (or use SQLite for local testing)

### 1. Clone the repository
```bash
git clone https://github.com/Rajshri-Priya/Invoice_MiniProject.git
cd Invoice_MiniProject
```
### 2. Install dependencies
You can use a virtual environment (recommended). First, install the required packages:
```bash
pip install -r requirements.txt
```
### 3. Set up the database
Make sure your database is set up correctly. If you're using PostgreSQL, create a database and configure the settings in the settings.py file. Otherwise, you can use the default SQLite database for local testing.

### 4. Apply migrations
Run the migrations to set up the database tables.
```bash
python manage.py migrate
```

### 5. Create a superuser
If you want to access the Django admin panel, you can create a superuser:
```bash
python manage.py createsuperuser
```
### 6. Run the development server
Start the Django development server:
```bash
python manage.py runserver
```
Your API will be accessible at http://127.0.0.1:8000/.

### Exception Handling
A custom decorator has been added to handle common exceptions like:

1. ValidationError
2. IntegrityError
3. KeyError
Any unexpected errors are handled gracefully with proper logging and a 500 status code response.

### API Documentation (Swagger UI)
Swagger UI is integrated and can be accessed at the following endpoint:
```bash
http://127.0.0.1:8000/swagger/
```
This provides a user-friendly interface to interact with the API, view available endpoints, and test them directly.

### Assumptions Made
- The invoice details must always be provided as an array of objects in the details field when creating or updating an invoice.
- The invoice_number is always unique when creating a new invoice.
- The line_total in the InvoiceDetail model is calculated based on quantity * price in the request payload.

