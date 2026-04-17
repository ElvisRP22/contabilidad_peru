import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { empresasApi } from '../services/api'
import { Plus, Search, Edit, Trash } from 'lucide-react'

export default function Empresas() {
  const queryClient = useQueryClient()
  const [search, setSearch] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [empresaEditando, setEmpresaEditando] = useState<any>(null)

  const { data: empresas, isLoading } = useQuery({
    queryKey: ['empresas'],
    queryFn: () => empresasApi.list().then(r => r.data),
  })

  const crearMut = useMutation({
    mutationFn: empresasApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['empresas'] })
      setModalOpen(false)
    },
  })

  const eliminarMut = useMutation({
    mutationFn: empresasApi.delete,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['empresas'] }),
  })

  const empresasFiltradas = empresas?.filter((e: any) => 
    e.razon_social.toLowerCase().includes(search.toLowerCase()) ||
    e.numero_documento.includes(search)
  )

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Empresas</h2>
        <button 
          onClick={() => { setEmpresaEditando(null); setModalOpen(true) }}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg"
        >
          <Plus className="w-4 h-4" /> Nueva Empresa
        </button>
      </div>

      <div className="bg-white rounded-lg border">
        <div className="p-4 border-b flex items-center gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar empresas..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10 w-full border rounded-lg py-2"
            />
          </div>
        </div>

        {isLoading ? (
          <div className="p-8 text-center text-gray-500">Cargando...</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-4 py-3">RUC</th>
                <th className="text-left px-4 py-3">Razón Social</th>
                <th className="text-left px-4 py-3">Régimen</th>
                <th className="text-left px-4 py-3">Estado</th>
                <th className="text-right px-4 py-3">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {empresasFiltradas?.map((empresa: any) => (
                <tr key={empresa.id} className="border-t">
                  <td className="px-4 py-3">{empresa.numero_documento}</td>
                  <td className="px-4 py-3">{empresa.razon_social}</td>
                  <td className="px-4 py-3">{empresa.tipo_regimen}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded text-xs ${empresa.activa ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {empresa.activa ? 'Activa' : 'Inactiva'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button 
                      onClick={() => { setEmpresaEditando(empresa); setModalOpen(true) }}
                      className="text-blue-600 hover:text-blue-800 mr-3"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                    <button 
                      onClick={() => { if(confirm('¿Eliminar?')) eliminarMut.mutate(empresa.id) }}
                      className="text-red-600 hover:text-red-800"
                    >
                      <Trash className="w-4 h-4" />
                    </button>
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