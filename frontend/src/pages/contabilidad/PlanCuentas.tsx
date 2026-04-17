import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { contabilidadApi } from '../../services/api'
import { useState } from 'react'

export default function PlanCuentas() {
  const queryClient = useQueryClient()
  const [filtro, setFiltro] = useState('')
  
  const { data, isLoading } = useQuery({
    queryKey: ['planCuentas'],
    queryFn: () => contabilidadApi.planCuentas.list().then(r => r.data),
  })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Plan de Cuentas</h2>
      </div>
      
      <div className="bg-white rounded-lg border">
        <div className="p-4 border-b">
          <input
            type="text"
            placeholder="Buscar cuenta..."
            value={filtro}
            onChange={(e) => setFiltro(e.target.value)}
            className="border rounded-lg py-2 px-3 w-full max-w-md"
          />
        </div>
        
        {isLoading ? (
          <div className="p-8 text-center">Cargando...</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-4 py-3">Código</th>
                <th className="text-left px-4 py-3">Nombre</th>
                <th className="text-left px-4 py-3">Naturaleza</th>
                <th className="text-left px-4 py-3">Tipo</th>
                <th className="text-left px-4 py-3">Nivel</th>
              </tr>
            </thead>
            <tbody>
              {data?.map((cuenta: any) => (
                <tr key={cuenta.id} className="border-t">
                  <td className="px-4 py-3 font-mono">{cuenta.codigo}</td>
                  <td className="px-4 py-3">{cuenta.nombre}</td>
                  <td className="px-4 py-3">{cuenta.naturaleza}</td>
                  <td className="px-4 py-3">{cuenta.tipo_cuenta}</td>
                  <td className="px-4 py-3">{cuenta.nivel}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}