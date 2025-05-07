import React from 'react';
import { Container } from '@mui/material';

export default function IAControlPanelLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <Container maxWidth="md">{children}</Container>
      </body>
    </html>
  );
}
