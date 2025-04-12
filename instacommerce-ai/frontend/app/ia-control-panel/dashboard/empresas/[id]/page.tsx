'use client'

import { useEffect, useState, useRef } from 'react'
import {
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Divider,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material'
import { useParams } from 'next/navigation'
import { toast } from 'react-hot-toast'

interface Empresa {
  id: number
  nombre_empresa: string
  correo: string
  estado_pago: string
  api_key_openai: string | null
  api_key_pinecone: string | null
  endpoint_productos: string | null
  indice_pinecone?: string | null
}

interface ProductoLog {
  title: string
  price: number
  category: string
}

export default function EmpresaDetallePage() {
  const { id } = useParams()
  const [empresa, setEmpresa] = useState<Empresa | null>(null)
  const [loading, setLoading] = useState(true)

  const [openaiKey, setOpenaiKey] = useState('')
  const [pineconeKey, setPineconeKey] = useState('')
  const [endpoint, setEndpoint] = useState('')
  const [indices, setIndices] = useState<string[]>([])
  const [indiceSeleccionado, setIndiceSeleccionado] = useState('')
  const [syncLoading, setSyncLoading] = useState(false)
  const [syncMessage, setSyncMessage] = useState('')
  const [productosLog, setProductosLog] = useState<ProductoLog[]>([])
  const [deleteMessage, setDeleteMessage] = useState('')
  const [progreso, setProgreso] = useState(0)
  const wsRef = useRef<WebSocket | null>(null)
  const [atributosDisponibles, setAtributosDisponibles] = useState<string[]>([])
  const [atributosSeleccionados, setAtributosSeleccionados] = useState<string[]>([])
  const [totalEsperado, setTotalEsperado] = useState(0)
  const [productosRecibidos, setProductosRecibidos] = useState(0)

  const token = typeof window !== 'undefined' ? localStorage.getItem("token") : null

  useEffect(() => {
    const fetchEmpresa = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/empresas/${id}`)
        const data = await res.json()
        setEmpresa(data)
        setOpenaiKey(data.api_key_openai || '')
        setPineconeKey(data.api_key_pinecone || '')
        setEndpoint(data.endpoint_productos || '')
        setIndiceSeleccionado(data.indice_pinecone || '')
      } catch {
        toast.error('Error al cargar la empresa')
      } finally {
        setLoading(false)
      }
    }

    if (id) fetchEmpresa()
  }, [id])

  useEffect(() => {
    const obtenerIndices = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/configuracion/indices-pinecone`)
        const data = await res.json()
        setIndices(data.indices || [])
      } catch {
        toast.error('No se pudieron cargar los índices de Pinecone')
      }
    }

    obtenerIndices()
  }, [])

  useEffect(() => {
    const fetchAtributos = async () => {
      try {
        const resDisponibles = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/configuracion/atributos-disponibles`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        const disponibles = await resDisponibles.json()
        setAtributosDisponibles(disponibles.atributos || [])

        const resSeleccionados = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/configuracion/atributos-seleccionados`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        const seleccionados = await resSeleccionados.json()
        setAtributosSeleccionados(seleccionados.atributos || [])
      } catch {
        toast.error('❌ Error al obtener los atributos')
      }
    }

    if (token) fetchAtributos()
  }, [token])

  const handleGuardarAtributos = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/configuracion/atributos-seleccionados`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ atributos: atributosSeleccionados }),
      })

      if (!res.ok) throw new Error()
      toast.success('✅ Atributos guardados correctamente')
    } catch {
      toast.error('❌ Error al guardar atributos') 
    }
  }

  const handleGuardarConfig = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/empresas/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key_openai: openaiKey,
          api_key_pinecone: pineconeKey,
          endpoint_productos: endpoint
        }),
      })

      if (!res.ok) throw new Error()
      toast.success('✅ Configuración técnica guardada')
    } catch {
      toast.error('❌ Error al guardar la configuración')
    }
  }

  const handleGuardarIndice = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/empresas/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          indice_pinecone: indiceSeleccionado
        }),
      })
      if (!res.ok) throw new Error()
      toast.success('✅ Índice guardado correctamente')
    } catch {
      toast.error('❌ Error al guardar el índice')
    }
  }

  const handleSincronizarProductos = async () => {
    if (!openaiKey || !pineconeKey || !endpoint || !indiceSeleccionado) {
      toast.error('❌ Faltan datos necesarios para sincronizar')
      return
    }
  
    setSyncLoading(true)
    setSyncMessage('🔄 Contando productos del endpoint...')
    setProductosLog([])
    setProgreso(0)
    setProductosRecibidos(0)
  
    try {
      // 1. Obtener la cantidad total de productos del endpoint de la empresa
      const resProductos = await fetch(endpoint)
      const productos = await resProductos.json()
  
      if (!Array.isArray(productos)) {
        toast.error('❌ El endpoint de productos no devuelve un arreglo válido')
        setSyncLoading(false)
        return
      }
  
      const total = productos.length
      setTotalEsperado(total)
  
      // 2. Abrir WebSocket para recibir progreso
      const ws = new WebSocket(`ws://localhost:8000/ws/sync/${id}`)
      wsRef.current = ws
  
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
  
        if (data.title && data.price && data.category) {
          setProductosLog(prev => [...prev, data])
  
          setProductosRecibidos(prev => {
            const nuevoTotal = prev + 1
            const progresoCalculado = Math.min((nuevoTotal / Math.max(total, 1)) * 100, 100)
            setProgreso(progresoCalculado)
            return nuevoTotal
          })
        }
      }
  
      ws.onopen = async () => {
        // 3. Lanzar la sincronización
        const resSync = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/sync/empresa-productos/${id}`, {
          method: 'POST',
        })
  
        const data = await resSync.json()
        if (!resSync.ok) {
          setSyncMessage('❌ Error al sincronizar productos')
          setSyncLoading(false)
          ws.close()
          return
        }
  
        setSyncMessage('✅ Sincronización en curso...')
      }
  
      ws.onerror = () => {
        setSyncMessage('❌ Error en la conexión WebSocket')
        setSyncLoading(false)
      }
  
      ws.onclose = () => {
        setSyncMessage('✅ Sincronización finalizada.')
        setSyncLoading(false)
      }
  
    } catch (err) {
      toast.error('❌ Error al contar productos del endpoint')
      setSyncLoading(false)
    }
  }      

  const handleEliminarProductos = async () => {
    if (!pineconeKey || !indiceSeleccionado) {
      toast.error('❌ Falta la clave Pinecone o el índice seleccionado')
      return
    }

    setDeleteMessage('🗑️ Eliminando productos del índice...')

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/sync/empresa-productos/${id}`, {
        method: 'DELETE',
      })

      const data = await res.json()

      if (!res.ok) throw new Error(data.detail || 'Error al eliminar productos')

      setDeleteMessage(`✅ ${data.message || 'Productos eliminados correctamente.'}`)
    } catch {
      setDeleteMessage('❌ Error al eliminar productos')
    }
  }

  if (loading) return <CircularProgress />

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>
        Configuración Técnica - {empresa?.nombre_empresa}
      </Typography>

      <Divider sx={{ my: 2 }} />

      <Box display="flex" flexDirection="column" gap={3}>
        <TextField label="API Key OpenAI" value={openaiKey} onChange={(e) => setOpenaiKey(e.target.value)} fullWidth />
        <TextField label="API Key Pinecone" value={pineconeKey} onChange={(e) => setPineconeKey(e.target.value)} fullWidth />
        <TextField label="Endpoint de productos" value={endpoint} onChange={(e) => setEndpoint(e.target.value)} fullWidth />

        <Button variant="contained" onClick={handleGuardarConfig}>Guardar configuración</Button>

        <FormControl fullWidth>
          <InputLabel>Índice de Pinecone</InputLabel>
          <Select value={indiceSeleccionado} label="Índice de Pinecone" onChange={(e) => setIndiceSeleccionado(e.target.value)}>
            {indices.map((nombre) => (
              <MenuItem key={nombre} value={nombre}>{nombre}</MenuItem>
            ))}
          </Select>
        </FormControl>

        <Box>
          <Typography variant="h6">🧩 Atributos a sincronizar</Typography>
          {atributosDisponibles.map(attr => (
            <label key={attr} style={{ display: 'block' }}>
              <input
                type="checkbox"
                checked={atributosSeleccionados.includes(attr)}
                onChange={(e) => {
                  if (e.target.checked) {
                    setAtributosSeleccionados(prev => [...prev, attr])
                  } else {
                    setAtributosSeleccionados(prev => prev.filter(a => a !== attr))
                  }
                }}
              />
              {attr}
            </label>
          ))}
          <Button variant="outlined" sx={{ mt: 1 }} onClick={handleGuardarAtributos}>Guardar atributos seleccionados</Button>
        </Box>

        <Button variant="outlined" onClick={handleGuardarIndice}>Guardar índice seleccionado</Button>

        <Button variant="contained" color="secondary" onClick={handleSincronizarProductos} disabled={syncLoading}>
          {syncLoading ? 'Sincronizando...' : 'Sincronizar productos ahora'}
        </Button>

        {syncMessage && <Typography variant="body1" color="primary">{syncMessage}</Typography>}

        {syncLoading && (
          <Box mt={2}>
            <Typography variant="body2">Progreso: {Math.round(progreso)}%</Typography>
            <Box sx={{ width: '100%', backgroundColor: '#eee', borderRadius: 2 }}>
              <Box
                sx={{
                  width: `${Math.min(progreso, 100)}%`,
                  height: 10,
                  backgroundColor: '#1976d2',
                  borderRadius: 2,
                  transition: 'width 0.3s ease-in-out',
                }}
              />
            </Box>
          </Box>
        )}

        {productosLog.length > 0 && (
          <Box mt={2}>
            <Typography variant="h6">🧾 Productos sincronizados:</Typography>
            <ul>
              {productosLog.map((p, idx) => (
                <li key={idx}><strong>{p.title}</strong> - ${p.price} ({p.category})</li>
              ))}
            </ul>
          </Box>
        )}

        <Button variant="outlined" color="error" onClick={handleEliminarProductos}>
          Eliminar productos del índice
        </Button>

        {deleteMessage && (
          <Typography variant="body2" color="error">{deleteMessage}</Typography>
        )}
      </Box>
    </Paper>
  )
}
