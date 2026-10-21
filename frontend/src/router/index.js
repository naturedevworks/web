export function resolveRoute(pathname) {
  if (pathname === '/login') return { name: 'login' }
  if (pathname === '/signup') return { name: 'signup' }
  if (pathname === '/auth/kakao/callback') return { name: 'kakao-callback' }
  if (pathname === '/payment/success') return { name: 'payment-success' }
  if (pathname === '/my/courses' || pathname === '/my' || pathname === '/mypage') return { name: 'my-courses' }
  const learningMatch = pathname.match(/^\/my\/courses\/(\d+)\/learn\/?$/)
  if (learningMatch) return { name: 'learning', courseId: learningMatch[1] }
  if (pathname === '/checkout') return { name: 'checkout' }
  const courseMatch = pathname.match(/^\/courses\/([^/]+)\/?$/)
  if (courseMatch) return { name: 'detail', courseId: decodeURIComponent(courseMatch[1]) }
  return { name: 'catalog' }
}
