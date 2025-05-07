'use client'

import { useEffect, useState } from 'react'
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  CircularProgress,
} from '@mui/material'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import BusinessIcon from '@mui/icons-material/Business'
import Inventory2Icon from '@mui/icons-material/Inventory2'
import ForumIcon from '@mui/icons-material/Forum'

interface AdminMetricas {
  total_empresas: number
  productos_indexados: number
  conversaciones_hoy: number
}

const DashboardHome = () => {
  const router = useRouter()
  const [metricas, setMetricas] = useState<AdminMetricas | null>(null)
  const [loading, setLoading] = useState(true)

  const getToken = () => {
    const match = document.cookie.match(/(^| )admin_token=([^;]+)/)
    return match ? match[2] : null
  }

  useEffect(() => {
    const token = getToken()

    if (!token) {
      toast.error('⚠️ Token de administrador no encontrado')
      router.push('/ia-control-panel/login')
      return
    }

    const fetchMetricas = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/metricas-globales`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!res.ok) throw new Error('❌ Error al cargar métricas')
        const data = await res.json()
        console.log('[✔️] Métricas recibidas:', data)
        setMetricas(data)
      } catch (err) {
        toast.error('❌ Error al obtener métricas del sistema')
      } finally {
        setLoading(false)
      }
    }

    fetchMetricas()
  }, [router])

  const handleLogout = () => {
    document.cookie = 'admin_token=; path=/; max-age=0'
    toast.success('🚪 Sesión de administrador cerrada')
    router.push('/ia-control-panel/login')
  }

  if (loading) return <CircularProgress />

  return (
    <Box sx={{ position: 'relative' }}>
      <Box sx={{ position: 'absolute', top: 0, right: 0 }}>
        <Button variant="outlined" color="error" onClick={handleLogout} sx={{ mt: 1, mr: 1 }}>
          Cerrar sesión
        </Button>
      </Box>

      <Typography variant="h4" gutterBottom>
        👋 Bienvenido al Panel IA de Instacommerce
      </Typography>

      <Typography variant="body1" gutterBottom>
        Aquí podrás gestionar tus empresas, revisar métricas, configurar tu agente de IA y monitorear las interacciones de los clientes.
      </Typography>

      <Grid container spacing={3} mt={3}>
        <Grid item xs={12} md={4}>
          <Card sx={{ backgroundColor: '#e3f2fd' }} elevation={4}>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <BusinessIcon fontSize="large" color="primary" />
                <Box>
                  <Typography variant="h6">Empresas Registradas</Typography>
                  <Typography variant="h4">
                    {metricas?.total_empresas ?? '...'}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ backgroundColor: '#e8f5e9' }} elevation={4}>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <Inventory2Icon fontSize="large" color="success" />
                <Box>
                  <Typography variant="h6">Productos Indexados</Typography>
                  <Typography variant="h4">
                    {metricas?.productos_indexados ?? '...'}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ backgroundColor: '#fff3e0' }} elevation={4}>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <ForumIcon fontSize="large" color="warning" />
                <Box>
                  <Typography variant="h6">Conversaciones Hoy</Typography>
                  <Typography variant="h4">
                    {metricas?.conversaciones_hoy ?? '...'}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default DashboardHome
