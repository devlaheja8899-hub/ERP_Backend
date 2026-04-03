from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Quotation, QuotationItem
from .serializers import QuotationSerializer, QuotationItemSerializer
from core.response_handler import APIResponse


class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Quotation validation failed"
                )
            self.perform_create(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Quotation created successfully",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to create quotation",
                error_details=str(e)
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return APIResponse.success(
                data=serializer.data,
                message="Quotations retrieved successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to retrieve quotations",
                error_details=str(e)
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return APIResponse.success(
                data=serializer.data,
                message="Quotation retrieved successfully"
            )
        except Exception as e:
            return APIResponse.not_found(message="Quotation not found")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Quotation validation failed"
                )
            self.perform_update(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Quotation updated successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to update quotation",
                error_details=str(e)
            )

    def destroy(self, request, *args, **kwargs):
        try:
            self.perform_destroy(self.get_object())
            return APIResponse.success(
                data=None,
                message="Quotation deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return APIResponse.not_found(message="Quotation not found")


class QuotationItemViewSet(viewsets.ModelViewSet):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Quotation item validation failed"
                )
            self.perform_create(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Quotation item created successfully",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to create quotation item",
                error_details=str(e)
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return APIResponse.success(
                data=serializer.data,
                message="Quotation items retrieved successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to retrieve quotation items",
                error_details=str(e)
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return APIResponse.success(
                data=serializer.data,
                message="Quotation item retrieved successfully"
            )
        except Exception as e:
            return APIResponse.not_found(message="Quotation item not found")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Quotation item validation failed"
                )
            self.perform_update(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Quotation item updated successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to update quotation item",
                error_details=str(e)
            )

    def destroy(self, request, *args, **kwargs):
        try:
            self.perform_destroy(self.get_object())
            return APIResponse.success(
                data=None,
                message="Quotation item deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return APIResponse.not_found(message="Quotation item not found")