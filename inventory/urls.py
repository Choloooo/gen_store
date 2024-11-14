# inventory/urls.py

from django.urls import path
from .views import login_view, dashboard, add_item, edit_item, delete_item, scan_barcode, item_list
from django.contrib.auth.views import LogoutView

from inventory import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-item/', add_item, name='add_item'),
    path('edit-item/<int:item_id>/', edit_item, name='edit_item'),
    path('delete-item/<int:item_id>/', delete_item, name='delete_item'),
    path('scan-barcode/', scan_barcode, name='scan_barcode'),
    path('items/', item_list, name='item_list'),  # Add this line to include the item list view
    path('logout/', LogoutView.as_view(), name='logout'),
    path("scan/", views.qr_scanner, name="qr_scanner"),  # Your template view

]
