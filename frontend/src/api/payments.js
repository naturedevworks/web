import { apiRequest } from './client'

const jsonHeaders = { Accept: 'application/json' }

export function listEnrollments() {
  return apiRequest('/payments/enrollments', { credentials: 'include', headers: jsonHeaders })
}

export function getEnrollment(courseId) {
  return apiRequest(`/payments/enrollments/${encodeURIComponent(courseId)}`, { credentials: 'include', headers: jsonHeaders })
}

export function createCheckout(courseId) {
  return apiRequest('/payments/checkout', {
    method: 'POST',
    credentials: 'include',
    headers: { ...jsonHeaders, 'Content-Type': 'application/json' },
    body: JSON.stringify({ course_id: courseId }),
  })
}

export function confirmPayment(paymentId) {
  return apiRequest('/payments/confirm', {
    method: 'POST',
    credentials: 'include',
    headers: { ...jsonHeaders, 'Content-Type': 'application/json' },
    body: JSON.stringify({ payment_id: paymentId }),
  })
}
