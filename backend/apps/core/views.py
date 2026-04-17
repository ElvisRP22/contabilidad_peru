from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Usuario, Empresa, SerieDocumento, ParametroSistema
from .serializers import UsuarioSerializer, EmpresaSerializer, SerieDocumentoSerializer, ParametroSistemaSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.tipo_usuario == 'admin':
            return qs
        return qs.filter(empresa=self.request.user.empresa)
    
    @action(detail=False, methods=['post'])
    def registro(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.tipo_usuario == 'admin':
            return Empresa.objects.all()
        return Empresa.objects.filter(id=self.request.user.empresa.id)
    
    @action(detail=True, methods=['get'])
    def series(self, request, pk=None):
        empresa = self.get_object()
        series = empresa.series.all()
        serializer = SerieDocumentoSerializer(series, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def agregar_serie(self, request, pk=None):
        empresa = self.get_object()
        serializer = SerieDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(empresa=empresa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def parametros(self, request, pk=None):
        empresa = self.get_object()
        parametros = empresa.parametros.all()
        serializer = ParametroSistemaSerializer(parametros, many=True)
        return Response(serializer.data)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = request.user
            response.data['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'tipo_usuario': user.tipo_usuario,
                'empresa_id': user.empresa_id,
            }
        return response


class RefreshTokenView(TokenRefreshView):
    pass