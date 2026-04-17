from rest_framework import serializers
from .models import PlanCuenta, Asiento, DetalleAsiento, CentroCosto


class PlanCuentaSerializer(serializers.ModelSerializer):
    hijos = serializers.SerializerMethodField()
    tiene_hijos = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = PlanCuenta
        fields = ['id', 'codigo', 'nombre', 'naturaleza', 'tipo_cuenta', 'nivel', 
                 'padre', 'hijos', 'tiene_hijos', 'acepta_movimiento', 'cta_banco', 'cta_efectivo']
    
    def get_hijos(self, obj):
        if obj.tiene_hijos():
            return PlanCuentaSerializer(obj.hijos.all(), many=True).data
        return []


class DetalleAsientoSerializer(serializers.ModelSerializer):
    cuenta_codigo = serializers.CharField(source='cuenta.codigo', read_only=True)
    cuenta_nombre = serializers.CharField(source='cuenta.nombre', read_only=True)
    centro_costo_nombre = serializers.CharField(source='centro_costo.nombre', read_only=True)
    
    class Meta:
        model = DetalleAsiento
        fields = ['id', 'cuenta', 'cuenta_codigo', 'cuenta_nombre', 'debe', 'haber', 'glosa', 
                 'centro_costo', 'centro_costo_nombre']


class AsientoSerializer(serializers.ModelSerializer):
    detalles = DetalleAsientoSerializer(many=True)
    usuario_registra_nombre = serializers.CharField(source='usuario_registra.get_full_name', read_only=True)
    balanceado = serializers.SerializerMethodField()
    
    class Meta:
        model = Asiento
        fields = ['id', 'numero', 'fecha', 'glosa', 'debe', 'haber', 'balanceado', 'estado', 
                 'cerrado', 'usuario_registra', 'usuario_registra_nombre', 
                 'fecha_registro', 'detalles']
    
    def get_balanceado(self, obj):
        return obj.calcular_totales()
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        asiento = Asiento.objects.create(**validated_data)
        for detalle_data in detalles_data:
            DetalleAsiento.objects.create(asiento=asiento, **detalle_data)
        asiento.calcular_totales()
        return asiento
    
    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.detalles.all().delete()
        for detalle_data in detalles_data:
            DetalleAsiento.objects.create(asiento=instance, **detalle_data)
        instance.calcular_totales()
        return instance


class CentroCostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroCosto
        fields = ['id', 'codigo', 'nombre', 'activo']