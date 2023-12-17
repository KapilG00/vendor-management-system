from datetime import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from common.tests import BaseAPITestCase, CommonAPITestCase


class CreateVendorTest(BaseAPITestCase):

    def test_vendor_creation_success(self):
        url = reverse('vendor:vendor-view')
        data = {
            'name': 'test vendor',
            'contact_details': '+1(614)332-6511',
            'address': 'Apt. 622 687 Flatley Mill, Murrayfort, UT 26795.',
            'vendor_code': '322'
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['results']['vendor_code'], '322')

    def test_vendor_creation_failure(self):
        url = reverse('vendor:vendor-view')
        data = {
            'name': 'test vendor',
            'contact_details': '+1(614)332-6511',
            'address': 'Apt. 622 687 Flatley Mill, Murrayfort, UT 26795.',
            'vendor_code': ''
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1)    


class FetchVendorListTest(BaseAPITestCase, CommonAPITestCase):

    def test_fetch_vendor_list_success(self):
        self.create_vendor()
        url = reverse('vendor:vendor-view')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['status_message'], 'Successfully fetched vendors list.')

    def test_fetch_vendor_list_failure(self):
        url = reverse('vendor:vendor-view')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1)
        self.assertEqual(response.data['status_message'], 'No vendors found, please create one.')    


class FetchVendorTest(BaseAPITestCase, CommonAPITestCase):

    def test_fetch_vendor_success(self):
        vendor = self.create_vendor()
        url = reverse('vendor:modify-vendor-view', kwargs={'vendor_id': vendor.vendor_code})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['status_message'], 'Successfully fetched vendor details.')

    def test_fetch_vendor_failure(self):
        self.create_vendor()
        vendor_id = 1437
        url = reverse('vendor:modify-vendor-view', kwargs={'vendor_id': vendor_id})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1)
        self.assertEqual(response.data['status_message'], f'Vendor with {vendor_id} vendor code does not exists.')    


class UpdateVendorTest(BaseAPITestCase, CommonAPITestCase):

    def test_update_vendor_success(self):
        vendor = self.create_vendor()
        url = reverse('vendor:modify-vendor-view', kwargs={'vendor_id': vendor.vendor_code})
        data = {
            'name': 'updated vendor',
            'contact_details': '+1(614)332-9900',
            'address': 'Apt. 622 687 Flatley Mill, Murrayfort, UT 26795.'
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.put(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['status_message'], 'Successfully updated vendor details.')
        self.assertEqual(response.data['results']['name'], 'updated vendor')

    def test_update_vendor_failure(self):
        self.create_vendor()
        vendor_id = 1437
        url = reverse('vendor:modify-vendor-view', kwargs={'vendor_id': vendor_id})
        data = {
            "name": "updated vendor",
            "contact_details": "testvendor1@gmail.com",
            "address": "This is the address of test vendor.",
            "vendor_code": ""
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.put(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1)
        self.assertEqual(response.data['status_message'], f'Vendor with {vendor_id} vendor code does not exists.')    


class DeleteVendorTest(BaseAPITestCase, CommonAPITestCase):

    def test_delete_vendor_success(self):
        vendor = self.create_vendor()
        url = reverse('vendor:modify-vendor-view', kwargs={'vendor_id': vendor.vendor_code})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.delete(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['status_message'], 'Successfully deleted a vendor.')
        self.assertEqual(response.data['results'], True)

    def test_delete_vendor_failure(self):
        self.create_vendor()
        vendor_id = 1437
        url = reverse('vendor:modify-vendor-view', kwargs={'vendor_id': vendor_id})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.delete(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1)
        self.assertEqual(response.data['status_message'], f'Vendor with {vendor_id} vendor code does not exists.')


class CreatePurchaseOrderTest(BaseAPITestCase, CommonAPITestCase):

    def test_purchase_order_creation_success(self):
        vendor = self.create_vendor()
        url = reverse('vendor:vendor-purchase-order-view')
        data = {
            'items': {
                'item 1': 2500,
                'item 2': 1800
            },
            'po_number': '1921',
            'vendor_code': vendor.vendor_code
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['results']['status'], 'pending')

    def test_purchase_order_creation_failure(self):
        self.create_vendor()
        vendor_id = '1437'
        url = reverse('vendor:vendor-purchase-order-view')
        data = {
            'items': {
                'item 1': 2500,
                'item 2': 1800
            },
            'po_number': '1921',
            'vendor_code': vendor_id
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1)
        self.assertEqual(response.data['status_message'], f'Vendor with {vendor_id} vendor code does not exists.')


class FetchPurchaseOrderListTest(BaseAPITestCase, CommonAPITestCase):

    def test_fetch_purchase_order_list_success(self):
        self.create_bulk_purchase_order()
        url = reverse('vendor:vendor-purchase-order-view')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1) 
        self.assertEqual(response.data['status_message'], 'Successfully fetched all purchase orders details.')

    def test_fetch_purchase_order_list_failure(self):
        self.create_bulk_vendor()
        url = reverse('vendor:vendor-purchase-order-view')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], 'No purchase orders found; please place an order first.')    

    def test_fetch_vendor_purchase_order_list_success(self):
        vendor_obj = self.create_bulk_vendor_purchase_order()
        url = reverse('vendor:vendor-purchase-order-view')
        url_with_param = f'{url}?vendor_id={vendor_obj.vendor_code}'
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url_with_param, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1) 
        self.assertEqual(response.data['status_message'], 'Successfully fetched all purchase orders details.')

    def test_fetch_vendor_purchase_order_list_failure(self):
        vendor_obj = self.create_vendor()
        url = reverse('vendor:vendor-purchase-order-view')
        url_with_param = f'{url}?vendor_id={vendor_obj.vendor_code}'
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url_with_param, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], 'No purchase orders found; please place an order first.')

    def test_fetch_vendor_not_found_failure(self):
        self.create_bulk_vendor_purchase_order()
        vendor_code = 399
        url = reverse('vendor:vendor-purchase-order-view')
        url_with_param = f'{url}?vendor_id={vendor_code}'
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url_with_param, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], f'Vendor with {vendor_code} vendor code does not exists.')    


