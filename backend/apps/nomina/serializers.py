from rest_framework import serializers
from .models import Empleado, Remuneracion, Descuento, BeneficioSocial, Asistencia, Planilla


class EmpleadoSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Empleado
        fields = ['id', 'numero_documento', 'tipo_documento', 'nombres', 'apellido_paterno', 
                 'apellido_materno', 'full_name', 'sexo', 'fecha_nacimiento', 'direccion', 
                 'telefono', 'email', 'fecha_ingreso', 'fecha_cese', 'motivo_cese',
                 'cargo', 'area', 'regimen_laboral', 'jornada_trabajo', 'tipo_contrato',
                 'cuenta_banco', 'banco', 'activo']


class RemuneracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remuneracion
        fields = ['id', 'periodo', 'basic_salary', 'asig_familiar', 'bonificacion', 
                 'comision', 'overtime', 'otros', 'ingreso_gravado', 'ingreso_no_gravado', 'total_ingreso']


class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = ['id', 'periodo', 'afp_aporte', 'afp_prima', 'afp_seguro', 'onp',
                 'faltas', 'tardanzas', 'anticipos', 'otros', 'total_descuento']


class BeneficioSocialSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.get_full_name', read_only=True)
    
    class Meta:
        model = BeneficioSocial
        fields = ['id', 'tipo', 'periodo', 'tiempo', 'basico', 'promedio', 'monto',
                 'fecha_pago', 'estado', 'empleado_nombre']


class AsistenciaSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.get_full_name', read_only=True)
    
    class Meta:
        model = Asistencia
        fields = ['id', 'empleado', 'empleado_nombre', 'fecha', 'hora_entrada', 'hora_salida',
                 'hora_entrada_min', 'horas_trabajadas', 'horas_extras', 
                 'falta', 'permiso', 'observacion']


class PlanillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planilla
        fields = ['id', 'periodo', 'total_empleados', 'total_ingresos', 'total_descuentos',
                  'total_aportes', 'total_neto', 'archivo_plame', 'estado', 'fecha_cierre']