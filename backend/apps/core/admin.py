from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Empresa, SerieDocumento, ParametroSistema


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'empresa', 'is_active']
    list_filter = ['tipo_usuario', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('tipo_usuario', 'empresa', 'telefono')}),
    )


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'razon_social', 'tipo_regimen', 'activa', 'ose_enabled']
    list_filter = ['tipo_regimen', 'activa', 'ose_enabled']
    search_fields = ['numero_documento', 'razon_social']
    raw_id_fields = []


@admin.register(SerieDocumento)
class SerieDocumentoAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'tipo_documento', 'serie', 'correlativo']
    list_filter = ['tipo_documento']


@admin.register(ParametroSistema)
class ParametroSistemaAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'clave', 'valor']
    search_fields = ['clave', 'empresa__razon_social']