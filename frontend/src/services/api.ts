import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  refresh: (refresh_token: string) =>
    api.post('/auth/refresh', { refresh_token }),
  me: () => api.get('/auth/me'),
}

export const usuariosApi = {
  list: (params?: any) => api.get('/core/usuarios', { params }),
  get: (id: number) => api.get(`/core/usuarios/${id}`),
  create: (data: any) => api.post('/core/usuarios', data),
  update: (id: number, data: any) => api.put(`/core/usuarios/${id}`, data),
  delete: (id: number) => api.delete(`/core/usuarios/${id}`),
}

export const empresasApi = {
  list: (params?: any) => api.get('/core/empresas', { params }),
  get: (id: number) => api.get(`/core/empresas/${id}`),
  create: (data: any) => api.post('/core/empresas', data),
  update: (id: number, data: any) => api.put(`/core/empresas/${id}`, data),
  delete: (id: number) => api.delete(`/core/empresas/${id}`),
  series: (id: number) => api.get(`/core/empresas/${id}/series`),
  agregarSerie: (id: number, data: any) => api.post(`/core/empresas/${id}/series`, data),
}

export const contabilidadApi = {
  planCuentas: {
    list: (params?: any) => api.get('/contabilidad/plan-cuentas', { params }),
    get: (id: number) => api.get(`/contabilidad/plan-cuentas/${id}`),
    create: (data: any) => api.post('/contabilidad/plan-cuentas', data),
    update: (id: number, data: any) => api.put(`/contabilidad/plan-cuentas/${id}`, data),
    delete: (id: number) => api.delete(`/contabilidad/plan-cuentas/${id}`),
  },
  asientos: {
    list: (params?: any) => api.get('/contabilidad/asientos', { params }),
    get: (id: number) => api.get(`/contabilidad/asientos/${id}`),
    create: (data: any) => api.post('/contabilidad/asientos', data),
    update: (id: number, data: any) => api.put(`/contabilidad/asientos/${id}`, data),
    delete: (id: number) => api.delete(`/contabilidad/asientos/${id}`),
    aprobar: (id: number) => api.post(`/contabilidad/asientos/${id}/aprobar`),
    cerrar: (id: number) => api.post(`/contabilidad/asientos/${id}/cerrar`),
  },
  reportes: {
    balanceComprobacion: (empresa_id: number, fecha: string) =>
      api.get('/contabilidad/reportes/balance_comprobacion', { params: { empresa_id, fecha } }),
    mayor: (empresa_id: number, cuenta_id: number, fecha_inicio: string, fecha_fin: string) =>
      api.get('/contabilidad/reportes/mayor', { params: { empresa_id, cuenta_id, fecha_inicio, fecha_fin } }),
  },
}

export const facturacionApi = {
  comprobantes: {
    list: (params?: any) => api.get('/facturacion/comprobantes', { params }),
    get: (id: number) => api.get(`/facturacion/comprobantes/${id}`),
    create: (data: any) => api.post('/facturacion/comprobantes', data),
    update: (id: number, data: any) => api.put(`/facturacion/comprobantes/${id}`, data),
    delete: (id: number) => api.delete(`/facturacion/comprobantes/${id}`),
    generar: (id: number) => api.post(`/facturacion/comprobantes/${id}/generar`),
    firmar: (id: number) => api.post(`/facturacion/comprobantes/${id}/firmar`),
    enviarSunat: (id: number) => api.post(`/facturacion/comprobantes/${id}/enviar_sunat`),
    pdf: (id: number) => api.get(`/facturacion/comprobantes/${id}/obtener_pdf`),
    anular: (id: number) => api.post(`/facturacion/comprobantes/${id}/anular`),
  },
}

export const inventarioApi = {
  almacenes: {
    list: (params?: any) => api.get('/inventario/almacenes', { params }),
    create: (data: any) => api.post('/inventario/almacenes', data),
  },
  categorias: {
    list: (params?: any) => api.get('/inventario/categorias', { params }),
    create: (data: any) => api.post('/inventario/categorias', data),
  },
  productos: {
    list: (params?: any) => api.get('/inventario/productos', { params }),
    get: (id: number) => api.get(`/inventario/productos/${id}`),
    create: (data: any) => api.post('/inventario/productos', data),
    update: (id: number, data: any) => api.put(`/inventario/productos/${id}`, data),
    delete: (id: number) => api.delete(`/inventario/productos/${id}`),
    kardex: (id: number, params?: any) => api.get(`/inventario/productos/${id}/kardex`, { params }),
  },
  kardex: {
    create: (data: any) => api.post('/inventario/kardex', data),
  },
  stock: {
    list: (empresa_id: number, params?: any) => api.get('/inventario/stock', { params: { empresa_id, ...params } }),
  },
}

export const nominaApi = {
  empleados: {
    list: (params?: any) => api.get('/nomina/empleados', { params }),
    get: (id: number) => api.get(`/nomina/empleados/${id}`),
    create: (data: any) => api.post('/nomina/empleados', data),
    update: (id: number, data: any) => api.put(`/nomina/empleados/${id}`, data),
    delete: (id: number) => api.delete(`/nomina/empleados/${id}`),
  },
  planillas: {
    list: (params?: any) => api.get('/nomina/planillas', { params }),
    get: (id: number) => api.get(`/nomina/planillas/${id}`),
    create: (data: any) => api.post('/nomina/planillas', data),
    generar: (id: number) => api.post(`/nomina/planillas/${id}/generar_planilla`),
    plame: (id: number) => api.get(`/nomina/planillas/${id}/generar_plame`),
  },
  beneficios: {
    list: (params?: any) => api.get('/nomina/beneficios', { params }),
    create: (data: any) => api.post('/nomina/beneficios', data),
  },
  asistencia: {
    list: (empresa_id: number, params?: any) => api.get('/nomina/asistencias', { params: { empresa_id, ...params } }),
    create: (data: any) => api.post('/nomina/asistencias', data),
  },
}