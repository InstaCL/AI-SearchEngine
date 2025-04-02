'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import {
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  Box,
  Alert,
} from '@mui/material'

const LoginPage = () => {
  const [usuario, setUsuario] = useState('')
  const [password, setPassword] = useState('')
  const [errorMsg, setErrorMsg] = useState('')
  const router = useRouter()

  const baseUrl = process.env.NEXT_PUBLIC_API_URL
  console.log('🔗 Conectando con backend en:', baseUrl)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    setErrorMsg('') // Limpia errores anteriores

    try {
      const res = await fetch(`${baseUrl}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario, password }),
      })

      const data = await res.json()

      if (!res.ok) {
        setErrorMsg(data.detail || 'Error al iniciar sesión')
        return
      }

      // Aquí podrías guardar info en localStorage o contexto si fuera necesario
      router.push('/ia-control-panel/dashboard')
    } catch (error) {
      setErrorMsg('❌ No se pudo conectar al servidor')
    }
  }

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ padding: 4, marginTop: 10, borderRadius: 3 }}>
        <Typography variant="h4" gutterBottom textAlign="center">
          Panel IA -- Login
        </Typography>

        {errorMsg && <Alert severity="error">{errorMsg}</Alert>}

        <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection="column" gap={2} mt={2}>
          <TextField
            label="Correo o alias"
            variant="outlined"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
            required
          />
          <TextField
            label="Contraseña"
            type="password"
            variant="outlined"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button type="submit" variant="contained" color="primary">
            Iniciar sesión
          </Button>
        </Box>
      </Paper>
    </Container>
  )
}

export default LoginPage
