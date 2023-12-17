import json
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Vendor model.

    This serializer is used to convert Vendor model instances into JSON data
    and exclude specific fields such as 'created_by', 'deleted_by', 'modified_by', 'is_deleted',
    'created_date', 'deleted_date', 'modified_date' during serialization.

    Attributes:
        Meta (class): Inner class specifying the metadata for the serializer.

    Methods:
        get_Serialized_JSON(obj): Static method to serialize Vendor model instances into JSON data.
    """
    class Meta:
        model = Vendor
        exclude = ['created_by', 'deleted_by', 'modified_by', 'is_deleted', 'created_date', 'deleted_date', 'modified_date']
        
    @staticmethod
    def get_Serialized_JSON(obj):
        """
        Static method to serialize Vendor model instances into JSON data.

        Parameters:
            obj: Vendor model instance or queryset.

        Returns:
            dict: Serialized JSON data.
        """
        try:
            obj.exists()
            serialized_data = VendorSerializer(obj, many=True).data
        except Exception as e:
            serialized_data = VendorSerializer(obj).data    
        return json.loads(JSONRenderer().render(serialized_data))


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
    Serializer class for the PurchaseOrder model.

    This serializer is used to convert PurchaseOrder model instances into JSON data
    and exclude specific fields such as 'created_by', 'deleted_by', 'modified_by', 'is_deleted',
    'created_date', 'deleted_date', 'modified_date' during serialization. It also formats
    date fields (order_date, delivery_date, issue_date, acknowledgment_date) as per the specified format.

    Attributes:
        order_date (DateTimeField): DateTimeField for the order date.
        delivery_date (DateTimeField): DateTimeField for the delivery date.
        issue_date (DateTimeField): DateTimeField for the issue date.
        acknowledgment_date (DateTimeField): DateTimeField for the acknowledgment date.
        Meta (class): Inner class specifying the metadata for the serializer.

    Methods:
        get_Serialized_JSON(obj): Static method to serialize PurchaseOrder model instances into JSON data.
    """
    order_date = serializers.DateTimeField(format="%d-%m-%Y, %H:%M:%S")
    delivery_date = serializers.DateTimeField(format="%d-%m-%Y, %H:%M:%S")
    issue_date = serializers.DateTimeField(format="%d-%m-%Y, %H:%M:%S")
    acknowledgment_date = serializers.DateTimeField(format="%d-%m-%Y, %H:%M:%S")

    class Meta:
        model = PurchaseOrder
        exclude = ['created_by', 'deleted_by', 'modified_by', 'is_deleted', 'created_date', 'deleted_date', 'modified_date']

    @staticmethod
    def get_Serialized_JSON(obj):
        """
        Static method to serialize PurchaseOrder model instances into JSON data.

        Parameters:
            obj: PurchaseOrder model instance or queryset.

        Returns:
            dict: Serialized JSON data.
        """
        try:
            obj.exists()
            serialized_data = PurchaseOrderSerializer(obj, many=True).data
        except Exception as e:
            serialized_data = PurchaseOrderSerializer(obj).data    
        return json.loads(JSONRenderer().render(serialized_data))