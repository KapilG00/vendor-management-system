from django.urls import path
import vendor.rest_views as rest_views

urlpatterns = [
    path('vendors/', rest_views.VendorView.as_view(), name='vendor-view'),
    path('vendors/<int:vendor_id>/', rest_views.VendorView.as_view(), name='modify-vendor-view'),
    path('vendors/<int:vendor_id>/performance/', rest_views.VendorPerformanceView.as_view(), name='vendor-performance-metrics-view'),
    path('purchase_orders/', rest_views.VendorPurchaseOrderView.as_view(), name='vendor-purchase-order-view'),
    path('purchase_orders/<int:po_id>/', rest_views.PurchaseOrderView.as_view(), name='modify-purchase-order-view'),
    path('purchase_orders/<int:po_id>/acknowledge/', rest_views.AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order-view'),  
]