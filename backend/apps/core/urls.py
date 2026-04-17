from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, EmpresaViewSet, LoginView, RefreshTokenView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'empresas', EmpresaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]