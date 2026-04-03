from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    """Standardized API Response Handler for all endpoints"""
    
    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK):
        """Return standardized success response"""
        return Response(
            {
                'success': True,
                'status_code': status_code,
                'message': message,
                'data': data,
                'error': None,
            },
            status=status_code
        )

    @staticmethod
    def error(message="Error", error_details=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Return standardized error response"""
        return Response(
            {
                'success': False,
                'status_code': status_code,
                'message': message,
                'data': None,
                'error': error_details,
            },
            status=status_code
        )

    @staticmethod
    def validation_error(errors, message="Validation failed"):
        """Return validation error response"""
        return Response(
            {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': message,
                'data': None,
                'error': errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def unauthorized(message="Authentication required"):
        """Return 401 Unauthorized response"""
        return Response(
            {
                'success': False,
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': message,
                'data': None,
                'error': 'Unauthorized',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def forbidden(message="Permission denied"):
        """Return 403 Forbidden response"""
        return Response(
            {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': message,
                'data': None,
                'error': 'Forbidden',
            },
            status=status.HTTP_403_FORBIDDEN
        )

    @staticmethod
    def not_found(message="Resource not found"):
        """Return 404 Not Found response"""
        return Response(
            {
                'success': False,
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': message,
                'data': None,
                'error': 'Not Found',
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @staticmethod
    def server_error(message="Internal server error", error_details=None):
        """Return 500 Server Error response"""
        return Response(
            {
                'success': False,
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': message,
                'data': None,
                'error': error_details,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
