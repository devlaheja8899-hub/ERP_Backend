from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from core.response_handler import APIResponse


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view with standardized response"""
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                return APIResponse.success(
                    data={
                        'access': response.data.get('access'),
                        'refresh': response.data.get('refresh'),
                    },
                    message="Login successful",
                    status_code=status.HTTP_200_OK
                )
            else:
                return APIResponse.error(
                    message="Invalid credentials",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return APIResponse.error(
                message="Authentication failed",
                error_details=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view with standardized response"""
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                return APIResponse.success(
                    data={
                        'access': response.data.get('access'),
                    },
                    message="Token refreshed successfully",
                    status_code=status.HTTP_200_OK
                )
            else:
                return APIResponse.error(
                    message="Invalid refresh token",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return APIResponse.error(
                message="Token refresh failed",
                error_details=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
