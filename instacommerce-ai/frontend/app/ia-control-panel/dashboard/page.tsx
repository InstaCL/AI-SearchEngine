'use client'

import { Box, Typography, Grid, Card, CardContent, Button } from '@mui/material'
import { useRouter } from 'next/navigation'
import { toast } from 'react-hot-toast'

const DashboardHome = () => {
  const router = useRouter()

  const handleLogout = () => {
    document.cookie = 'admin_token=; path=/; max-age=0'
    toast.success('🚪 Sesión de administrador cerrada')
    router.push('/ia-control-panel/login')
  }

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
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6">Empresas Registradas</Typography>
              <Typography variant="h4">12</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6">Productos Indexados</Typography>
              <Typography variant="h4">325</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6">Conversaciones Hoy</Typography>
              <Typography variant="h4">48</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default DashboardHome
