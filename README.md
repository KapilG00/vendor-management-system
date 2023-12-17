r# Vendor Management System

## Overview

Developed a 'Vendor Management System' using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics.

## Setup

### Prerequisites

Make sure you have the following installed:

- Python (version 3.11.3)
- Virtualenv (optional but recommended)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/KapilG00/vendor-management-system.git
    ```

2. Navigate to the project directory:

    ```bash
    cd vendor_management_system
    ```

3. Create and activate a virtual environment (optional but recommended):
    
    ```bash
    virtualenv venv
    ```

    ```bash
    source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Install database (recommended Postgresql):
   
   ### Below commands are specific to Postgresql, make necessary changes if any.

   After successful installation, login to psql-shell/Terminal to create database using following commands:

   ```bash
   CREATE ROLE vendor_management_system;
   ```
   ```bash
   ALTER ROLE vendor_management_system WITH PASSWORD 'vendor_management_system';
   ```
   ```bash
   ALTER ROLE vendor_management_system WITH LOGIN;
   ```
   ```bash
   CREATE DATABASE vendor_management_system WITH OWNER vendor_management_system;
   ```
   ```bash
   GRANT ALL PRIVILEGES ON DATABASE vendor_management_system TO vendor_management_system;
   ```

6. Apply database migrations and create Superuser:

    ```bash
    python manage.py migrate
    ```

    ```bash
    python manage.py createsuperuser
    ```

### Configuration

 Update the values in the `.env` file with your specific configuration.

### Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

### API Endpoints
### 1. User Login : /api/auth/user-login/

    This view allows users to Log In and obtain authentication tokens.

    Method : POST

    Request Body :

    {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
### 2. User Registration : /api/auth/user-registration/

    This view allows users to register and create a new account.

    Method : POST

    Request Body :

    {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword"
    }

### 3. Fetching all vendor's : /api/vendors/

    This view allows user to retrieve details of all vendor's.

    Method : GET

### 4. Fetching particular vendor : /api/vendors/{vendor_id}/

    This view allows user to retrieve details of a particular vendor.

    Method : GET

### 5. Creating a vendor : /api/vendors/

    This view allows user to create a new vendor.

    Method : POST

    Request Body :

    {
        "name": "vendor name",
        "contact_details": " vendor contact details",
        "address": "vendor address",
        "vendor_code": "322"
    }

### 6. Updating a vendor : /api/vendors/{vendor_id}/

    This view allows vendor to update it's details.

    Method : PUT

    Request Body :

    {
        "name": "updated name",
        "contact_details": " updated vendor contact details",
        "address": "updated vendor address"
    }

### 7. Deleting a vendor : /api/vendors/{vendor_id}/

    This view allows user to delete already existing vendor'.

    Method : DELETE

### 8. Fetching all purchase order's : /api/purchase_orders/

    This view allows user to retrieve details of all purchase order's. 
    
    It also allows to filter based on vendor. Below is the related URL.

    /api/purchase_orders/?vendor_id=322

    Method : GET

### 9. Creating a purchase order : /api/purchase_orders/

    This view allows buyer(s)/customer(s) to create a new purchase order.

    Method : POST
    
    Request Body :

    {
        "items": {
            "item1": 3200
        },
        "po_number": "1437",
        "vendor_code": "322"
    }
    
    Note :- "items" dict => {"item name": item price}

### 10. Fetching particular purchase order : /api/purchase_orders/{po_id}/

    This view allows user to retrieve details of a particular purchase order.

    Method : GET    
 
### 11. Updating a purchase order : /api/purchase_orders/{po_id}/

    This view allows vendor(s) and buyer(s)/customer(s) to update an already existing purchase order.

    Method : PUT
    
    Request Body :

    {
        "status": "completed",
        "quality_rating": 5.5  # This is passed only when buyer rates the PO, it is provided by buyer.
    }

### 12. Deleting a purchase order : /api/purchase_orders/{po_id}/

    This view allows user to delete an already existing purchase order.

    Method : DELETE

### 13. Fetching a particular vendor performance metrics : /api/vendors/{vendor_id}/performance/

    This view allows user to retrieve particular vendor's performance metrics.

    Method : GET

### 14. Vendor acknowledge's the purchase order : /api/purchase_orders/{po_id}/acknowledge/

    This view allows vendor to acknowlegde a particular purchase order.

    Method : POST

### Testing

To run the test suite, use the following command:

```bash
python manage.py test
```
This will execute the test suite and provide feedback on the test results.

To run the app specific test cases, use the following command:

```bash
python manage.py test app_name
```
This will execute all the tests specific to the app and provide feedback on the test results.

## Contact
For questions or feedback, please email me at kapil.gupta4949@gmail.com.
