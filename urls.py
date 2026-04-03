from django.contrib import admin
from django.urls import path, include
from invoices.views.invoice_pdf import invoice_pdf_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/', include('accounts.urls')),
    path("api/invoices/", include("invoices.urls")),
    path('invoice/<int:invoice_id>/pdf/', invoice_pdf_view),
]
