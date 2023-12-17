from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, PerformanceHistory
from .helpers.signal_helpers import update_on_time_delivery_rate, update_quality_rating_avg, update_fulfillment_rate, update_avg_response_time


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    """
    Signal receiver function to update vendor performance metrics and store the history.

    This function is triggered after a PurchaseOrder instance is saved. It checks if the instance
    is not created (i.e., it's an update), and then updates various performance metrics for the associated vendor.
    It also creates a new entry in the PerformanceHistory model to store historical performance metrics.

    Parameters:
        sender (Type[PurchaseOrder]): The sender class.
        instance (PurchaseOrder): The instance of the PurchaseOrder being saved.
        created (bool): Indicates whether the instance is being created or updated.
        **kwargs: Additional keyword arguments.
    """
    if not created:
        update_on_time_delivery_rate(instance)
        update_quality_rating_avg(instance)
        update_fulfillment_rate(instance)
        update_avg_response_time(instance)  

        PerformanceHistory.objects.create(vendor=instance.vendor, on_time_delivery_rate=instance.vendor.on_time_delivery_rate,
                                          quality_rating_avg=instance.vendor.quality_rating_avg, 
                                          average_response_time=instance.vendor.average_response_time,
                                          fulfillment_rate=instance.vendor.fulfillment_rate)