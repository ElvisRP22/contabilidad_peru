import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { nominaApi } from '../../services/api'
import { useState } from 'react'
import { FileSpreadsheet, Download, Play } from 'lucide-react'

export default function Planillas() {
  const queryClient = useQueryClient()
  const [periodo, setPeriodo] = useState('')
  
  const { data, isLoading } = useQuery({
    queryKey: ['planillas'],
    queryFn: () => nominaApi.planillas.list().then(r => r.data),
  })

  const generarMut = useMutation({
    mutationFn: (id: number) => nominaApi.planillas.generar(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['planillas'] }),
  })

  const getEstadoColor = (estado: string) => {
    const colores: Record<string, string> = {
      borrador: 'bg-gray-100 text-gray-800',
      calculado: 'bg-blue-100 text-blue-800',
      cerrado: 'bg-green-100 text-green-800',
    }
    return colores[estado] || 'bg-gray-100'
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Planillas</h2>
      </div>

      <div className="flex gap-4">
        <input
          type="month"
          value={periodo}
          onChange={(e) => setPeriodo(e.target.value)}
          className="border rounded-lg py-2 px-3"
        />
      </div>
      
      <div className="bg-white rounded-lg border">
        {isLoading ? (
          <div className="p-8 text-center">Cargando...</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-4 py-3">Periodo</th>
                <th className="text-right px-4 py-3">Empleados</th>
                <th className="text-right px-4 py-3">Total Ingresos</th>
                <th className="text-right px-4 py-3">Total Descuentos</th>
                <th className="text-right px-4 py-3">Neto a Pagar</th>
                <th className="text-center px-4 py-3">Estado</th>
                <th className="text-center px-4 py-3">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {data?.map((planilla: any) => (
                <tr key={planilla.id} className="border-t">
                  <td className="px-4 py-3">{planilla.periodo}</td>
                  <td className="px-4 py-3 text-right">{planilla.total_empleados}</td>
                  <td className="px-4 py-3 text-right">S/ {planilla.total_ingresos}</td>
                  <td className="px-4 py-3 text-right">S/ {planilla.total_descuentos}</td>
                  <td className="px-4 py-3 text-right">S/ {planilla.total_neto}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`px-2 py-1 rounded text-xs ${getEstadoColor(planilla.estado)}`}>
                      {planilla.estado}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <div className="flex items-center justify-center gap-2">
                      {planilla.estado === 'borrador' && (
                        <button 
                          onClick={() => generarMut.mutate(planilla.id)} 
                          title="Generar Planilla"
                          className="text-blue-600"
                        >
                          <Play className="w-4 h-4" />
                        </button>
                      )}
                      {planilla.archivo_plame && (
                        <a 
                          href={planilla.archivo_plame} 
                          target="_blank"
                          title="Descargar PLAME"
                          className="text-green-600"
                        >
                          <Download className="w-4 h-4" />
                        </a>
                      )}
                    </div>
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