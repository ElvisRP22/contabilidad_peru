from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Max
from datetime import datetime
from .models import PlanCuenta, Asiento, DetalleAsiento, CentroCosto
from .serializers import PlanCuentaSerializer, AsientoSerializer, CentroCostoSerializer


class PlanCuentaViewSet(viewsets.ModelViewSet):
    serializer_class = PlanCuentaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PlanCuenta.objects.filter(empresa=self.request.user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)


class AsientoViewSet(viewsets.ModelViewSet):
    serializer_class = AsientoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['fecha', 'estado', 'cerrado']
    
    def get_queryset(self):
        qs = Asiento.objects.filter(empresa=self.request.user.empresa)
        fecha_inicio = self.request.query_params.get('fecha_inicio')
        fecha_fin = self.request.query_params.get('fecha_fin')
        if fecha_inicio and fecha_fin:
            qs = qs.filter(fecha__range=[fecha_inicio, fecha_fin])
        return qs.prefetch_related('detalles', 'detalles__cuenta')
    
    def perform_create(self, serializer):
        empresa = self.request.user.empresa
        ultimo = Asiento.objects.filter(empresa=empresa).aggregate(Max('numero'))
        ultimo_num = ultimo['numero__max']
        if ultimo_num:
            try:
                nuevo_num = int(ultimo_num) + 1
            except ValueError:
                nuevo_num = 1
        else:
            nuevo_num = 1
        serializer.save(
            empresa=empresa,
            numero=str(nuevo_num).zfill(6),
            usuario_registra=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        asiento = self.get_object()
        if asiento.cerrado:
            return Response({'error': 'El asiento ya está cerrado'}, status=status.HTTP_400_BAD_REQUEST)
        if not asiento.validar_partida_doble():
            return Response({'error': 'El asiento no está balanceado'}, status=status.HTTP_400_BAD_REQUEST)
        asiento.estado = 'aprobado'
        asiento.usuario_aprueba = request.user
        asiento.fecha_aprueba = datetime.now()
        asiento.save()
        return Response(AsientoSerializer(asiento).data)
    
    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        asiento = self.get_object()
        if asiento.estado != 'aprobado':
            return Response({'error': 'El asiento debe estar aprobado'}, status=status.HTTP_400_BAD_REQUEST)
        asiento.cerrado = True
        asiento.save()
        return Response(AsientoSerializer(asiento).data)


class CentroCostoViewSet(viewsets.ModelViewSet):
    serializer_class = CentroCostoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CentroCosto.objects.filter(empresa=self.request.user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)


class ReporteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def balance_comprobacion(self, request):
        empresa = request.user.empresa
        fecha = request.query_params.get('fecha')
        
        movimientos = DetalleAsiento.objects.filter(
            asiento__empresa=empresa,
            asiento__cerrado=True,
            asiento__fecha__lte=fecha
        ).values('cuenta__codigo', 'cuenta__nombre', 'cuenta__naturaleza').annotate(
            debe_total=Sum('debe'),
            haber_total=Sum('haber')
        ).order_by('cuenta__codigo')
        
        resultado = []
        for m in movimientos:
            saldo = m['debe_total'] - m['haber_total'] if m['cuenta__naturaleza'] == 'deudora' else m['haber_total'] - m['debe_total']
            resultado.append({
                'codigo': m['cuenta__codigo'],
                'nombre': m['cuenta__nombre'],
                'debe': m['debe_total'],
                'haber': m['haber_total'],
                'saldo': saldo,
            })
        
        return Response(resultado)
    
    @action(detail=False, methods=['get'])
    def mayor(self, request):
        empresa = request.user.empresa
        cuenta_id = request.query_params.get('cuenta_id')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        detalles = DetalleAsiento.objects.filter(
            asiento__empresa=empresa,
            asiento__cerrado=True,
            cuenta_id=cuenta_id,
            asiento__fecha__gte=fecha_inicio,
            asiento__fecha__lte=fecha_fin
        ).select_related('asiento').order_by('asiento__fecha', 'asiento__numero')
        
        from .serializers import DetalleAsientoSerializer
        return Response(DetalleAsientoSerializer(detalles, many=True).data)