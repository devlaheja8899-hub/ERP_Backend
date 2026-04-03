from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Customer, Company
from .serializers import CustomerSerializer, CompanySerializer
from core.response_handler import APIResponse


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Customer validation failed"
                )
            self.perform_create(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Customer created successfully",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to create customer",
                error_details=str(e)
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return APIResponse.success(
                data=serializer.data,
                message="Customers retrieved successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to retrieve customers",
                error_details=str(e)
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return APIResponse.success(
                data=serializer.data,
                message="Customer retrieved successfully"
            )
        except Exception as e:
            return APIResponse.not_found(message="Customer not found")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Customer validation failed"
                )
            self.perform_update(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Customer updated successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to update customer",
                error_details=str(e)
            )

    def destroy(self, request, *args, **kwargs):
        try:
            self.perform_destroy(self.get_object())
            return APIResponse.success(
                data=None,
                message="Customer deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return APIResponse.not_found(message="Customer not found")


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Company validation failed"
                )
            self.perform_create(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Company created successfully",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to create company",
                error_details=str(e)
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return APIResponse.success(
                data=serializer.data,
                message="Companies retrieved successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to retrieve companies",
                error_details=str(e)
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return APIResponse.success(
                data=serializer.data,
                message="Company retrieved successfully"
            )
        except Exception as e:
            return APIResponse.not_found(message="Company not found")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Company validation failed"
                )
            self.perform_update(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Company updated successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to update company",
                error_details=str(e)
            )

    def destroy(self, request, *args, **kwargs):
        try:
            self.perform_destroy(self.get_object())
            return APIResponse.success(
                data=None,
                message="Company deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return APIResponse.not_found(message="Company not found")