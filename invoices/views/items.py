from rest_framework import viewsets, status
from rest_framework.response import Response
from invoices.models import Item
from invoices.serializers import ItemSerializer
from core.response_handler import APIResponse


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Item validation failed"
                )
            self.perform_create(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Item created successfully",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to create item",
                error_details=str(e)
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return APIResponse.success(
                data=serializer.data,
                message="Items retrieved successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to retrieve items",
                error_details=str(e)
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return APIResponse.success(
                data=serializer.data,
                message="Item retrieved successfully"
            )
        except Exception as e:
            return APIResponse.not_found(message="Item not found")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if not serializer.is_valid():
                return APIResponse.validation_error(
                    errors=serializer.errors,
                    message="Item validation failed"
                )
            self.perform_update(serializer)
            return APIResponse.success(
                data=serializer.data,
                message="Item updated successfully"
            )
        except Exception as e:
            return APIResponse.server_error(
                message="Failed to update item",
                error_details=str(e)
            )

    def destroy(self, request, *args, **kwargs):
        try:
            self.perform_destroy(self.get_object())
            return APIResponse.success(
                data=None,
                message="Item deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return APIResponse.not_found(message="Item not found")