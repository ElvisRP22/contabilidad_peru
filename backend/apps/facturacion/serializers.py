from rest_framework import serializers
from .models import Comprobante, DetalleComprobante, DocumentoReferencia, HistorialEnvio


class DetalleComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleComprobante
        fields = ['numero_item', 'codigo_producto', 'descripcion', 'unidad', 'cantidad',
                 'precio_unitario', 'precio_base', 'tipo_afectacion_igv', 'porcentaje_igv',
                 'igv', 'monto_descuento', 'importe_total']


class DocumentoReferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoReferencia
        fields = ['tipo_documento', 'serie', 'correlativo', 'motivo']


class ComprobanteSerializer(serializers.ModelSerializer):
    detalles = DetalleComprobanteSerializer(many=True)
    referencias = DocumentoReferenciaSerializer(many=True, required=False)
    
    class Meta:
        model = Comprobante
        fields = ['id', 'tipo_documento', 'moneda', 'tipo_cambio', 'fecha_emision', 'hora_emision',
                 'serie', 'correlativo', 'numero', 
                 'cliente_tipo_documento', 'cliente_numero_documento', 'cliente_denominacion', 
                 'cliente_direccion',
                 'importe_subtotal', 'importe_igv', 'importe_total',
                 'observaciones', 'estado', 'pdf_url', 
                 'referencia_documento', 'referencia_motivo',
                 'detalles', 'referencias']
        read_only_fields = ['numero', 'importe_subtotal', 'importe_igv', 'importe_total', 'hash_cpe', 'cdr_sunat']
    
    def validate_detalles(self, value):
        if not value:
            raise serializers.ValidationError("Debe incluir al menos un detalle")
        return value
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        referencias_data = validated_data.pop('referencias', [])
        
        from apps.core.models import SerieDocumento
        empresa = self.context['request'].user.empresa
        tipo_doc = validated_data['tipo_documento']
        serie = validated_data['serie']
        
        try:
            serie_obj = SerieDocumento.objects.get(empresa=empresa, tipo_documento=tipo_doc, serie=serie)
            serie_obj.correlativo += 1
            correlativo = str(serie_obj.correlativo).zfill(8)
            serie_obj.save()
        except SerieDocumento.DoesNotExist:
            raise serializers.ValidationError(f"Serie {serie} no configurada para {tipo_doc}")
        
        validated_data['correlativo'] = correlativo
        validated_data['numero'] = f"{serie}-{correlativo}"
        
        comprobante = Comprobante.objects.create(**validated_data)
        
        for i, detalle_data in enumerate(detalles_data, 1):
            detalle_data['numero_item'] = i
            DetalleComprobante.objects.create(comprobante=comprobante, **detalle_data)
        
        for ref_data in referencias_data:
            DocumentoReferencia.objects.create(comprobante=comprobante, **ref_data)
        
        comprobante.calcular_totales()
        return comprobante


class HistorialEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialEnvio
        fields = ['id', 'fecha_envio', 'tipo', 'estado', 'mensaje']