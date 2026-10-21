<script setup>
import CoursePageShell from '../components/CoursePageShell.vue'

defineProps({ courses: { type: Array, default: () => [] }, loading: { type: Boolean, default: false }, error: { type: String, default: '' }, currentUser: { type: Object, default: null } })
const emit = defineEmits(['navigate', 'retry', 'logout'])
</script>

<template>
  <CoursePageShell active="my" :current-user="currentUser" @navigate="emit('navigate', $event)" @logout="emit('logout')">
    <section class="my-courses-view"><div class="my-courses-view__heading"><div><p>MY LEARNING</p><h1>내 강의</h1></div><a href="/courses" @click.prevent="emit('navigate', '/courses')">강의 더 찾아보기</a></div>
      <div v-if="loading" class="my-courses-view__state" role="status">수강 목록을 불러오고 있어요.</div>
      <div v-else-if="error" class="my-courses-view__state" role="alert"><h2>수강 목록을 불러오지 못했어요</h2><p>{{ error }}</p><button type="button" @click="emit('retry')">다시 불러오기</button></div>
      <div v-else-if="courses.length === 0" class="my-courses-view__state"><h2>아직 수강 중인 강의가 없어요</h2><p>관심 있는 강의를 찾아 첫 수강을 시작해 보세요.</p><button type="button" @click="emit('navigate', '/courses')">강의 둘러보기</button></div>
      <div v-else class="my-courses-view__grid"><article v-for="course in courses" :key="course.id" class="my-courses-view__card"><button class="my-courses-view__cover" type="button" :aria-label="`${course.title} 학습하기`" @click="emit('navigate', `/my/courses/${course.id}/learn`)"><img v-if="course.thumbnail_url" :src="course.thumbnail_url" :alt="`${course.title} 강의 이미지`" /><span v-else>{{ course.level || '온라인 클래스' }}</span></button><div class="my-courses-view__copy"><p>{{ course.instructor_name || '강사' }}<span v-if="course.enrolled_at"> · {{ course.enrolled_at }}</span></p><h2>{{ course.title }}</h2><button type="button" @click="emit('navigate', `/my/courses/${course.id}/learn`)">이어서 학습하기 <span aria-hidden="true">→</span></button></div></article></div>
    </section>
  </CoursePageShell>
</template>

<style scoped>
.my-courses-view__heading{display:flex;align-items:flex-end;justify-content:space-between;margin:5px 0 26px}.my-courses-view__heading p{margin:0 0 7px;color:#666;font-size:11px}.my-courses-view__heading h1{margin:0;font-size:30px;letter-spacing:-.8px}.my-courses-view__heading a{font-size:12px;text-decoration:underline}.my-courses-view__state{min-height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.my-courses-view__state h2{margin:0;font-size:19px}.my-courses-view__state p{color:#666;font-size:13px}.my-courses-view__state button,.my-courses-view__copy>button{min-height:40px;margin-top:12px;padding:0 14px;border:0;border-radius:8px;background:#ffff00;color:#111;font:inherit;font-size:12px;font-weight:700;cursor:pointer}.my-courses-view__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}.my-courses-view__card{overflow:hidden;border:1px solid #e5e5e5;border-radius:13px;background:#fff}.my-courses-view__cover{width:100%;aspect-ratio:1.6;display:grid;place-items:center;overflow:hidden;padding:0;border:0;background:#f2f0c2;color:#394638;font-weight:700;cursor:pointer}.my-courses-view__cover img{width:100%;height:100%;object-fit:cover}.my-courses-view__copy{padding:16px}.my-courses-view__copy p{margin:0;color:#666;font-size:11px}.my-courses-view__copy h2{margin:8px 0 14px;font-size:16px}.my-courses-view__copy>button{margin:0}@media(max-width:800px){.my-courses-view__grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.my-courses-view__heading h1{font-size:25px}.my-courses-view__grid{gap:13px}.my-courses-view__copy{padding:12px}.my-courses-view__copy h2{font-size:14px}}
</style>
