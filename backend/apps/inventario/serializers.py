from rest_framework import serializers
from .models import Almacen, Categoria, Producto, Kardex, StockAlmacen


class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = ['id', 'codigo', 'nombre', 'direccion', 'principal', 'activo']


class CategoriaSerializer(serializers.ModelSerializer):
    subcategorias = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = ['id', 'codigo', 'nombre', 'padre', 'subcategorias']
    
    def get_subcategorias(self, obj):
        if obj.subcategorias.exists():
            return CategoriaSerializer(obj.subcategorias.all(), many=True).data
        return []


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    stock_actual = serializers.DecimalField(source='cantidad', max_digits=15, decimal_places=3, read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'codigo_barras', 'nombre', 'descripcion', 'categoria', 'categoria_nombre',
                 'unidad', 'presentacion', 'cantidad', 'cantidad_minima', 'cantidad_maxima',
                 'costo_unitario', 'precio_venta', 'afecta_igv', 'tipo_afectacion',
                 'stock_actual', 'activo']


class KardexSerializer(serializers.ModelSerializer):
    producto_codigo = serializers.CharField(source='producto.codigo', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    almacen_nombre = serializers.CharField(source='almacen.nombre', read_only=True)
    
    class Meta:
        model = Kardex
        fields = ['id', 'producto', 'producto_codigo', 'producto_nombre', 'almacen', 'almacen_nombre',
                 'tipo_movimiento', 'numero_documento', 'fecha_movimiento',
                 'cantidad', 'costo_unitario', 'costo_total',
                 'cantidad_saldo', 'costo_promedio', 'costo_saldo',
                 'glosa', 'referencia_id', 'referencia_tipo', 'fecha_registro']


class StockAlmacenSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    almacen_nombre = serializers.CharField(source='almacen.nombre', read_only=True)
    
    class Meta:
        model = StockAlmacen
        fields = ['id', 'producto', 'producto_nombre', 'almacen', 'almacen_nombre', 'cantidad', 'costo_promedio']