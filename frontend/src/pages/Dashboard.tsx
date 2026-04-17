import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'

const dataVentas = [
  { mes: 'Ene', ventas: 4000 },
  { mes: 'Feb', ventas: 3000 },
  { mes: 'Mar', ventas: 5000 },
  { mes: 'Abr', ventas: 4500 },
  { mes: 'May', ventas: 6000 },
  { mes: 'Jun', ventas: 5500 },
]

const datosContabilidad = [
  { mes: 'Ene', debe: 4000, haber: 4000 },
  { mes: 'Feb', debe: 3000, haber: 3000 },
  { mes: 'Mar', debe: 5000, haber: 5000 },
  { mes: 'Abr', debe: 4500, haber: 4500 },
  { mes: 'May', debe: 6000, haber: 6000 },
  { mes: 'Jun', debe: 5500, haber: 5500 },
]

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Dashboard</h2>
      
      {/* Tarjetas de resumen */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <p className="text-sm text-gray-600">Empresas Activas</p>
          <p className="text-2xl font-bold">12</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <p className="text-sm text-gray-600">Comprobantes Emitidos</p>
          <p className="text-2xl font-bold">1,234</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <p className="text-sm text-gray-600">Total Ventas (S/)</p>
          <p className="text-2xl font-bold">125,400</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <p className="text-sm text-gray-600">Empleados</p>
          <p className="text-2xl font-bold">48</p>
        </div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold mb-4">Ventas Mensuales</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dataVentas}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="mes" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="ventas" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold mb-4">Movimientos Contables</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={datosContabilidad}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="mes" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="debe" stroke="#3b82f6" />
              <Line type="monotone" dataKey="haber" stroke="#22c55e" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Actividad reciente */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold mb-4">Actividad Reciente</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2 border-b">
            <span>Factura F001-00001234 creada</span>
            <span className="text-sm text-gray-500">Hace 5 minutos</span>
          </div>
          <div className="flex items-center justify-between py-2 border-b">
            <span>Asiento #001025 aprobado</span>
            <span className="text-sm text-gray-500">Hace 1 hora</span>
          </div>
          <div className="flex items-center justify-between py-2 border-b">
            <span>Empresa "Empresa ABC" registrada</span>
            <span className="text-sm text-gray-500">Hace 3 horas</span>
          </div>
        </div>
      </div>
    </div>
  )
}