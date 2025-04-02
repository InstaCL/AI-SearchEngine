'use client'

import { ReactNode } from 'react'
import Sidebar from '../components/Sidebar'
import { Box } from '@mui/material'

interface DashboardLayoutProps {
  children: ReactNode
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  return (
    <Box display="flex">
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        {children}
      </Box>
    </Box>
  )
}

export default DashboardLayout 