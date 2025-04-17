'use client'

import { useEffect, useState } from 'react'
import {
  Box,
  Typography,
  CircularProgress,
  Paper,
  Divider,
} from '@mui/material'
import { useRouter } from 'next/navigation'
import { toast } from 'react-hot-toast'

interface Empresa {
  id: number
  nombre_empresa: string
  correo: string
  rut: string
  tipo_productos: string
  estado_pago: string
}

export default function DashboardCliente() {
  const [empresa, setEmpresa] = useState<Empresa | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')

    if (!token) {
      router.push('/login')
      return
    }

    const fetchPerfil = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/empresa/perfil`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!res.ok) throw new Error()

        const data = await res.json()
        setEmpresa(data)
      } catch {
        toast.error('❌ Sesión no válida o expirada')
        router.push('/login')
      } finally {
        setLoading(false)
      }
    }

    fetchPerfil()
  }, [router])

  if (loading) return <CircularProgress />

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>
        Bienvenido(a) al Panel de Cliente
      </Typography>

      <Divider sx={{ my: 2 }} />

      {empresa ? (
        <Box>
          <Typography variant="body1"><strong>Empresa:</strong> {empresa.nombre_empresa}</Typography>
          <Typography variant="body1"><strong>Correo:</strong> {empresa.correo}</Typography>
          <Typography variant="body1"><strong>RUT:</strong> {empresa.rut}</Typography>
          <Typography variant="body1"><strong>Giro o Rubro:</strong> {empresa.tipo_productos}</Typography>
          <Typography variant="body1"><strong>Estado de pago:</strong> {empresa.estado_pago}</Typography>

          <Box mt={3}>
            <Typography variant="body2" color="text.secondary">
              Muy pronto verás tus métricas, historial de conversaciones y configuración del chatbot aquí. 🚀
            </Typography>
          </Box>
        </Box>
      ) : (
        <Typography variant="body2" color="error">
          No se pudo cargar la información de la empresa.
        </Typography>
      )}
    </Paper>
  )
}