class FetchVendorPurchaseOrderTest(BaseAPITestCase, CommonAPITestCase):

    def test_fetch_purchase_order_success(self):
        po_obj = self.create_purchase_order()
        url = reverse('vendor:modify-purchase-order-view', kwargs={'po_id': po_obj.po_number})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1) 
        self.assertEqual(response.data['status_message'], 'Successfully fetched purchase order details.')

    def test_fetch_purchase_order_failure(self):
        self.create_vendor()
        po_number = '1900'
        url = reverse('vendor:modify-purchase-order-view', kwargs={'po_id': po_number})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)
        
        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], f'Purchase order with {po_number} purchase order number does not exists.')


class UpdatePurchaseOrderTest(BaseAPITestCase, CommonAPITestCase):

    def test_update_purchase_order_success(self):
        po_obj = self.create_purchase_order()
        url = reverse('vendor:modify-purchase-order-view', kwargs={'po_id': po_obj.po_number})
        data = {
            'status': 'completed',
            'quality_rating': 5.5
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.put(url, data, format='json', **headers)
    
        self.assertEqual(response.data['status_code'], 1) 
        self.assertEqual(response.data['status_message'], 'Successfully updated purchase order details.')

    def test_update_po_not_found_failure(self):
        self.create_purchase_order()
        po_number = '1900'
        url = reverse('vendor:modify-purchase-order-view', kwargs={'po_id': po_number})
        data = {
            'status': 'completed',
            'quality_rating': 5.5
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.put(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], f'Purchase order with {po_number} purchase order number does not exists.')

    def test_update_po_already_completed_failure(self):
        po_obj = self.create_completed_purchase_order()
        url = reverse('vendor:modify-purchase-order-view', kwargs={'po_id': po_obj.po_number})
        data = {
            'status': 'completed',
            'quality_rating': 5.5
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.put(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], 'This purchase order was already completed.')

    def test_update_po_already_canceled_failure(self):
        po_obj = self.create_canceled_purchase_order()
        url = reverse('vendor:modify-purchase-order-view', kwargs={'po_id': po_obj.po_number})
        data = {
            'status': 'completed',
            'quality_rating': 5.5
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.put(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], 'This purchase order was canceled; please place a new purhcase order.')

    def test_update_po_with_same_status_failure(self):
        po_obj = self.create_purchase_order()
        url = reverse('vendor:modify-purchase-order-view', kwargs={'po_id': po_obj.po_number})
        data = {
            'status': 'pending'
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.put(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], f'This purchase order is already in {po_obj.status} status.')


class DeletePurchaseOrderTest(BaseAPITestCase, CommonAPITestCase):

    def test_delete_purchase_order_success(self):
        po_obj = self.create_purchase_order()
        url = reverse('vendor:modify-purchase-order-view', kwargs={'po_id': po_obj.po_number})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.delete(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['status_message'], 'Successfully deleted a purchase order.')
        self.assertEqual(response.data['results'], True)

    def test_delete_purchase_order_failure(self):
        self.create_vendor()
        po_id = 1437
        url = reverse('vendor:modify-purchase-order-view', kwargs={'po_id': po_id})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.delete(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1)
        self.assertEqual(response.data['status_message'], f'Purchase order with {po_id} purchase order number does not exists.')


class FetchVendorPerformanceMetricsTest(BaseAPITestCase, CommonAPITestCase):

    def test_fetch_vendor_performance_metrics_success(self):
        vendor_obj = self.create_bulk_vendor_purchase_order()
        url = reverse('vendor:vendor-performance-metrics-view', kwargs={'vendor_id': vendor_obj.vendor_code})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['status_message'], 'Successfully fetched vendor performance metrics details.')

    def test_fetch_vendor_performance_metrics_failure(self):
        self.create_bulk_vendor_purchase_order()
        vendor_code = '1900'
        url = reverse('vendor:vendor-performance-metrics-view', kwargs={'vendor_id': vendor_code})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(url, format='json', **headers)
        
        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], f'Vendor with {vendor_code} vendor code does not exists.')


class UpdateAcknowledgePurchaseOrderTest(BaseAPITestCase, CommonAPITestCase):

    def test_update_vendor_acknowledge_po_success(self):
        po_obj = self.create_purchase_order()
        url = reverse('vendor:acknowledge-purchase-order-view', kwargs={'po_id': po_obj.po_number})
        data = {
            "acknowledgment_date": datetime.now()
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], 1) 
        self.assertEqual(response.data['status_message'], 'Vendor successfully acknowledged a purchase order.')

    def test_update_vendor_acknowledge_po_failure(self):
        self.create_purchase_order()
        po_number = '1900'
        url = reverse('vendor:acknowledge-purchase-order-view', kwargs={'po_id': po_number})
        data = {
            "acknowledgment_date": datetime.now()
        }
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.data['status_code'], -1) 
        self.assertEqual(response.data['status_message'], f'Purchase order with {po_number} purchase order number does not exists.')    