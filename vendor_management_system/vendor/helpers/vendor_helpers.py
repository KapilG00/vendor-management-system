from vendor.models import Vendor
from vendor.serializers import VendorSerializer
from common.custom_exceptions import CustomExceptions


class VendorHelper:
    """
    A helper class for managing vendor-related operations, including CRUD operations and performance metrics retrieval.

    Methods:
        __init__(self):
            Initialize an instance of the VendorHelper.
    """        
    def __init__(self):
        pass

    def get_all_vendors(self):
        """
        Retrieve a list of all vendors.

        Returns:
            list: A list of serialized vendor data.

        Raises:
            CustomExceptions: If no vendors are found.

        """
        try:
            vendors_list = Vendor.objects.all()
            if not vendors_list.exists():
                raise CustomExceptions('No vendors found, please create one.')
            vendors_serialized_list = VendorSerializer.get_Serialized_JSON(vendors_list)
        except Exception as e:
            raise CustomExceptions(str(e))

        return vendors_serialized_list
    
    def get_vendor(self, vendor_code):
        """
        Retrieve details of a specific vendor based on the vendor code.

        Parameters:
            vendor_code (str): The unique code identifying the vendor.

        Returns:
            dict: Serialized data of the requested vendor.

        Raises:
            CustomExceptions: If the vendor with the specified code does not exist.

        """
        try:
            vendor_obj = Vendor.objects.get(vendor_code=vendor_code)
            vendors_serialized_data = VendorSerializer.get_Serialized_JSON(vendor_obj)
        except Vendor.DoesNotExist:
            raise CustomExceptions(f'Vendor with {vendor_code} vendor code does not exists.')
        except Exception as e:
            raise CustomExceptions(str(e))

        return vendors_serialized_data

    def create_vendor(self, vendor_data):
        """
        Create a new vendor based on the provided data.

        Parameters:
            vendor_data (dict): A dictionary containing vendor details.
                Required keys: 'name', 'contact_details', 'address', 'vendor_code'.

        Returns:
            dict: Serialized data of the created vendor.

        Raises:
            CustomExceptions: If an error occurs during vendor creation.

        """
        name = vendor_data.get('name').lstrip()
        contact_details = vendor_data.get('contact_details').lstrip()
        address = vendor_data.get('address').lstrip()
        vendor_code = vendor_data.get('vendor_code').lstrip()
        try:
            vendor_data = Vendor.objects.create(name=name, contact_details=contact_details, address=address, vendor_code=vendor_code)
            vendors_serialized_data = VendorSerializer.get_Serialized_JSON(vendor_data)
            return vendors_serialized_data
        except Exception as e:
            raise CustomExceptions(str(e))

    def update_vendor(self, vendor_code, vendor_data):
        """
        Update details of an existing vendor based on the provided data.

        Parameters:
            vendor_code (str): The unique code identifying the vendor to be updated.
            vendor_data (dict): A dictionary containing updated vendor details.
                Required keys: 'name', 'contact_details', 'address'.

        Returns:
            dict: Serialized data of the updated vendor.

        Raises:
            CustomExceptions: If the vendor with the specified code does not exist or if an error occurs during the update.

        """
        name = vendor_data.get('name').lstrip()
        contact_details = vendor_data.get('contact_details').lstrip()
        address = vendor_data.get('address').lstrip()
        try:
            vendor_obj = Vendor.objects.get(vendor_code=vendor_code)
            vendor_obj.name = name
            vendor_obj.contact_details = contact_details
            vendor_obj.address = address
            vendor_obj.save(update_fields=["name", "contact_details", "address"])

            updated_vendor_data = self.get_vendor(vendor_code)
        except Vendor.DoesNotExist:
            raise CustomExceptions(f'Vendor with {vendor_code} vendor code does not exists.')
        except Exception as e:
            raise CustomExceptions(str(e))   

        return updated_vendor_data

    def delete_vendor(self, vendor_code):
        """
        Delete a vendor based on the provided vendor code.

        Parameters:
            vendor_code (str): The unique code identifying the vendor to be deleted.

        Returns:
            bool: True if deletion is successful.

        Raises:
            CustomExceptions: If the vendor with the specified code does not exist.

        """
        success = False
        try:  
            vendor_obj = Vendor.objects.get(vendor_code=vendor_code)
            vendor_obj.delete()
            success = True
        except Vendor.DoesNotExist:
            raise CustomExceptions(f'Vendor with {vendor_code} vendor code does not exists.')
        
        return success
    
    def get_vendor_performance(self, vendor_code):
        """
        Retrieve performance metrics of a specific vendor based on the vendor code.

        Parameters:
            vendor_code (str): The unique code identifying the vendor.

        Returns:
            dict: Performance metrics data for the vendor.

        Raises:
            CustomExceptions: If the vendor with the specified code does not exist.

        """
        try:
            vendor_obj = Vendor.objects.get(vendor_code=vendor_code)
            vendor_performance_resp_dict = {
                "vendor_name": vendor_obj.name,
                "vendor_code": vendor_obj.vendor_code,
                "on_time_delivery_rate": vendor_obj.on_time_delivery_rate,
                "quality_rating_average": vendor_obj.quality_rating_avg,
                "average_response_time": vendor_obj.average_response_time,
                "fulfillment_rate": vendor_obj.fulfillment_rate
            }
        except Vendor.DoesNotExist:
            raise CustomExceptions(f'Vendor with {vendor_code} vendor code does not exists.')
        except Exception as e:
            raise CustomExceptions(str(e))

        return vendor_performance_resp_dict