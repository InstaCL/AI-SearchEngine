import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  const clientToken = request.cookies.get('token')?.value
  const adminToken = request.cookies.get('admin_token')?.value

  // 👉 No proteger las páginas públicas de login
  const isClientLogin = pathname === '/login'
  const isAdminLogin = pathname === '/ia-control-panel/login'

  // Cliente: proteger /dashboard, excepto /login
  if (pathname.startsWith('/dashboard') && !isClientLogin && !clientToken) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('callbackUrl', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Admin: proteger /ia-control-panel, excepto /ia-control-panel/login
  if (pathname.startsWith('/ia-control-panel') && !isAdminLogin && !adminToken) {
    const loginUrl = new URL('/ia-control-panel/login', request.url)
    loginUrl.searchParams.set('callbackUrl', pathname)
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

// ✅ Middleware activo solo para rutas protegidas
export const config = {
  matcher: ['/dashboard/:path*', '/ia-control-panel/:path*'],
}
