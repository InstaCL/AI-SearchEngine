'use client'

import {
  Box,
  Button,
  Checkbox,
  CircularProgress,
  FormControlLabel,
  Paper,
  TextField,
  Typography,
} from '@mui/material'
import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import ReCAPTCHA from 'react-google-recaptcha'
import { toast } from 'react-hot-toast'
import { useRouter } from 'next/navigation'

const schema = z.object({
  nombre_empresa: z.string().min(3, 'Debe tener al menos 3 caracteres'),
  correo: z.string().email('Correo inválido'),
  rut: z.string().min(8, 'RUT inválido'),
  rubro: z.string().min(3, 'Debe indicar un rubro válido'),
  password: z.string().min(6, 'Debe tener al menos 6 caracteres'),
  confirm_password: z.string(),
  terms_accepted: z.literal(true, {
    errorMap: () => ({ message: 'Debes aceptar los términos' }),
  }),
  recaptcha_token: z.string().min(1, 'Completa el reCAPTCHA'),
}).refine((data) => data.password === data.confirm_password, {
  message: 'Las contraseñas no coinciden',
  path: ['confirm_password'],
})

type FormData = z.infer<typeof schema>

export default function RegistroEmpresa() {
  const [loading, setLoading] = useState(false)
  const [recaptchaToken, setRecaptchaToken] = useState<string | null>(null)
  const router = useRouter()
  const [countdown, setCountdown] = useState(3)

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  useEffect(() => {
    if (countdown === 0) {
      router.push('/login')
    }
  }, [countdown, router])

  const onSubmit = async (data: FormData) => {
    setLoading(true)

    const payload = {
      nombre_empresa: data.nombre_empresa,
      correo: data.correo,
      rut: data.rut.replace(/\./g, ''),
      rubro: data.rubro,
      password: data.password,
      recaptcha_token: data.recaptcha_token,
    }

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/registro`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!response.ok) throw new Error('Error al registrar empresa')

      toast.custom(() => (
        <Paper sx={{
          padding: 3,
          border: '2px solid #1976d2',
          backgroundColor: '#fff',
          textAlign: 'center',
          minWidth: 280,
        }}>
          <Typography variant="h6" color="primary">✅ Registro exitoso</Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            Serás redirigido al login en {countdown} segundos...
          </Typography>
        </Paper>
      ), { duration: 3000 })

      // Iniciar cuenta regresiva visual y redirección
      let sec = 3
      const interval = setInterval(() => {
        sec--
        setCountdown(sec)
        if (sec === 0) clearInterval(interval)
      }, 1000)

    } catch {
      toast.error('❌ Error en el registro')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Paper sx={{ maxWidth: 600, mx: 'auto', mt: 6, p: 4 }}>
      <Typography variant="h5" gutterBottom>
        Registro de Empresa
      </Typography>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <TextField
          label="Nombre de la empresa"
          fullWidth
          margin="normal"
          {...register('nombre_empresa')}
          error={!!errors.nombre_empresa}
          helperText={errors.nombre_empresa?.message}
        />
        <TextField
          label="Correo corporativo"
          type="email"
          fullWidth
          margin="normal"
          {...register('correo')}
          error={!!errors.correo}
          helperText={errors.correo?.message}
        />
        <TextField
          label="RUT empresa"
          fullWidth
          margin="normal"
          {...register('rut')}
          error={!!errors.rut}
          helperText={errors.rut?.message}
        />
        <TextField
          label="Rubro o giro"
          fullWidth
          margin="normal"
          {...register('rubro')}
          error={!!errors.rubro}
          helperText={errors.rubro?.message}
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
        <TextField
          label="Confirmar contraseña"
          type="password"
          fullWidth
          margin="normal"
          {...register('confirm_password')}
          error={!!errors.confirm_password}
          helperText={errors.confirm_password?.message}
        />

        <Box my={2}>
          <ReCAPTCHA
            sitekey={process.env.NEXT_PUBLIC_RECAPTCHA_KEY!}
            onChange={(token) => {
              setRecaptchaToken(token)
              setValue('recaptcha_token', token || '')
            }}
          />
          {errors.recaptcha_token && (
            <Typography variant="caption" color="error">
              {errors.recaptcha_token.message}
            </Typography>
          )}
        </Box>

        <FormControlLabel
          control={<Checkbox {...register('terms_accepted')} />}
          label="Acepto los términos y condiciones"
        />
        {errors.terms_accepted && (
          <Typography variant="caption" color="error">
            {errors.terms_accepted.message}
          </Typography>
        )}

        <Button
          variant="contained"
          fullWidth
          type="submit"
          sx={{ mt: 2 }}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Registrar Empresa'}
        </Button>
      </form>
    </Paper>
  )
}
