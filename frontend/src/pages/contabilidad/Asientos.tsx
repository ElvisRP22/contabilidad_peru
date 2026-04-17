import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { contabilidadApi } from '../../services/api'
import { useState, useEffect } from 'react'
import { Check, X } from 'lucide-react'

export default function Asientos() {
  const queryClient = useQueryClient()
  const [filtroFecha, setFiltroFecha] = useState({ desde: '', hasta: '' })
  
  const { data: asientos, isLoading } = useQuery({
    queryKey: ['asientos', filtroFecha],
    queryFn: () => contabilidadApi.asientos.list(filtroFecha).then(r => r.data),
  })

  const aprobarMut = useMutation({
    mutationFn: (id: number) => contabilidadApi.asientos.aprobar(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['asientos'] }),
  })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Asientos Contables</h2>
      </div>

      <div className="flex gap-4">
        <input type="date" value={filtroFecha.desde} onChange={e => setFiltroFecha({...filtroFecha, desde: e.target.value})} className="border rounded-lg py-2 px-3" />
        <input type="date" value={filtroFecha.hasta} onChange={e => setFiltroFecha({...filtroFecha, hasta: e.target.value})} className="border rounded-lg py-2 px-3" />
      </div>
      
      <div className="bg-white rounded-lg border">
        {isLoading ? (
          <div className="p-8 text-center">Cargando...</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-4 py-3">#</th>
                <th className="text-left px-4 py-3">Fecha</th>
                <th className="text-left px-4 py-3">Glosa</th>
                <th className="text-right px-4 py-3">Debe</th>
                <th className="text-right px-4 py-3">Haber</th>
                <th className="text-center px-4 py-3">Estado</th>
                <th className="text-center px-4 py-3">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {asientos?.map((asiento: any) => (
                <tr key={asiento.id} className="border-t">
                  <td className="px-4 py-3">{asiento.numero}</td>
                  <td className="px-4 py-3">{asiento.fecha}</td>
                  <td className="px-4 py-3">{asiento.glosa}</td>
                  <td className="px-4 py-3 text-right">{asiento.debe}</td>
                  <td className="px-4 py-3 text-right">{asiento.haber}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`px-2 py-1 rounded text-xs ${
                      asiento.cerrado ? 'bg-green-100 text-green-800' : 
                      asiento.estado === 'aprobado' ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {asiento.cerrado ? 'Cerrado' : asiento.estado}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    {asiento.estado === 'pendiente' && (
                      <button 
                        onClick={() => aprobarMut.mutate(asiento.id)}
                        className="text-green-600 hover:text-green-800"
                        title="Aprobar"
                      >
                        <Check className="w-4 h-4" />
                      </button>
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