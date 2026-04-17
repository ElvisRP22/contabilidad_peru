from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Max, Avg
from .models import Almacen, Categoria, Producto, Kardex, StockAlmacen
from .serializers import AlmacenSerializer, CategoriaSerializer, ProductoSerializer, KardexSerializer, StockAlmacenSerializer


class AlmacenViewSet(viewsets.ModelViewSet):
    serializer_class = AlmacenSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Almacen.objects.filter(empresa=self.request.user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Categoria.objects.filter(empresa=self.request.user.empresa, padre__isnull=True)
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)


class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['categoria', 'activo']
    search_fields = ['codigo', 'nombre', 'codigo_barras']
    
    def get_queryset(self):
        return Producto.objects.filter(empresa=self.request.user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)
    
    @action(detail=True, methods=['get'])
    def kardex(self, request, pk=None):
        producto = self.get_object()
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')
        
        queryset = Kardex.objects.filter(producto=producto)
        if desde and hasta:
            queryset = queryset.filter(fecha_movimiento__range=[desde, hasta])
        
        return Response(KardexSerializer(queryset, many=True).data)
    
    @action(detail=False, methods=['get'])
    def stock_minimo(self, request):
        productos = Producto.objects.filter(
            empresa=request.user.empresa,
            cantidad__lte=models.F('cantidad_minima')
        )
        return Response(ProductoSerializer(productos, many=True).data)


class KardexViewSet(viewsets.ModelViewSet):
    serializer_class = KardexSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['producto', 'almacen', 'tipo_movimiento', 'fecha_movimiento']
    
    def get_queryset(self):
        return Kardex.objects.filter(empresa=self.request.user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa, usuario_registra=self.request.user)
        producto = serializer.instance.producto
        producto.save()
    
    @action(detail=False, methods=['post'])
    def movimientos_bulk(self, request):
        movimientos = request.data.get('movimientos', [])
        results = []
        
        for mov_data in movimientos:
            serializer = KardexSerializer(data=mov_data)
            if serializer.is_valid():
                serializer.save(empresa=request.user.empresa, usuario_registra=request.user)
                results.append({'success': True, 'data': serializer.data})
            else:
                results.append({'success': False, 'errors': serializer.errors})
        
        return Response(results)
    
    @action(detail=False, methods=['get'])
    def kardex_producto(self, request):
        producto_id = request.query_params.get('producto_id')
        almacen_id = request.query_params.get('almacen_id')
        
        queryset = Kardex.objects.filter(
            empresa=request.user.empresa,
            producto_id=producto_id,
            almacen_id=almacen_id
        ).order_by('fecha_movimiento', 'id')
        
        return Response(KardexSerializer(queryset, many=True).data)


class StockAlmacenViewSet(viewsets.ModelViewSet):
    serializer_class = StockAlmacenSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return StockAlmacen.objects.filter(producto__empresa=self.request.user.empresa)