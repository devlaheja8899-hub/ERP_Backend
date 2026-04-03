from django.contrib import admin
from django.urls import path, include
from accounts.custom_views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('api/accounts/', include('accounts.urls')),
    path('api/invoices/', include('invoices.urls')),
    path('api/quotations/', include('quotations.urls')),
]



    
