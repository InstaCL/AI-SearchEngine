'use client'

import { Box, Button, CircularProgress, Paper, TextField, Typography } from '@mui/material'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'

const schema = z.object({
  correo: z.string().email('Correo inválido'),
  password: z.string().min(6, 'Mínimo 6 caracteres'),
})

type FormData = z.infer<typeof schema>

export default function LoginAdminPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      const result = await res.json()

      if (!res.ok || !result.access_token) {
        throw new Error(result.detail || 'Error en el login')
      }

      // Guardar como cookie para el middleware
      document.cookie = `admin_token=${result.access_token}; path=/; max-age=86400; SameSite=Lax`

      toast.success('✅ Sesión de administrador iniciada')
      router.push('/ia-control-panel/dashboard')
    } catch (error: any) {
      toast.error(error.message || '❌ Error al iniciar sesión')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Paper sx={{ maxWidth: 420, mx: 'auto', mt: 8, p: 4 }}>
      <Typography variant="h5" gutterBottom>Iniciar Sesión - Administrador</Typography>

      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField
          label="Correo"
          fullWidth
          margin="normal"
          {...register('correo')}
          error={!!errors.correo}
          helperText={errors.correo?.message}
        />

        <TextField
          label="Contraseña"
          type="password"
          fullWidth
          margin="normal"
          {...register('password')}
          error={!!errors.password}
          helperText={errors.password?.message}
        />

        <Box mt={3}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Iniciar sesión'}
          </Button>
        </Box>
      </form>
    </Paper>
  )
}
