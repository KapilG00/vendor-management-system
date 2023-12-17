import math
from django.db.models import Avg, fields, F, ExpressionWrapper
from vendor.models import PurchaseOrder


def update_on_time_delivery_rate(instance):
    """
    Update the on-time delivery rate of the vendor when a purchase order is marked as 'completed'.

    Parameters:
        instance (PurchaseOrder): The instance of the completed purchase order.

    """
    if instance.status == 'completed':
        vendor_completed_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
        on_time_deliveries = vendor_completed_pos.filter(is_delivered_late=False).count()
        total_completed_pos = vendor_completed_pos.count()

        if total_completed_pos > 0:
            on_time_delivery_rate = math.ceil((on_time_deliveries/total_completed_pos)*100)/100  # round-off to 2 decimal places.
            instance.vendor.on_time_delivery_rate = on_time_delivery_rate*100
            instance.vendor.save()    

def update_quality_rating_avg(instance):
    """
    Update the average quality rating of the vendor when a purchase order is marked as 'completed'
    and has a quality rating.

    Parameters:
        instance (PurchaseOrder): The instance of the completed purchase order.

    """
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor_completed_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
        average_quality_rating = vendor_completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']
        
        instance.vendor.quality_rating_avg = average_quality_rating
        instance.vendor.save()

def update_avg_response_time(instance):
    """
    Update the average response time of the vendor when a purchase order is acknowledged.

    Parameters:
        instance (PurchaseOrder): The instance of the acknowledged purchase order.

    """
    if instance.acknowledgment_date and instance.status == 'pending':
        vendor_pos = PurchaseOrder.objects.filter(vendor=instance.vendor)
        average_response_time = vendor_pos.annotate(response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'),
                                                                                    output_field=fields.DurationField())).aggregate(
                                                                                        Avg('response_time'))['response_time__avg']
        average_response_time_in_minutes = average_response_time.total_seconds()/60
        instance.vendor.average_response_time = math.ceil(average_response_time_in_minutes*100)/100  # round-off to 2 decimal places.
        instance.vendor.save()

def update_fulfillment_rate(instance):
    """
    Update the fulfillment rate of the vendor when the status of a purchase order changes.

    Parameters:
        instance (PurchaseOrder): The instance of the purchase order with a status change.

    """
    if instance.status != instance.prev_status:
        vendor_pos = PurchaseOrder.objects.filter(vendor=instance.vendor)
        total_pos = vendor_pos.count()
        successful_fulfillments = vendor_pos.filter(status='completed').count() 

        if total_pos > 0:
            fulfillment_rate = math.ceil((successful_fulfillments/total_pos)*100)/100  # round-off to 2 decimal places.
            instance.vendor.fulfillment_rate = fulfillment_rate * 100
            instance.vendor.save()