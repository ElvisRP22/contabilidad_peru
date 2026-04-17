from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlmacenViewSet, CategoriaViewSet, ProductoViewSet, KardexViewSet, StockAlmacenViewSet

router = DefaultRouter()
router.register(r'almacenes', AlmacenViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'kardex', KardexViewSet)
router.register(r'stocks', StockAlmacenViewSet)

urlpatterns = [
    path('', include(router.urls)),
]