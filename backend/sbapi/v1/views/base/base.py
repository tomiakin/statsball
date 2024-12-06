from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

class BaseViewSet(viewsets.ReadOnlyModelViewSet):
    """Base ViewSet adding success wrapper and lookup field configuration"""
    
    # Use match_id/competition_id instead of pk where appropriate
    lookup_field = 'pk'  # Override in child classes if needed
    
    def get_object(self):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup_value = self.kwargs.get(lookup_url_kwarg) or self.kwargs.get('pk')
            
            if not lookup_value:
                return None
                
            filter_kwargs = {self.lookup_field: lookup_value}
            obj = queryset.get(**filter_kwargs)
            
            self.check_object_permissions(self.request, obj)
            return obj
        except (self.queryset.model.DoesNotExist, ValidationError):
            raise NotFound(f"{self.queryset.model.__name__} not found")
        except Exception as e:
            raise ValidationError(f"Error retrieving object: {str(e)}")

    def get_response(self, data):
        """Wrap response in success format"""
        if isinstance(data, list) or (isinstance(data, dict) and 'results' in data):
            return Response({
                'status': 'success',
                'data': data,
                'message': None
            })
        return Response(data)  # Individual objects already wrapped by serializer
        
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return self.get_response(response.data)
        
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self.get_response(response.data)