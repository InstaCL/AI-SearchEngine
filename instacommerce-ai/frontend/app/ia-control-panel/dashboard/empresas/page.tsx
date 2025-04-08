'use client'

import React, { useEffect, useState } from 'react'
import {
  Typography,
  Box,
  Paper,
  Button,
  CircularProgress,
} from '@mui/material'
import { toast } from 'react-hot-toast'
import { useRouter } from 'next/navigation'

interface Empresa {
  id: number
  nombre_empresa: string
  correo: string
  estado_pago: string
}

const EmpresasConfigPage = () => {
  const [empresas, setEmpresas] = useState<Empresa[] | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  const fetchEmpresas = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/empresas`)
      const data = await res.json()

      if (!Array.isArray(data)) {
        throw new Error('La respuesta no es una lista de empresas')
      }

      setEmpresas(data)
    } catch (error) {
      console.error('Error al obtener empresas:', error)
      toast.error('❌ Error al cargar empresas')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEmpresas()
  }, [])

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Gestión de Empresas
      </Typography>

      {loading ? (
        <CircularProgress />
      ) : (
        empresas?.map((empresa) => (
          <Paper key={empresa.id} elevation={3} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6">{empresa.nombre_empresa}</Typography>
            <Typography>Correo: {empresa.correo}</Typography>
            <Typography>Estado: {empresa.estado_pago || 'Sin definir'}</Typography>

            <Box mt={2}>
              <Button
                variant="contained"
                onClick={() => router.push(`/ia-control-panel/dashboard/empresas/${empresa.id}`)}
              >
                Configurar Empresa
              </Button>
            </Box>
          </Paper>
        ))
      )}
    </Box>
  )
}

export default EmpresasConfigPage