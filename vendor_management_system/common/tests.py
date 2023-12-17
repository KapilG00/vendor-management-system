import uuid
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from vendor.models import Vendor, PurchaseOrder


class BaseAPITestCase(APITestCase):

    def setUp(self):
        # Common setup code for all test cases.
        self.user = self.create_user(email='test@example.com', username='testuser', password='testpassword')
        self.token = self.obtain_token(email='test@example.com', password='testpassword')

    def create_user(self, email, username, password):
        return User.objects.create_user(email=email, username=username, password=password)
        
    def obtain_token(self, email, password):
        url = reverse('home:login')
        data = {
            'email': email,
            'password': password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        return response.data['results']['access_token']
    

class CommonAPITestCase(APITestCase):

    def create_vendor(self):
        return Vendor.objects.create(name='test vendor',
                                     contact_details='+1(123)456-7890',
                                     address='Apt. 622 687 Flatley Mill, Murrayfort, UT 26795.',
                                     vendor_code= '322')

    def create_purchase_order(self):
        vendor_obj = self.create_vendor()
        items = [{'item 1': 2500, 'item 2': 1800}]
        return PurchaseOrder.objects.create(vendor=vendor_obj, items=items, quantity=len(items), po_number=1921)
    
    def create_completed_purchase_order(self):
        vendor_obj = self.create_vendor()
        items = [{'item 1': 2500, 'item 2': 1800}]
        return PurchaseOrder.objects.create(vendor=vendor_obj, status='completed', prev_status='pending', items=items, quantity=len(items), po_number=1921)
    
    def create_canceled_purchase_order(self):
        vendor_obj = self.create_vendor()
        items = [{'item 1': 2500, 'item 2': 1800}]
        return PurchaseOrder.objects.create(vendor=vendor_obj, status='canceled', prev_status='pending', items=items, quantity=len(items), po_number=1921)

    def create_bulk_vendor_purchase_order(self):
        vendor_obj = self.create_vendor()
        po_data = [
            {'items': {'item 1': 2500, 'item 2': 1800}, 'po_number': '100'},
            {'items': {'item 1': 2500, 'item 2': 1800, 'item3': 1450}, 'po_number': '101'},
            {'items': {'item 1': 12000, 'item 2': 3450}, 'po_number': '102'},
            {'items': {'item 1': 990}, 'po_number': '103'}
        ]
        purchase_order_list = [PurchaseOrder(po_uuid=uuid.uuid4().hex, items=po['items'], quantity=len(po['items']), po_number=po['po_number'], vendor=vendor_obj)for po in po_data]
        PurchaseOrder.objects.bulk_create(purchase_order_list)
        return vendor_obj
    
    def create_bulk_vendor(self):
        vendor_data = [
            {'vendor_code': '1010', 'name': 'test vendor 1', 'contact_details': '+1(123)456-7890', 'address': 'Apt. 622 681 Flatley Mill, Murrayfort, UT 26795.'},
            {'vendor_code': '1011', 'name': 'test vendor 2', 'contact_details': '+1(123)456-7891', 'address': 'Apt. 623 682 Flatley Mill, Murrayfort, UT 26795.'}
        ]
        vendor_list = [Vendor(vendor_uuid=uuid.uuid4().hex,
                                      vendor_code=vendor['vendor_code'],
                                      name=vendor['name'],
                                      contact_details=vendor['contact_details'],
                                      address=vendor['address']) for vendor in vendor_data]
        Vendor.objects.bulk_create(vendor_list)

    def create_bulk_purchase_order(self):
        self.create_bulk_vendor()
        po_data = [
            {'items': {'item 1': 2500, 'item 2': 1800}, 'po_number': '100', 'vendor_code': '1010'},
            {'items': {'item 1': 2500, 'item 2': 1800, 'item3': 1450}, 'po_number': '101', 'vendor_code': '1011'},
            {'items': {'item 1': 12000, 'item 2': 3450}, 'po_number': '102', 'vendor_code': '1011'},
            {'items': {'item 1': 990}, 'po_number': '103', 'vendor_code': '1010'}
        ]
        purchase_order_list = [PurchaseOrder(po_uuid=uuid.uuid4().hex,
                                                items=po['items'],
                                                quantity=len(po['items']),
                                                po_number=po['po_number'],
                                                vendor=Vendor.objects.get(vendor_code=po['vendor_code']))for po in po_data]
        PurchaseOrder.objects.bulk_create(purchase_order_list)