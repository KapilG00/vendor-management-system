from  datetime import datetime
from vendor.models import Vendor, PurchaseOrder
from vendor.serializers import PurchaseOrderSerializer
from common.custom_exceptions import CustomExceptions


class PurchaseOrderHelper:
    """
    A helper class for managing purchase order-related operations, including CRUD operations,
    vendor-specific retrieval, and acknowledgment.

    Methods:
        __init__(self):
            Initialize an instance of the PurchaseOrderHelper.
    """        

    def __init__(self):
        pass

    def get_vendor_purchase_orders(self, vendor_code):
        """
        Retrieve a list of purchase orders for a specific vendor or all purchase orders if vendor_code is None.

        Parameters:
            vendor_code (str): The unique code identifying the vendor.

        Returns:
            list: A list of serialized purchase order data.

        Raises:
            CustomExceptions: If no purchase orders are found.

        """
        try:
            if vendor_code is not None:
                try:
                    vendor_obj = Vendor.objects.get(vendor_code=vendor_code)
                    purchase_orders_list = PurchaseOrder.objects.filter(vendor=vendor_obj)
                except Vendor.DoesNotExist:
                    raise CustomExceptions(f'Vendor with {vendor_code} vendor code does not exists.') 
            else:
                purchase_orders_list = PurchaseOrder.objects.all()
            if not purchase_orders_list.exists():
                raise CustomExceptions('No purchase orders found; please place an order first.')
            else:
                purchase_orders_serialized_list = PurchaseOrderSerializer.get_Serialized_JSON(purchase_orders_list)
        except Exception as e:
            raise CustomExceptions(str(e))

        return purchase_orders_serialized_list

    def get_purchase_order(self, po_number):
        """
        Retrieve details of a specific purchase order based on the purchase order number.

        Parameters:
            po_number (str): The unique number identifying the purchase order.

        Returns:
            dict: Serialized data of the requested purchase order.

        Raises:
            CustomExceptions: If the purchase order with the specified number does not exist.

        """
        try:
            purchase_order_obj = PurchaseOrder.objects.get(po_number=po_number)
            purchase_order_serialized_data = PurchaseOrderSerializer.get_Serialized_JSON(purchase_order_obj)
        except PurchaseOrder.DoesNotExist:
            raise CustomExceptions(f'Purchase order with {po_number} purchase order number does not exists.')
        except Exception as e:
            raise CustomExceptions(str(e))
        
        return purchase_order_serialized_data

    def create_purchase_order(self, order_data):
        """
        Create a new purchase order based on the provided data.

        Parameters:
            order_data (dict): A dictionary containing purchase order details.
                Required keys: 'items', 'po_number', 'vendor_code'.

        Returns:
            dict: Serialized data of the created purchase order.

        Raises:
            CustomExceptions: If an error occurs during purchase order creation.

        """
        items = order_data.get('items')
        quantity = len(items)
        po_number = order_data.get('po_number').lstrip()
        vendor_code = order_data.get('vendor_code').lstrip()
        try:
            try:
                vendor_obj = Vendor.objects.get(vendor_code=vendor_code)
            except Vendor.DoesNotExist:
                raise CustomExceptions(f'Vendor with {vendor_code} vendor code does not exists.')     
            purchase_order_obj = PurchaseOrder.objects.create(vendor=vendor_obj, po_number=po_number, items=items, quantity=quantity)
            purchase_order_serialized_data = PurchaseOrderSerializer.get_Serialized_JSON(purchase_order_obj)
            return purchase_order_serialized_data
        except Exception as e:
            raise CustomExceptions(str(e))

    def update_purchase_order(self, po_number, order_data):
        """
        Update details of an existing purchase order based on the provided data.

        Parameters:
            po_number (str): The unique number identifying the purchase order to be updated.
            order_data (dict): A dictionary containing updated purchase order details.
                Required keys: 'status', 'quality_rating'.

        Returns:
            dict: Serialized data of the updated purchase order.

        Raises:
            CustomExceptions: If the purchase order with the specified number does not exist or if an error occurs during the update.

        """
        current_status = order_data.get('status')
        quality_rating = order_data.get('quality_rating')
        try:
            purchase_order_obj = PurchaseOrder.objects.get(po_number=po_number)
            # Check if the order was already completed.
            if purchase_order_obj.status == "completed":
                raise CustomExceptions('This purchase order was already completed.')
            
            # Check if the order was already canceled.
            if purchase_order_obj.status == "canceled":
                raise CustomExceptions('This purchase order was canceled; please place a new purhcase order.')
            
            # Check to not letting the vendor to update the PO with same status.
            if purchase_order_obj.status == current_status:
                raise CustomExceptions(f'This purchase order is already in {current_status} status.')

            # Previous status of order.
            purchase_order_obj.prev_status = purchase_order_obj.status
            # Updated status of order.
            purchase_order_obj.status = current_status
            purchase_order_obj.quality_rating = quality_rating

            expected_delivery_date = purchase_order_obj.delivery_date.strftime("%d-%m-%Y, %H:%M:%S")
            actual_delivery_date = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

            # Check for the possible late delivery of purchase order and mark it as delivered late if any.
            if actual_delivery_date > expected_delivery_date:
                purchase_order_obj.is_delivered_late = True
            
            purchase_order_obj.save()

            updated_purchase_order_data = self.get_purchase_order(po_number)    

        except PurchaseOrder.DoesNotExist:
            raise CustomExceptions(f'Purchase order with {po_number} purchase order number does not exists.')
        except Exception as e:
            raise CustomExceptions(str(e))   

        return updated_purchase_order_data

    def delete_purchase_order(self, po_number):
        """
        Delete a purchase order based on the provided purchase order number.

        Parameters:
            po_number (str): The unique number identifying the purchase order to be deleted.

        Returns:
            bool: True if deletion is successful.

        Raises:
            CustomExceptions: If the purchase order with the specified number does not exist.

        """
        success = False
        try:  
            purchase_order_obj = PurchaseOrder.objects.get(po_number=po_number)
            purchase_order_obj.delete()
            success = True
        except PurchaseOrder.DoesNotExist:
            raise CustomExceptions(f'Purchase order with {po_number} purchase order number does not exists.')
        
        return success
    
    def vendor_acknowledge_purchase_order(self, po_number):
        """
        Acknowledge a purchase order as a vendor by updating the acknowledgment date.

        Parameters:
            po_number (str): The unique number identifying the purchase order to be acknowledged.

        Returns:
            dict: Serialized data of the acknowledged purchase order.

        Raises:
            CustomExceptions: If the purchase order with the specified number does not exist or if an error occurs during acknowledgment.

        """
        try:
            purchase_order_obj = PurchaseOrder.objects.get(po_number=po_number)
            purchase_order_obj.acknowledgment_date = datetime.now()
            purchase_order_obj.save()

            purchase_order_serialized_data = PurchaseOrderSerializer.get_Serialized_JSON(purchase_order_obj)
            return purchase_order_serialized_data
        except PurchaseOrder.DoesNotExist:
            raise CustomExceptions(f'Purchase order with {po_number} purchase order number does not exists.')
        except Exception as e:
            raise CustomExceptions(str(e))