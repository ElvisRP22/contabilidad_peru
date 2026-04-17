import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAuthStore } from './stores/auth'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Empresas from './pages/Empresas'
import PlanCuentas from './pages/contabilidad/PlanCuentas'
import Asientos from './pages/contabilidad/Asientos'
import Comprobantes from './pages/facturacion/Comprobantes'
import Productos from './pages/inventario/Productos'
import Empleados from './pages/nomina/Empleados'
import Planillas from './pages/nomina/Planillas'

const queryClient = new QueryClient()

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return <>{children}</>
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="empresas" element={<Empresas />} />
            <Route path="contabilidad/plan-cuentas" element={<PlanCuentas />} />
            <Route path="contabilidad/asientos" element={<Asientos />} />
            <Route path="facturacion/comprobantes" element={<Comprobantes />} />
            <Route path="inventario/productos" element={<Productos />} />
            <Route path="nomina/empleados" element={<Empleados />} />
            <Route path="nomina/planillas" element={<Planillas />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App