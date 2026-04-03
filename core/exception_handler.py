from rest_framework.views import exception_handler
from rest_framework import status
from core.response_handler import APIResponse


def custom_exception_handler(exc, context):
    """
    Custom exception handler to format all DRF exceptions
    to match the standard API response structure
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        # Get the exception status code
        status_code = response.status_code
        
        # Get the detail message
        detail = response.data.get('detail', 'An error occurred')
        
        # Map common status codes to appropriate messages
        if status_code == 401:
            return APIResponse.unauthorized(message=str(detail))
        elif status_code == 403:
            return APIResponse.forbidden(message=str(detail))
        elif status_code == 404:
            return APIResponse.not_found(message=str(detail))
        elif status_code == 400:
            # For validation errors, return formatted error response
            errors = response.data
            return APIResponse.validation_error(
                errors=errors,
                message="Validation failed"
            )
        elif status_code == 500:
            return APIResponse.server_error(
                message="Internal server error",
                error_details=str(detail)
            )
        else:
            # For any other error
            return APIResponse.error(
                message=str(detail),
                status_code=status_code
            )
    
    return response
