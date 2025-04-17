import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value

  // Rutas protegidas
  const protectedRoutes = ['/dashboard']

  const { pathname } = request.nextUrl
  const isProtected = protectedRoutes.some(route => pathname.startsWith(route))

  if (isProtected && !token) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('callbackUrl', pathname) // guardar destino original
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

// Aplicar middleware solo a rutas protegidas
export const config = {
  matcher: ['/dashboard/:path*'],
}
