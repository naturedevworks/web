import { apiRequest } from './client'

const jsonHeaders = { Accept: 'application/json' }

export function listCourses() {
  return apiRequest('/courses', { headers: jsonHeaders })
}

export function getCourse(courseId) {
  return apiRequest(`/courses/${encodeURIComponent(courseId)}`, { headers: jsonHeaders })
}
