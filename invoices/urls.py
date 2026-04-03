from django.urls import path
from invoices.views.items import ItemViewSet
from invoices.views.invoice import InvoiceViewSet
from invoices.views.invoice_pdf import invoice_pdf_view

item_list = ItemViewSet.as_view({
    "get": "list",
    "post": "create",
})

item_detail = ItemViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

invoice_list = InvoiceViewSet.as_view({
    "get": "list",
    "post": "create",
})

invoice_detail = InvoiceViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

urlpatterns = [
    path("items/", item_list),
    path("items/<int:pk>/", item_detail),
    path("invoices/", invoice_list),
    path("invoices/<int:pk>/", invoice_detail),
    path("invoices/<int:invoice_id>/pdf/", invoice_pdf_view),
]