import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { nominaApi } from '../../services/api'
import { useState } from 'react'
import { UserCheck, UserX } from 'lucide-react'

export default function Empleados() {
  const queryClient = useQueryClient()
  const [filtro, setFiltro] = useState('')
  const [soloActivos, setSoloActivos] = useState(true)
  
  const { data, isLoading } = useQuery({
    queryKey: ['empleados', soloActivos],
    queryFn: () => nominaApi.empleados.list({ activo: soloActivos }).then(r => r.data),
  })

  const empleadosFiltrados = data?.filter((e: any) => 
    e.nombres.toLowerCase().includes(filtro.toLowerCase()) ||
    e.numero_documento.includes(filtro)
  )

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Empleados</h2>
      </div>

      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Buscar empleado..."
          value={filtro}
          onChange={(e) => setFiltro(e.target.value)}
          className="border rounded-lg py-2 px-3 w-full max-w-md"
        />
        <label className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={soloActivos} 
            onChange={(e) => setSoloActivos(e.target.checked)}
            className="rounded"
          />
          Solo activos
        </label>
      </div>
      
      <div className="bg-white rounded-lg border">
        {isLoading ? (
          <div className="p-8 text-center">Cargando...</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-4 py-3">DNI</th>
                <th className="text-left px-4 py-3">Nombre</th>
                <th className="text-left px-4 py-3">Cargo</th>
                <th className="text-left px-4 py-3">Área</th>
                <th className="text-left px-4 py-3">Fecha Ingreso</th>
                <th className="text-center px-4 py-3">Estado</th>
              </tr>
            </thead>
            <tbody>
              {empleadosFiltrados?.map((emp: any) => (
                <tr key={emp.id} className="border-t">
                  <td className="px-4 py-3">{emp.numero_documento}</td>
                  <td className="px-4 py-3">{emp.apellido_paterno} {emp.apellido_materno}, {emp.nombres}</td>
                  <td className="px-4 py-3">{emp.cargo}</td>
                  <td className="px-4 py-3">{emp.area}</td>
                  <td className="px-4 py-3">{emp.fecha_ingreso}</td>
                  <td className="px-4 py-3 text-center">
                    {emp.activo ? (
                      <span className="flex items-center justify-center text-green-600">
                        <UserCheck className="w-4 h-4" />
                      </span>
                    ) : (
                      <span className="flex items-center justify-center text-red-600">
                        <UserX className="w-4 h-4" />
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}