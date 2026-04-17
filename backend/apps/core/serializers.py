from rest_framework import serializers
from .models import Usuario, Empresa, SerieDocumento, ParametroSistema


class UsuarioSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.razon_social', read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo_usuario', 
                 'empresa', 'empresa_nombre', 'telefono', 'fecha_registro', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'razon_social', 'nombre_comercial', 'tipo_documento', 
                 'numero_documento', 'direccion', 'departamento', 'provincia', 
                 'distrito', 'telefono', 'email', 'tipo_regimen', 'representante_legal',
                 'dni_representante', 'activa', 'fecha_registro', 'ose_enabled', 'ose_proveedor']


class SerieDocumentoSerializer(serializers.ModelSerializer):
    tipo_documento_display = serializers.CharField(source='get_tipo_documento_display', read_only=True)
    
    class Meta:
        model = SerieDocumento
        fields = ['id', 'tipo_documento', 'tipo_documento_display', 'serie', 
                 'correlativo', 'observaciones']


class ParametroSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametroSistema
        fields = ['id', 'clave', 'valor', 'descripcion']