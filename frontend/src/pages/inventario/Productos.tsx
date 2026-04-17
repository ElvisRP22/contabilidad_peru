import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { inventarioApi } from '../../services/api'
import { useState } from 'react'
import { Package, AlertTriangle } from 'lucide-react'

export default function Productos() {
  const queryClient = useQueryClient()
  const [filtro, setFiltro] = useState('')
  
  const { data, isLoading } = useQuery({
    queryKey: ['productos'],
    queryFn: () => inventarioApi.productos.list().then(r => r.data),
  })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Inventario</h2>
      </div>

      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Buscar producto..."
          value={filtro}
          onChange={(e) => setFiltro(e.target.value)}
          className="border rounded-lg py-2 px-3 w-full max-w-md"
        />
      </div>
      
      <div className="bg-white rounded-lg border">
        {isLoading ? (
          <div className="p-8 text-center">Cargando...</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-4 py-3">Código</th>
                <th className="text-left px-4 py-3">Nombre</th>
                <th className="text-left px-4 py-3">Categoría</th>
                <th className="text-right px-4 py-3">Stock</th>
                <th className="text-right px-4 py-3">Costo</th>
                <th className="text-right px-4 py-3">Precio</th>
                <th className="text-center px-4 py-3">Estado</th>
              </tr>
            </thead>
            <tbody>
              {data?.map((prod: any) => (
                <tr key={prod.id} className="border-t">
                  <td className="px-4 py-3">{prod.codigo}</td>
                  <td className="px-4 py-3">{prod.nombre}</td>
                  <td className="px-4 py-3">{prod.categoria_nombre}</td>
                  <td className="px-4 py-3 text-right">{prod.cantidad}</td>
                  <td className="px-4 py-3 text-right">S/ {prod.costo_unitario}</td>
                  <td className="px-4 py-3 text-right">S/ {prod.precio_venta}</td>
                  <td className="px-4 py-3 text-center">
                    {prod.cantidad <= prod.cantidad_minima ? (
                      <span className="flex items-center justify-center text-red-600">
                        <AlertTriangle className="w-4 h-4" />
                      </span>
                    ) : (
                      <span className="text-green-600">OK</span>
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