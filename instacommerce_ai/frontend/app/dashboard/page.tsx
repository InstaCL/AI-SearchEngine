'use client'

import { useEffect, useState } from 'react'
import {
  Box,
  Typography,
  CircularProgress,
  Paper,
  Divider,
  Grid,
  Card,
  CardContent,
  Button,
} from '@mui/material'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import InventoryIcon from '@mui/icons-material/Inventory'
import ForumIcon from '@mui/icons-material/Forum'
import TodayIcon from '@mui/icons-material/Today'

interface Empresa {
  id: number
  nombre_empresa: string
  correo: string
  rut: string
  tipo_productos: string
  estado_pago: string
}

interface Metricas {
  total_productos: number
  total_conversaciones: number
  conversaciones_hoy: number
}

export default function DashboardCliente() {
  const [empresa, setEmpresa] = useState<Empresa | null>(null)
  const [metricas, setMetricas] = useState<Metricas | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  const getToken = (): string | null => {
    const match = document.cookie.match(/(^| )token=([^;]+)/)
    return match ? match[2] : null
  }

  useEffect(() => {
    const token = getToken()
    if (!token) {
      toast.error('⚠️ Token no encontrado')
      router.push('/login')
      return
    }

    const fetchDatos = async () => {
      try {
        const headers = {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        }

        const perfilRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/empresa/perfil`, { headers })
        const perfilData = await perfilRes.json()
        if (!perfilRes.ok) throw new Error(perfilData.detail)

        const metricasRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/empresa/metricas`, { headers })
        const metricasData = await metricasRes.json()
        if (!metricasRes.ok) throw new Error(metricasData.detail)

        setEmpresa(perfilData)
        setMetricas(metricasData)
      } catch {
        toast.error('❌ Sesión no válida o error al cargar datos')
        router.push('/login')
      } finally {
        setLoading(false)
      }
    }

    fetchDatos()
  }, [router])

  const logout = () => {
    document.cookie = 'token=; Max-Age=0; path=/'
    router.push('/login')
  }

  if (loading) return <CircularProgress />

  return (
    <Paper sx={{ p: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">📊 Panel de Cliente</Typography>
        <Button onClick={logout} variant="outlined" color="error">
          Cerrar sesión
        </Button>
      </Box>

      <Divider sx={{ mb: 3 }} />

      {empresa && metricas ? (
        <>
          <Box mb={3}>
            <Typography variant="body1"><strong>🏢 Empresa:</strong> {empresa.nombre_empresa}</Typography>
            <Typography variant="body1"><strong>📧 Correo:</strong> {empresa.correo}</Typography>
            <Typography variant="body1"><strong>🆔 RUT:</strong> {empresa.rut}</Typography>
            <Typography variant="body1"><strong>🛍️ Rubro:</strong> {empresa.tipo_productos}</Typography>
            <Typography variant="body1"><strong>💳 Estado de pago:</strong> {empresa.estado_pago}</Typography>
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Card sx={{ bgcolor: '#f3f4f6' }} elevation={4}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={2}>
                    <InventoryIcon fontSize="large" color="primary" />
                    <Box>
                      <Typography variant="h6">Productos sincronizados</Typography>
                      <Typography variant="h4">{metricas.total_productos}</Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={4}>
              <Card sx={{ bgcolor: '#e8f5e9' }} elevation={4}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={2}>
                    <ForumIcon fontSize="large" color="success" />
                    <Box>
                      <Typography variant="h6">Conversaciones totales</Typography>
                      <Typography variant="h4">{metricas.total_conversaciones}</Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={4}>
              <Card sx={{ bgcolor: '#fff3e0' }} elevation={4}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={2}>
                    <TodayIcon fontSize="large" color="warning" />
                    <Box>
                      <Typography variant="h6">Conversaciones hoy</Typography>
                      <Typography variant="h4">{metricas.conversaciones_hoy}</Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </>
      ) : (
        <Typography variant="body2" color="error">
          No se pudo cargar la información del perfil o métricas.
        </Typography>
      )}
    </Paper>
  )
}
