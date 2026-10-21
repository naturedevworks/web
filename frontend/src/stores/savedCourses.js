import { ref } from 'vue'

const savedCourseIds = ref([])

export function useSavedCoursesStore() {
  function toggle(course) {
    savedCourseIds.value = savedCourseIds.value.includes(course.id)
      ? savedCourseIds.value.filter((id) => id !== course.id)
      : [...savedCourseIds.value, course.id]
  }

  return { savedCourseIds, toggle }
}
