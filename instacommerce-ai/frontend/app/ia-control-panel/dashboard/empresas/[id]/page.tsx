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
    setSyncMessage('🔄 Iniciando sincronización...')
    setProductosLog([])
    setProgreso(0)

    if (wsRef.current) {
      wsRef.current.close()
    }

    const ws = new WebSocket(`ws://localhost:8000/ws/sync/${id}`)
    wsRef.current = ws

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.title && data.price && data.category) {
        setProductosLog(prev => [...prev, data])
        setProgreso(prev => Math.min(prev + 5, 100))
      }
    }

    ws.onopen = async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/sync/empresa-productos/${id}`, {
        method: 'POST',
      })

      const data = await res.json()
      if (!res.ok) {
        setSyncMessage('❌ Error al sincronizar productos')
      } else {
        setSyncMessage(`✅ ${data.message || 'Sincronización completada correctamente.'}`)
      }

      setSyncLoading(false)
    }

    ws.onerror = () => {
      setSyncMessage('❌ Error en la conexión WebSocket')
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
        <TextField
          label="API Key OpenAI"
          value={openaiKey}
          onChange={(e) => setOpenaiKey(e.target.value)}
          fullWidth
        />

        <TextField
          label="API Key Pinecone"
          value={pineconeKey}
          onChange={(e) => setPineconeKey(e.target.value)}
          fullWidth
        />

        <TextField
          label="Endpoint de productos"
          value={endpoint}
          onChange={(e) => setEndpoint(e.target.value)}
          fullWidth
        />

        <Button variant="contained" onClick={handleGuardarConfig}>
          Guardar configuración
        </Button>

        <FormControl fullWidth>
          <InputLabel>Índice de Pinecone</InputLabel>
          <Select
            value={indiceSeleccionado}
            label="Índice de Pinecone"
            onChange={(e) => setIndiceSeleccionado(e.target.value)}
          >
            {indices.map((nombre) => (
              <MenuItem key={nombre} value={nombre}>
                {nombre}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button variant="outlined" onClick={handleGuardarIndice}>
          Guardar índice seleccionado
        </Button>

        <Button
          variant="contained"
          color="secondary"
          onClick={handleSincronizarProductos}
          disabled={syncLoading}
        >
          {syncLoading ? 'Sincronizando...' : 'Sincronizar productos ahora'}
        </Button>

        {syncMessage && (
          <Typography variant="body1" color="primary">
            {syncMessage}
          </Typography>
        )}

        {syncLoading && (
          <Box mt={2}>
            <Typography variant="body2">Progreso: {Math.round(progreso)}%</Typography>
            <Box sx={{ width: '100%', backgroundColor: '#eee', borderRadius: 2 }}>
              <Box
                sx={{
                  width: `${progreso}%`,
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
                <li key={idx}>
                  <strong>{p.title}</strong> - ${p.price} ({p.category})
                </li>
              ))}
            </ul>
          </Box>
        )}

        <Button
          variant="outlined"
          color="error"
          onClick={handleEliminarProductos}
        >
          Eliminar productos del índice
        </Button>

        {deleteMessage && (
          <Typography variant="body2" color="error">
            {deleteMessage}
          </Typography>
        )}
      </Box>
    </Paper>
  )
}