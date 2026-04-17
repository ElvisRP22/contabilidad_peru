import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { facturacionApi } from '../../services/api'
import { useState } from 'react'
import { FileText, Send, Download } from 'lucide-react'

export default function Comprobantes() {
  const queryClient = useQueryClient()
  const [filtro, setFiltro] = useState({ tipo: '', estado: '' })
  
  const { data, isLoading } = useQuery({
    queryKey: ['comprobantes', filtro],
    queryFn: () => facturacionApi.comprobantes.list(filtro).then(r => r.data),
  })

  const generarMut = useMutation({
    mutationFn: (id: number) => facturacionApi.comprobantes.generar(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['comprobantes'] }),
  })

  const enviarMut = useMutation({
    mutationFn: (id: number) => facturacionApi.comprobantes.enviarSunat(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['comprobantes'] }),
  })

  const getEstadoColor = (estado: string) => {
    const colores: Record<string, string> = {
      borrador: 'bg-gray-100 text-gray-800',
      generado: 'bg-blue-100 text-blue-800',
      firmado: 'bg-indigo-100 text-indigo-800',
      enviado: 'bg-purple-100 text-purple-800',
      aceptado: 'bg-green-100 text-green-800',
      rechazado: 'bg-red-100 text-red-800',
      anulado: 'bg-yellow-100 text-yellow-800',
    }
    return colores[estado] || 'bg-gray-100'
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Comprobantes Electrónicos</h2>
      </div>

      <div className="flex gap-4">
        <select 
          value={filtro.tipo} 
          onChange={e => setFiltro({...filtro, tipo: e.target.value})}
          className="border rounded-lg py-2 px-3"
        >
          <option value="">Todos los tipos</option>
          <option value="01">Factura</option>
          <option value="03">Boleta</option>
          <option value="07">Nota de Crédito</option>
        </select>
        <select 
          value={filtro.estado} 
          onChange={e => setFiltro({...filtro, estado: e.target.value})}
          className="border rounded-lg py-2 px-3"
        >
          <option value="">Todos los estados</option>
          <option value="borrador">Borrador</option>
          <option value="generado">Generado</option>
          <option value="enviado">Enviado</option>
          <option value="aceptado">Aceptado</option>
        </select>
      </div>
      
      <div className="bg-white rounded-lg border">
        {isLoading ? (
          <div className="p-8 text-center">Cargando...</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-4 py-3">Número</th>
                <th className="text-left px-4 py-3">Tipo</th>
                <th className="text-left px-4 py-3">Cliente</th>
                <th className="text-right px-4 py-3">Total</th>
                <th className="text-left px-4 py-3">Fecha</th>
                <th className="text-center px-4 py-3">Estado</th>
                <th className="text-center px-4 py-3">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {data?.map((comp: any) => (
                <tr key={comp.id} className="border-t">
                  <td className="px-4 py-3">{comp.numero}</td>
                  <td className="px-4 py-3">{comp.tipo_documento}</td>
                  <td className="px-4 py-3">{comp.cliente_denominacion}</td>
                  <td className="px-4 py-3 text-right">S/ {comp.importe_total}</td>
                  <td className="px-4 py-3">{comp.fecha_emision}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`px-2 py-1 rounded text-xs ${getEstadoColor(comp.estado)}`}>
                      {comp.estado}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <div className="flex items-center justify-center gap-2">
                      {comp.estado === 'borrador' && (
                        <button onClick={() => generarMut.mutate(comp.id)} title="Generar" className="text-blue-600">
                          <FileText className="w-4 h-4" />
                        </button>
                      )}
                      {comp.estado === 'firmado' && (
                        <button onClick={() => enviarMut.mutate(comp.id)} title="Enviar a SUNAT" className="text-purple-600">
                          <Send className="w-4 h-4" />
                        </button>
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