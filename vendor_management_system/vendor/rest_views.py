from rest_framework.views import APIView
from common.helpers.rest_api_helpers import ResultBuilder
from common.custom_exceptions import CustomExceptions, CustomFormErrorExceptions
from .helpers.vendor_helpers import VendorHelper
from .helpers.purchase_orders_helpers import PurchaseOrderHelper
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class VendorView(APIView):
    """
    API View for managing vendor operations.

    Attributes:
        authentication_classes (list): A list of authentication classes, including JWTAuthentication.
        permission_classes (list): A list of permission classes, including IsAuthenticated.
    Methods:
        get(self, request, *args, **kwargs):
            Get method to retrieve vendor details or a list of vendors.

        post(self, request, *args, **kwargs):
            Post method to create a new vendor.

        put(self, request, *args, **kwargs):
            Put method to update the details of an existing vendor.

        delete(self, request, *args, **kwargs):
            Delete method to remove a vendor.

    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve details for a specific vendor or a list of all vendors.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs:
                vendor_id (str, optional): The unique identifier of the vendor to retrieve details for.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 200 OK: Successful retrieval of vendor information.
                - 404 Not Found: Vendor not found.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully fetched vendors list.",
                "results": [
                    {
                        "vendor_uuid": "f6f637d6-9507-4983-8c99-eb14dcc2cfa9",
                        "name": "vendor1",
                        "contact_details": "kapil123@gmail.com",
                        "address": "This is vendor1 address.",
                        "vendor_code": "128",
                        "on_time_delivery_rate": 75.0,
                        "quality_rating_avg": 5.83,
                        "average_response_time": 403.97,
                        "fulfillment_rate": 1.0
                    },
                    {
                        "vendor_uuid": "7031e49f-fb78-4af9-a669-8e3252246d9d",
                        "name": "vendor2",
                        "contact_details": "kapilasd@gmail.com",
                        "address": "This is vendor2 address.",
                        "vendor_code": "131",
                        "on_time_delivery_rate": 0.0,
                        "quality_rating_avg": 0.0,
                        "average_response_time": 0.0,
                        "fulfillment_rate": 0.0
                    }
                ]
            }        

        """
        vendor_code = kwargs.get('vendor_id')
        try:
            if vendor_code:
                temp_resp = VendorHelper().get_vendor(vendor_code)
                response_object = ResultBuilder().success().message("Successfully fetched vendor details.").result_object(temp_resp).get_response_rest()
            else:
                temp_resp = VendorHelper().get_all_vendors()
                response_object = ResultBuilder().success().message("Successfully fetched vendors list.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new vendor.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs: Not used.

        Request Data:
            - vendor_data (dict): A dictionary containing the new vendor information.    

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 201 Created: Vendor successfully created.
                - 400 Bad Request: Invalid request data.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Request Data Format:
            {
                "name": "vendor3",
                "contact_details": "kapilasd90@gmail.com",
                "address": "This is vendor3 address.",
                "vendor_code": "199"
            }    

        Response Format:    
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully created a vendor.",
                "results": {
                    "vendor_uuid": "8db7a0e77e9b4963a906471413ce8b00",
                    "name": "vendor3",
                    "contact_details": "kapilasd90@gmail.com",
                    "address": "This is vendor3 address.",
                    "vendor_code": "199",
                    "on_time_delivery_rate": 0.0,
                    "quality_rating_avg": 0.0,
                    "average_response_time": 0.0,
                    "fulfillment_rate": 0.0
                }
            }    

        """
        vendor_data = request.data
        try:
            temp_resp = VendorHelper().create_vendor(vendor_data)
            response_object = ResultBuilder().success().message("Successfully created a vendor.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object
    
    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests to update details for a specific vendor.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs:
                vendor_id (str): The unique identifier of the vendor to update.

        Request Data:
            - vendor_data (dict): A dictionary containing the updated vendor information.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 200 OK: Successful update of vendor information.
                - 400 Bad Request: Invalid request data.
                - 404 Not Found: Vendor not found.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Request Data Format:
            {
                "name": "new vendor3",
                "contact_details": "9090122345",
                "address": "This is vendor 3 new address."
            }

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully updated vendor details.",
                "results": {
                    "vendor_uuid": "8db7a0e7-7e9b-4963-a906-471413ce8b00",
                    "name": "new vendor3",
                    "contact_details": "9090122345",
                    "address": "This is vendor 3 new address.",
                    "vendor_code": "199",
                    "on_time_delivery_rate": 0.0,
                    "quality_rating_avg": 0.0,
                    "average_response_time": 0.0,
                    "fulfillment_rate": 0.0
                }
            }

        """
        vendor_code = kwargs.get('vendor_id')
        vendor_data = request.data
        try:
            temp_resp = VendorHelper().update_vendor(vendor_code, vendor_data)
            response_object = ResultBuilder().success().message("Successfully updated vendor details.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object
    
    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to delete a specific vendor.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs:
                vendor_id (str): The unique identifier of the vendor to delete.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 204 No Content: Vendor successfully deleted.
                - 404 Not Found: Vendor not found.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomExceptions: For custom exceptions.

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully deleted a vendor.",
                "results": true
            }

        """
        vendor_code = kwargs.get('vendor_id')
        try:
            temp_resp = VendorHelper().delete_vendor(vendor_code)
            response_object = ResultBuilder().success().message("Successfully deleted a vendor.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object


class VendorPurchaseOrderView(APIView):
    """
    A class representing API views for managing purchase orders related to a vendor.

    This view allows the retrieval and creation of purchase orders associated with a specific vendor.

    Attributes:
        authentication_classes (list): A list of authentication classes, including JWTAuthentication.
        permission_classes (list): A list of permission classes, including IsAuthenticated.

    Methods:
        get(self, request, *args, **kwargs):
            Get method to retrieve all purchase order details of a particular vendor or of all vendors.

        post(self, request, *args, **kwargs):
            Post method to create a new purchase order.

    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve purchase orders for a specific vendor.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs:
                vendor_id (str, optional): The unique identifier of the vendor to retrieve purchase orders for.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 200 OK: Successful retrieval of purchase orders.
                - 404 Not Found: Vendor not found or no purchase orders for the vendor.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully fetched all purchase orders details.",
                "results": [
                    {
                        "po_uuid": "a675a073-b52e-49f0-bbf7-c3338049ca19",
                        "order_date": "13-12-2023, 11:15:22",
                        "delivery_date": "12-12-2023, 12:00:00",
                        "issue_date": "13-12-2023, 11:15:22",
                        "acknowledgment_date": null,
                        "po_number": "1010",
                        "items": {
                            "item1": 2800
                        },
                        "quantity": 1,
                        "status": "completed",
                        "prev_status": "completed",
                        "quality_rating": null,
                        "is_delivered_late": true,
                        "vendor": "f6f637d6-9507-4983-8c99-eb14dcc2cfa9"
                    },
                    # Additional purchase orders...
                ]
            }

        """
        vendor_code = request.GET.get('vendor_id', None)
        try:
            temp_resp = PurchaseOrderHelper().get_vendor_purchase_orders(vendor_code)
            response_object = ResultBuilder().success().message("Successfully fetched all purchase orders details.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new purchase order for a specific vendor.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs: Not used.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 201 Created: Purchase order successfully created.
                - 400 Bad Request: Invalid request data.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Request Data Format:
            {
                "items": {
                    "Nike t-shirt": 3200
                },
                "po_number": "1222",
                "vendor_code": "131"
            }

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully created a purchase order.",
                "results": {
                    "po_uuid": "4c6b778941034d399cb27ee1ba69e37d",
                    "order_date": "13-12-2023, 13:43:57",
                    "delivery_date": "14-12-2023, 13:38:21",
                    "issue_date": "13-12-2023, 13:43:57",
                    "acknowledgment_date": null,
                    "po_number": "1222",
                    "items": {
                        "Nike t-shirt": 3200
                    },
                    "quantity": 1,
                    "status": "pending",
                    "prev_status": null,
                    "quality_rating": null,
                    "is_delivered_late": false,
                    "vendor": "7031e49f-fb78-4af9-a669-8e3252246d9d"
                }
            }
        """
        order_data = request.data
        try:
            temp_resp = PurchaseOrderHelper().create_purchase_order(order_data)
            response_object = ResultBuilder().success().message("Successfully created a purchase order.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object
    
    
class PurchaseOrderView(APIView):
    """
    A class representing API views for managing purchase orders.

    This view allows the retrieval, updating, and deletion of purchase orders.

    Attributes:
        authentication_classes (list): A list of authentication classes, including JWTAuthentication.
        permission_classes (list): A list of permission classes, including IsAuthenticated.

    Methods:
        get(self, request, *args, **kwargs):
            Get method to retrieve particular purchase order details.

        put(self, request, *args, **kwargs):
            Put method to update the details of an existing purchase order (can be updated by vendor or customer).

        delete(self, request, *args, **kwargs):
            Delete method to remove a purchase order.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve details for a specific purchase order.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs:
                po_id (str): The unique identifier of the purchase order to retrieve details for.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 200 OK: Successful retrieval of purchase order details.
                - 404 Not Found: Purchase order not found.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully fetched purchase order details.",
                "results": {
                    "po_uuid": "a675a073-b52e-49f0-bbf7-c3338049ca19",
                    "order_date": "13-12-2023, 11:15:22",
                    "delivery_date": "12-12-2023, 12:00:00",
                    "issue_date": "13-12-2023, 11:15:22",
                    "acknowledgment_date": null,
                    "po_number": "1010",
                    "items": {
                        "VIP briefcase": 2800
                    },
                    "quantity": 1,
                    "status": "completed",
                    "prev_status": "completed",
                    "quality_rating": null,
                    "is_delivered_late": true,
                    "vendor": "f6f637d6-9507-4983-8c99-eb14dcc2cfa9"
                }
            }

        """
        po_number = kwargs.get('po_id')
        try:
            temp_resp = PurchaseOrderHelper().get_purchase_order(po_number)
            response_object = ResultBuilder().success().message("Successfully fetched purchase order details.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object
    
    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests to update details for a specific purchase order.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs:
                po_id (str): The unique identifier of the purchase order to update.

        Request Data:
            - order_data (dict): A dictionary containing the updated purchase order information.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 200 OK: Successful update of purchase order details.
                - 400 Bad Request: Invalid request data.
                - 404 Not Found: Purchase order not found.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Request Data Format:
            {
                "status": "completed"
            }

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully updated purchase order details.",
                "results": {
                    "po_uuid": "53e444dc-3dff-4daf-b1c1-49ca96de477c",
                    "order_date": "13-12-2023, 13:52:37",
                    "delivery_date": "14-12-2023, 19:20:55",
                    "issue_date": "13-12-2023, 13:52:37",
                    "acknowledgment_date": "13-12-2023, 20:36:35",
                    "po_number": "1221",
                    "items": {
                        "Denim jacket": 3000
                    },
                    "quantity": 1,
                    "status": "completed",
                    "prev_status": "pending",
                    "quality_rating": null,
                    "is_delivered_late": true,
                    "vendor": "f6f637d6-9507-4983-8c99-eb14dcc2cfa9"
                }
            }

        """
        po_number = kwargs.get('po_id')
        order_data = request.data
        try:
            temp_resp = PurchaseOrderHelper().update_purchase_order(po_number, order_data)
            response_object = ResultBuilder().success().message("Successfully updated purchase order details.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object
    
    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to delete a specific purchase order.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs:
                po_id (str): The unique identifier of the purchase order to delete.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 204 No Content: Purchase order successfully deleted.
                - 404 Not Found: Purchase order not found.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomExceptions: For custom exceptions.

        Response Format:    
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully deleted a purchase order.",
                "results": true
            }    

        """
        po_number = kwargs.get('po_id')
        try:
            temp_resp = PurchaseOrderHelper().delete_purchase_order(po_number)
            response_object = ResultBuilder().success().message("Successfully deleted a purchase order.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object


class AcknowledgePurchaseOrderView(APIView):
    """
    A class representing an API view for acknowledging a purchase order by a vendor.

    This view allows a vendor to acknowledge the receipt of a purchase order.

    Attributes:
        authentication_classes (list): A list of authentication classes, including JWTAuthentication.
        permission_classes (list): A list of permission classes, including IsAuthenticated.

    Methods:
        post(self, request, *args, **kwargs):
                Post method for vendor to update purchase order by acknowledgment.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to acknowledge a specific purchase order by a vendor.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs:
                po_id (str): The unique identifier of the purchase order to acknowledge.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 200 OK: Vendor successfully acknowledged the purchase order.
                - 400 Bad Request: Invalid request data.
                - 404 Not Found: Purchase order not found or cannot be acknowledged.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Vendor successfully acknowledged a purchase order.",
                "results": {
                    "po_uuid": "999e3444-e1f5-46c1-9fa1-4c0b97cd45dc",
                    "order_date": "12-12-2023, 10:19:44",
                    "delivery_date": "14-12-2023, 15:49:40",
                    "issue_date": "12-12-2023, 10:19:44",
                    "acknowledgment_date": "13-12-2023, 14:06:54",
                    "po_number": "1050",
                    "items": {
                        "cricket kit set": 15000
                    },
                    "quantity": 1,
                    "status": "completed",
                    "prev_status": "",
                    "quality_rating": null,
                    "is_delivered_late": false,
                    "vendor": "f6f637d6-9507-4983-8c99-eb14dcc2cfa9"
                }
            }

        """
        po_number = kwargs.get('po_id')
        try:
            temp_resp = PurchaseOrderHelper().vendor_acknowledge_purchase_order(po_number)
            response_object = ResultBuilder().success().message("Vendor successfully acknowledged a purchase order.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object


class VendorPerformanceView(APIView):
    """
    A class representing an API view for retrieving performance metrics for a specific vendor.

    This view allows the retrieval of performance metrics for a vendor based on their unique identifier.

    Attributes:
        authentication_classes (list): A list of authentication classes, including JWTAuthentication.
        permission_classes (list): A list of permission classes, including IsAuthenticated.

    Methods:
        get(self, request, *args, **kwargs):
                Get method to retrieve particular vendor performance metrics details.

    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve performance metrics for a specific vendor.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs:
                vendor_id (str): The unique identifier of the vendor to retrieve performance metrics for.

        Returns:
            Response: A JSON response with the result of the operation.
            Possible status codes:
                - 200 OK: Successful retrieval of vendor performance metrics.
                - 404 Not Found: Vendor not found or no performance metrics available.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Successfully fetched vendor performance metrics details.",
                "results": {
                    "vendor_name": "vendor1",
                    "vendor_code": "128",
                    "on_time_delivery_rate": 100.0,
                    "quality_rating_average": 2.1,
                    "average_response_time": 403.97,
                    "fulfillment_rate": 100.0
                }
            }
        """
        vendor_code = kwargs.get('vendor_id')
        try:
            temp_resp = VendorHelper().get_vendor_performance(vendor_code)
            response_object = ResultBuilder().success().message("Successfully fetched vendor performance metrics details.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object