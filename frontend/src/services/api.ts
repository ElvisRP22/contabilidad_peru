import axios from 'axios'

export const api = axios.create({
  baseURL: '/api',
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
    api.post('/core/auth/login/', { username, password }),
  refresh: (refresh: string) =>
    api.post('/core/auth/refresh/', { refresh }),
}

export const empresasApi = {
  list: () => api.get('/core/empresas/'),
  get: (id: number) => api.get(`/core/empresas/${id}/`),
  create: (data: any) => api.post('/core/empresas/', data),
  update: (id: number, data: any) => api.patch(`/core/empresas/${id}/`, data),
  delete: (id: number) => api.delete(`/core/empresas/${id}/`),
}

export const contabilidadApi = {
  planCuentas: {
    list: (empresaId: number) => api.get(`/contabilidad/plan-cuentas/?empresa=${empresaId}`),
    get: (id: number) => api.get(`/contabilidad/plan-cuentas/${id}/`),
    create: (data: any) => api.post('/contabilidad/plan-cuentas/', data),
    update: (id: number, data: any) => api.patch(`/contabilidad/plan-cuentas/${id}/`, data),
    delete: (id: number) => api.delete(`/contabilidad/plan-cuentas/${id}/`),
  },
  asientos: {
    list: (params?: any) => api.get('/contabilidad/asientos/', { params }),
    get: (id: number) => api.get(`/contabilidad/asientos/${id}/`),
    create: (data: any) => api.post('/contabilidad/asientos/', data),
    update: (id: number, data: any) => api.patch(`/contabilidad/asientos/${id}/`, data),
    delete: (id: number) => api.delete(`/contabilidad/asientos/${id}/`),
    aprobar: (id: number) => api.post(`/contabilidad/asientos/${id}/aprobar/`),
    cerrar: (id: number) => api.post(`/contabilidad/asientos/${id}/cerrar/`),
  },
}

export const facturacionApi = {
  comprobantes: {
    list: (params?: any) => api.get('/facturacion/comprobantes/', { params }),
    get: (id: number) => api.get(`/facturacion/comprobantes/${id}/`),
    create: (data: any) => api.post('/facturacion/comprobantes/', data),
    update: (id: number, data: any) => api.patch(`/facturacion/comprobantes/${id}/`, data),
    delete: (id: number) => api.delete(`/facturacion/comprobantes/${id}/`),
    generar: (id: number) => api.post(`/facturacion/comprobantes/${id}/generar/`),
    firmar: (id: number) => api.post(`/facturacion/comprobantes/${id}/firmar/`),
    enviarSunat: (id: number) => api.post(`/facturacion/comprobantes/${id}/enviar_sunat/`),
    pdf: (id: number) => api.get(`/facturacion/comprobantes/${id}/obtener_pdf/`),
  },
}

export const inventarioApi = {
  productos: {
    list: (params?: any) => api.get('/inventario/productos/', { params }),
    get: (id: number) => api.get(`/inventario/productos/${id}/`),
    create: (data: any) => api.post('/inventario/productos/', data),
    update: (id: number, data: any) => api.patch(`/inventario/productos/${id}/`, data),
    delete: (id: number) => api.delete(`/inventario/productos/${id}/`),
    kardex: (id: number, params?: any) => api.get(`/inventario/productos/${id}/kardex/`, { params }),
  },
}

export const nominaApi = {
  empleados: {
    list: (params?: any) => api.get('/nomina/empleados/', { params }),
    get: (id: number) => api.get(`/nomina/empleados/${id}/`),
    create: (data: any) => api.post('/nomina/empleados/', data),
    update: (id: number, data: any) => api.patch(`/nomina/empleados/${id}/`, data),
    delete: (id: number) => api.delete(`/nomina/empleados/${id}/`),
  },
  planillas: {
    list: (params?: any) => api.get('/nomina/planillas/', { params }),
    get: (id: number) => api.get(`/nomina/planillas/${id}/`),
    create: (data: any) => api.post('/nomina/planillas/', data),
    generar: (id: number) => api.post(`/nomina/planillas/${id}/generar_planilla/`),
    plame: (id: number) => api.get(`/nomina/planillas/${id}/generar_plame/`),
  },
}