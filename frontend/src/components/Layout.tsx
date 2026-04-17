import { Outlet, Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '../stores/auth'
import { 
  LayoutDashboard, 
  Building2, 
  BookOpen, 
  FileText, 
  Package, 
  Users, 
  Settings,
  LogOut,
  Menu
} from 'lucide-react'
import { useState } from 'react'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Empresas', href: '/empresas', icon: Building2 },
  { name: 'Contabilidad', href: '#', icon: BookOpen, children: [
    { name: 'Plan de Cuentas', href: '/contabilidad/plan-cuentas' },
    { name: 'Asientos', href: '/contabilidad/asientos' },
  ]},
  { name: 'Facturación', href: '/facturacion/comprobantes', icon: FileText },
  { name: 'Inventario', href: '/inventario/productos', icon: Package },
  { name: 'Nómina', href: '#', icon: Users, children: [
    { name: 'Empleados', href: '/nomina/empleados' },
    { name: 'Planillas', href: '/nomina/planillas' },
  ]},
]

export default function Layout() {
  const location = useLocation()
  const { logout, user } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-16'} bg-white border-r transition-all duration-300`}>
        <div className="flex items-center justify-between p-4 border-b">
          {sidebarOpen && <span className="font-bold text-lg">ContaPerú</span>}
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-1 hover:bg-gray-100 rounded">
            <Menu className="w-5 h-5" />
          </button>
        </div>
        
        <nav className="p-2 space-y-1">
          {navigation.map((item) => (
            <div key={item.name}>
              <Link
                to={item.href}
                className={`flex items-center px-3 py-2 text-sm hover:bg-gray-100 rounded ${
                  location.pathname === item.href ? 'bg-blue-50 text-blue-600' : ''
                }`}
              >
                <item.icon className="w-5 h-5 mr-3" />
                {sidebarOpen && item.name}
              </Link>
              {item.children && sidebarOpen && (
                <div className="ml-6 space-y-1">
                  {item.children.map((child) => (
                    <Link
                      key={child.name}
                      to={child.href}
                      className={`flex items-center px-3 py-2 text-sm hover:bg-gray-100 rounded ${
                        location.pathname === child.href ? 'text-blue-600' : ''
                      }`}
                    >
                      {child.name}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b px-6 py-4 flex items-center justify-between">
          <h1 className="text-xl font-semibold">Sistema Contable</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">{user?.email}</span>
            <button onClick={logout} className="flex items-center text-sm text-gray-600 hover:text-red-600">
              <LogOut className="w-4 h-4 mr-1" />
              Salir
            </button>
          </div>
        </header>
        
        <main className="flex-1 p-6 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}