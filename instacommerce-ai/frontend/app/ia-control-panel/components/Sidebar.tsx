'use client'

import { useRouter, usePathname } from 'next/navigation'
import { Box, Drawer, List, ListItem, ListItemButton, ListItemText, Toolbar, Typography } from '@mui/material'

const menuItems = [
  { label: 'Inicio', path: '/ia-control-panel/dashboard' },
  { label: 'Empresas', path: '/ia-control-panel/dashboard/empresas' },
  { label: 'Historial', path: '/ia-control-panel/dashboard/historial' },
  { label: 'Configuración', path: '/ia-control-panel/dashboard/configuracion' },
]

export const Sidebar = () => {
  const router = useRouter()
  const pathname = usePathname()

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: 240, boxSizing: 'border-box' },
      }}
    >
      <Toolbar>
        <Typography variant="h6">Admin Panel</Typography>
      </Toolbar>
      <Box sx={{ overflow: 'auto' }}>
        <List>
          {menuItems.map((item) => (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                selected={pathname === item.path}
                onClick={() => router.push(item.path)}
              >
                <ListItemText primary={item.label} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  )
}

export default Sidebar
