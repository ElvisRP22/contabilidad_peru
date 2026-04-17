from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewSet, RemuneracionViewSet, DescuentoViewSet, BeneficioSocialViewSet, AsistenciaViewSet, PlanillaViewSet

router = DefaultRouter()
router.register(r'empleados', EmpleadoViewSet)
router.register(r'remuneraciones', RemuneracionViewSet)
router.register(r'descuentos', DescuentoViewSet)
router.register(r'beneficios', BeneficioSocialViewSet)
router.register(r'asistencias', AsistenciaViewSet)
router.register(r'planillas', PlanillaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]