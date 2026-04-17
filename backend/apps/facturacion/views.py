from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Max
from django.utils import timezone
from .models import Comprobante, DetalleComprobante, HistorialEnvio
from .serializers import ComprobanteSerializer, HistorialEnvioSerializer


class ComprobanteViewSet(viewsets.ModelViewSet):
    serializer_class = ComprobanteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['tipo_documento', 'estado', 'fecha_emision']
    
    def get_queryset(self):
        return Comprobante.objects.filter(empresa=self.request.user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)
    
    @action(detail=True, methods=['post'])
    def generar(self, request, pk=None):
        comprobante = self.get_object()
        if comprobante.estado != 'borrador':
            return Response({'error': 'Solo se pueden generar comprobantes en estado borrador'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        from apps.facturacion.services import GenerarComprobanteService
        servicio = GenerarComprobanteService(comprobante)
        result = servicio.generar()
        
        if result['success']:
            comprobante.estado = 'generado'
            comprobante.save()
        
        return Response(result)
    
    @action(detail=True, methods=['post'])
    def firmar(self, request, pk=None):
        comprobante = self.get_object()
        if comprobante.estado != 'generado':
            return Response({'error': 'El comprobante debe estar generado'}, status=status.HTTP_400_BAD_REQUEST)
        
        from apps.facturacion.services import FirmarComprobanteService
        servicio = FirmarComprobanteService(comprobante)
        result = servicio.firmar(empresa=request.user.empresa)
        
        if result['success']:
            comprobante.estado = 'firmado'
            comprobante.hash_cpe = result.get('hash')
            comprobante.xml_firmado = result.get('xml')
            comprobante.save()
        
        return Response(result)
    
    @action(detail=True, methods=['post'])
    def enviar_sunat(self, request, pk=None):
        comprobante = self.get_object()
        if not request.user.empresa.ose_enabled:
            return Response({'error': 'Empresa no tiene OSE configurado'}, status=status.HTTP_400_BAD_REQUEST)
        
        from apps.facturacion.services import EnviarSunatService
        servicio = EnviarSunatService(comprobante)
        result = servicio.enviar()
        
        HistorialEnvio.objects.create(
            comprobante=comprobante,
            tipo='sunat',
            request_data=result.get('request'),
            response_data=result.get('response'),
            estado=result.get('estado', 'error'),
            mensaje=result.get('mensaje', '')
        )
        
        if result['success']:
            comprobante.estado = 'enviado'
            comprobante.cdr_sunat = result.get('cdr', '')
            comprobante.codigo_respuesta = result.get('codigo', '')
            comprobante.descripcion_respuesta = result.get('descripcion', '')
            comprobante.save()
        
        return Response(result)
    
    @action(detail=True, methods=['get'])
    def obtener_pdf(self, request, pk=None):
        comprobante = self.get_object()
        
        if not comprobante.pdf_url:
            from apps.facturacion.services import GenerarPdfService
            servicio = GenerarPdfService(comprobante)
            result = servicio.generar()
            if result['success']:
                comprobante.pdf_url = result['url']
                comprobante.save()
                return Response(result)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'url': comprobante.pdf_url})
    
    @action(detail=True, methods=['post'])
    def anular(self, request, pk=None):
        comprobante = self.get_object()
        if comprobante.estado not in ['aceptado', 'enviado']:
            return Response({'error': 'Solo se pueden anular comprobantes aceptados o enviados'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        comprobante.estado = 'anulado'
        comprobante.save()
        
        return Response(ComprobanteSerializer(comprobante).data)
    
    @action(detail=False, methods=['get'])
    def resumen(self, request):
        empresa = request.user.empresa
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')
        
        queryset = self.get_queryset()
        if desde and hasta:
            queryset = queryset.filter(fecha_emision__range=[desde, hasta])
        
        return Response({
            'total': queryset.count(),
            'generados': queryset.filter(estado='generado').count(),
            'enviados': queryset.filter(estado='enviado').count(),
            'aceptados': queryset.filter(estado='aceptado').count(),
            'anulados': queryset.filter(estado='anulado').count(),
            'total_venta': queryset.filter(estado='aceptado').aggregate(total=models.Sum('importe_total'))['total'] or 0,
        })