from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanCuentaViewSet, AsientoViewSet, CentroCostoViewSet, ReporteViewSet

router = DefaultRouter()
router.register(r'plan-cuentas', PlanCuentaViewSet)
router.register(r'asientos', AsientoViewSet)
router.register(r'centros-costo', CentroCostoViewSet)
router.register(r'reportes', ReporteViewSet, basename='reportes')

urlpatterns = [
    path('', include(router.urls)),
]