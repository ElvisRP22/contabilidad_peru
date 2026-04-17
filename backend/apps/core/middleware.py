from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        from apps.core.models import Empresa
        
        request.empresa = None
        
        if request.user.is_authenticated and hasattr(request.user, 'empresa'):
            request.empresa = request.user.empresa
        
        tenant_id = request.headers.get('X-Tenant-ID')
        if tenant_id and request.user.is_superuser:
            try:
                request.empresa = Empresa.objects.get(id=tenant_id, activa=True)
            except Empresa.DoesNotExist:
                pass
        
        return None