from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q
from decimal import Decimal
from datetime import datetime, date
from .models import Empleado, Remuneracion, Descuento, BeneficioSocial, Asistencia, Planilla
from .serializers import (
    EmpleadoSerializer, RemuneracionSerializer, DescuentoSerializer,
    BeneficioSocialSerializer, AsistenciaSerializer, PlanillaSerializer
)


class EmpleadoViewSet(viewsets.ModelViewSet):
    serializer_class = EmpleadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['activo', 'area', 'cargo']
    search_fields = ['numero_documento', 'nombres', 'apellido_paterno']
    
    def get_queryset(self):
        return Empleado.objects.filter(empresa=self.request.user.empresa).select_related('empresa')
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        empleados = self.get_queryset().filter(activo=True)
        return Response(EmpleadoSerializer(empleados, many=True).data)


class RemuneracionViewSet(viewsets.ModelViewSet):
    serializer_class = RemuneracionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Remuneracion.objects.filter(empleado__empresa=self.request.user.empresa)
    
    def perform_create(self, serializer):
        empleado = Empleado.objects.get(id=self.request.data.get('empleado'))
        serializer.save(empleado=empleado)


class DescuentoViewSet(viewsets.ModelViewSet):
    serializer_class = DescuentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Descuento.objects.filter(empleado__empresa=self.request.user.empresa)


class BeneficioSocialViewSet(viewsets.ModelViewSet):
    serializer_class = BeneficioSocialSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['tipo', 'estado']
    
    def get_queryset(self):
        return BeneficioSocial.objects.filter(empleado__empresa=self.request.user.empresa)
    
    @action(detail=False, methods=['post'])
    def calcular_cts(self, request):
        empleado_id = request.data.get('empleado_id')
        periodo = request.data.get('periodo')  # YYYY
        
        empleado = Empleado.objects.get(id=empleado_id)
        basico = Decimal('1500.00')
        promedio = Decimal('1600.00')
        tiempo = Decimal('6.00')
        
        monto_cts = (basico + promedio) / 12 * tiempo
        
        beneficio, created = BeneficioSocial.objects.update_or_create(
            empleado=empleado,
            tipo='cts',
            periodo=periodo,
            defaults={
                'tiempo': tiempo,
                'basico': basico,
                'promedio': promedio,
                'monto': monto_cts,
                'estado': 'calculado'
            }
        )
        
        return Response(BeneficioSocialSerializer(beneficio).data)


class AsistenciaViewSet(viewsets.ModelViewSet):
    serializer_class = AsistenciaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['empleado', 'fecha']
    
    def get_queryset(self):
        return Asistencia.objects.filter(empresa=self.request.user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)
    
    @action(detail=False, methods=['get'])
    def resumen_mensual(self, request):
        periodo = request.query_params.get('periodo')
        desde = f"{periodo}-01"
        hasta = f"{periodo}-31"
        
        summary = Asistencia.objects.filter(
            empresa=request.user.empresa,
            fecha__range=[desde, hasta]
        ).aggregate(
            total=Count('id'),
            dias_trabajados=Count('id', filter=~Q(falta=True)),
            horas_extras_total=Sum('horas_extras')
        )
        
        return Response(summary)


class PlanillaViewSet(viewsets.ModelViewSet):
    serializer_class = PlanillaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Planilla.objects.filter(empresa=self.request.user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)
    
    @action(detail=True, methods=['post'])
    def generar_planilla(self, request, pk=None):
        planilla = self.get_object()
        periodo = planilla.periodo
        
        empleados = Empleado.objects.filter(empresa=request.user.empresa, activo=True)
        
        for emp in empleados:
            remuneracion, _ = Remuneracion.objects.get_or_create(
                empleado=emp,
                periodo=periodo,
                defaults={
                    'basic_salary': Decimal('1500.00'),
                    'total_ingreso': Decimal('1500.00'),
                    'ingreso_gravado': Decimal('1500.00')
                }
            )
            
            descuento, _ = Descuento.objects.get_or_create(
                empleado=emp,
                periodo=periodo,
                defaults={
                    'afp_aporte': Decimal('135.00'),
                    'total_descuento': Decimal('135.00')
                }
            )
        
        total_ingresos = Remuneracion.objects.filter(
            empleado__empresa=request.user.empresa,
            periodo=periodo
        ).aggregate(total=Sum('total_ingreso'))['total'] or Decimal('0.00')
        
        total_descuentos = Descuento.objects.filter(
            empleado__empresa=request.user.empresa,
            periodo=periodo
        ).aggregate(total=Sum('total_descuento'))['total'] or Decimal('0.00')
        
        planilla.total_empleados = empleados.count()
        planilla.total_ingresos = total_ingresos
        planilla.total_descuentos = total_descuentos
        planilla.total_neto = total_ingresos - total_descuentos
        planilla.save()
        
        return Response(PlanillaSerializer(planilla).data)
    
    @action(detail=True, methods=['get'])
    def generar_plame(self, request, pk=None):
        planilla = self.get_object()
        
        from apps.nomina.services import GenerarPlameService
        servicio = GenerarPlameService(planilla)
        result = servicio.generar()
        
        if result['success']:
            planilla.archivo_plame = result['filepath']
            planilla.save()
        
        return Response(result)
    
    @action(detail=True, methods=['get'])
    def exportar_pdf(self, request, pk=None):
        planilla = self.get_object()
        
        from apps.nomina.services import GenerarPdfPlanillaService
        servicio = GenerarPdfPlanillaService(planilla)
        result = servicio.generar()
        
        return Response(result)