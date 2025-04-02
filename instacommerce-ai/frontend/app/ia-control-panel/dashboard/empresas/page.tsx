'use client'

import { useEffect, useState } from 'react'
import {
  Container,
  Typography,
  Paper,
  Box,
  TextField,
  Button,
  CircularProgress,
} from '@mui/material'
import { toast } from 'react-hot-toast'

interface Empresa {
  id: number
  nombre_empresa: string
  correo: string
  api_key_openai: string
  api_key_pinecone: string
  endpoint_productos: string
}

const EmpresasConfigPage = () => {
  const [empresas, setEmpresas] = useState<Empresa[]>([])
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    const fetchEmpresas = async () => {
      setLoading(true)
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/empresas`)
        const data = await res.json()
        setEmpresas(Array.isArray(data) ? data : [])
      } catch (error) {
        toast.error('Error al cargar las empresas')
      } finally {
        setLoading(false)
      }
    }

    fetchEmpresas()
  }, [])

  const handleChange = (index: number, field: keyof Empresa, value: string) => {
    const actualizadas = [...empresas]
    actualizadas[index][field] = value
    setEmpresas(actualizadas)
  }

  const handleGuardar = async (empresa: Empresa) => {
    setSaving(true)
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/configuracion/set`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ empresa_id: empresa.id, ...empresa }),
      })
      if (!res.ok) throw new Error('Error al guardar configuración')
      toast.success(`✅ Configuración guardada para ${empresa.nombre_empresa}`)
    } catch (err) {
      toast.error(`❌ Error al guardar para ${empresa.nombre_empresa}`)
    } finally {
      setSaving(false)
    }
  }

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Gestión de Empresas
      </Typography>
      {loading ? (
        <CircularProgress />
      ) : (
        empresas.map((empresa, index) => (
          <Paper key={empresa.id} elevation={3} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6">{empresa.nombre_empresa}</Typography>
            <Box display="flex" flexDirection="column" gap={2} mt={2}>
              <TextField
                label="API Key OpenAI"
                value={empresa.api_key_openai || ''}
                onChange={(e) => handleChange(index, 'api_key_openai', e.target.value)}
                fullWidth
              />
              <TextField
                label="API Key Pinecone"
                value={empresa.api_key_pinecone || ''}
                onChange={(e) => handleChange(index, 'api_key_pinecone', e.target.value)}
                fullWidth
              />
              <TextField
                label="Endpoint de Productos"
                value={empresa.endpoint_productos || ''}
                onChange={(e) => handleChange(index, 'endpoint_productos', e.target.value)}
                fullWidth
              />
              <Button
                variant="contained"
                color="primary"
                onClick={() => handleGuardar(empresa)}
                disabled={saving}
              >
                {saving ? 'Guardando...' : 'Guardar Configuración'}
              </Button>
            </Box>
          </Paper>
        ))
      )}
    </Container>
  )
}

export default EmpresasConfigPage