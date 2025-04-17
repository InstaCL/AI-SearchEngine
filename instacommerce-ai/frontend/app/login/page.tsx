'use client'

import { Box, Button, Paper, TextField, Typography, CircularProgress } from '@mui/material'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'

const schema = z.object({
  correo: z.string().email({ message: "Correo inválido" }),
  contraseña: z.string().min(6, { message: "Mínimo 6 caracteres" }),
})

type FormData = z.infer<typeof schema>

export default function LoginEmpresaPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/empresa/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      const result = await res.json()
      if (!res.ok || !result.token) throw new Error(result.detail || "Error al iniciar sesión")

      // Guardar token y redirigir
      localStorage.setItem('token', result.token)
      toast.success('✅ Sesión iniciada correctamente')
      router.push('/dashboard')  // Redirigir al dashboard privado
    } catch (error) {
      toast.error(`❌ ${error}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Paper sx={{ maxWidth: 420, mx: 'auto', mt: 8, p: 4 }}>
      <Typography variant="h5" gutterBottom>Iniciar Sesión - Clientes</Typography>

      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField
          label="Correo corporativo"
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
          {...register('contraseña')}
          error={!!errors.contraseña}
          helperText={errors.contraseña?.message}
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
