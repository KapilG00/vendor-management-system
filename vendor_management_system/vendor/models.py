import uuid
from datetime import datetime, timedelta
from django.db import models
from common.models import CommonModel
from django.contrib.auth import get_user_model
User = get_user_model()


class Vendor(CommonModel):
    """
    Vendor Model.
    """
    vendor_uuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=20)
    contact_details = models.TextField()
    address =  models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True, db_index=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk:
            self.vendor_uuid = uuid.uuid4().hex
        super(Vendor, self).save(*args, **kwargs)


class PurchaseOrder(CommonModel):
    """
    Purchase Order Model.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_uuid = models.UUIDField(primary_key=True, editable=False)
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, related_name="purchase_order_vendor", on_delete=models.CASCADE, db_index=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(default=datetime.now()+timedelta(days=1))
    items = models.JSONField()
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    prev_status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True, db_index=True)
    is_delivered_late = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f'{self.vendor.name} - {self.po_number}'
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk:
            self.po_uuid = uuid.uuid4().hex
        super(PurchaseOrder, self).save(*args, **kwargs)


class PerformanceHistory(CommonModel):
    """
    Performance History Model.
    """
    ph_uuid = models.UUIDField(primary_key=True, editable=False)
    vendor = models.ForeignKey(Vendor, related_name="performance_history_vendor", on_delete=models.CASCADE, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.vendor.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk:
            self.ph_uuid = uuid.uuid4().hex
        super(PerformanceHistory, self).save(*args, **kwargs)