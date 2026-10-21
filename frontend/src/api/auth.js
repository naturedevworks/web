import { apiRequest } from './client'

const jsonHeaders = { Accept: 'application/json' }

export function getCurrentUser() {
  return apiRequest('/auth/me', { credentials: 'include', headers: jsonHeaders })
}

export function getKakaoLoginState() {
  return apiRequest('/auth/kakao/state', { credentials: 'include', headers: jsonHeaders })
}

export function completeKakaoLogin(code, state) {
  return apiRequest('/auth/kakao/login', {
    method: 'POST',
    credentials: 'include',
    headers: { ...jsonHeaders, 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, state }),
  })
}

export function logoutUser() {
  return apiRequest('/auth/logout', { method: 'POST', credentials: 'include' })
}

export function registerEmailAccount({ name, email, password }) {
  return apiRequest('/auth/email/register', {
    method: 'POST',
    credentials: 'include',
    headers: { ...jsonHeaders, 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password }),
  })
}

export function loginWithEmail({ email, password }) {
  return apiRequest('/auth/email/login', {
    method: 'POST',
    credentials: 'include',
    headers: { ...jsonHeaders, 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
}
