<script setup>
import { computed, ref } from 'vue'
import CourseEnrollmentCard from '../components/CourseEnrollmentCard.vue'
import CourseGallery from '../components/CourseGallery.vue'
import CoursePageShell from '../components/CoursePageShell.vue'

const props = defineProps({ course: { type: Object, default: null }, loading: { type: Boolean, default: false }, error: { type: String, default: '' }, paymentBusy: { type: Boolean, default: false }, isEnrolled: { type: Boolean, default: false }, currentUser: { type: Object, default: null }, savedCourseIds: { type: Array, default: () => [] } })
const emit = defineEmits(['navigate', 'purchase', 'retry', 'logout', 'toggle-save'])
const copied = ref(false)
const courseImages = computed(() => props.course?.thumbnail_url ? [{ src: props.course.thumbnail_url, alt: `${props.course.title} 강의 이미지` }] : [{ label: props.course?.level ? `${props.course.level} 강의` : '배우고 성장하는 시간' }])
const duration = computed(() => {
  const value = props.course?.duration
  if (!value) return '시간 정보 없음'
  if (typeof value !== 'number') return String(value)
  const hours = Math.floor(value / 60)
  const minutes = value % 60
  return [hours ? `${hours}시간` : '', minutes ? `${minutes}분` : ''].filter(Boolean).join(' ') || '시간 정보 없음'
})
const hasPrice = computed(() => props.course?.price !== null && props.course?.price !== undefined && props.course?.price !== '' && Number.isFinite(Number(props.course.price)))
const price = computed(() => hasPrice.value ? Number(props.course.price) : '가격 정보 없음')
const isSaved = computed(() => props.course ? props.savedCourseIds.includes(props.course.id) : false)

async function shareCourse() {
  const url = window.location.href
  try {
    if (navigator.share) await navigator.share({ title: props.course?.title, url })
    else if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(url)
    else return
    copied.value = true
    window.setTimeout(() => { copied.value = false }, 1800)
  } catch {
    copied.value = false
  }
}
</script>

<template>
  <CoursePageShell active="detail" :current-user="currentUser" @navigate="emit('navigate', $event)" @logout="emit('logout')">
    <section class="course-detail-page">
      <a class="course-detail-page__back" href="/courses" @click.prevent="emit('navigate', '/courses')">← 강의 목록으로</a>
      <div v-if="loading" class="course-detail-page__state" role="status"><span class="course-detail-page__spinner"></span><p>강의 정보를 불러오고 있어요.</p></div>
      <div v-else-if="error" class="course-detail-page__state" role="alert"><h1>강의를 찾을 수 없어요</h1><p>{{ error }}</p><button type="button" @click="emit('retry')">다시 불러오기</button></div>
      <article v-else-if="course" class="course-detail">
        <div class="course-detail__heading"><div><p class="course-detail__eyebrow">{{ course.category || '온라인 클래스' }}</p><h1>{{ course.title }}</h1><p class="course-detail__instructor">{{ course.instructor_name || '강사 정보 준비 중' }}</p></div><div class="course-detail__actions"><button type="button" @click="shareCourse">{{ copied ? '링크 복사됨' : '공유' }}</button><button type="button" :aria-pressed="isSaved" @click="emit('toggle-save', course)">{{ isSaved ? '♥ 찜 완료' : '♡ 찜하기' }}</button></div></div>
        <CourseGallery :images="courseImages" :title="course.title" />
        <div class="course-detail__body"><div class="course-detail__copy"><h2>강의 소개</h2><p>{{ course.description || '강의 소개가 준비 중입니다.' }}</p><div class="course-detail__rule"></div><h2>이 강의에서 배워요</h2><ul><li>강의 핵심 개념을 차근차근 학습합니다.</li><li>실습을 통해 배운 내용을 직접 적용합니다.</li><li>내 속도에 맞춰 원하는 시간에 수강합니다.</li></ul></div><CourseEnrollmentCard :price="price" :duration="duration" :level="course.level || ''" :action-label="paymentBusy ? '결제 준비 중…' : isEnrolled ? '수강 중인 강의' : '강의 구매하기'" :disabled="paymentBusy" @enroll="emit('purchase')" /></div>
      </article>
    </section>
  </CoursePageShell>
</template>

<style scoped>
.course-detail-page__back{display:inline-block;margin:2px 0 22px;color:#444;font-size:13px;text-decoration:none}.course-detail-page__heading{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:20px}.course-detail-page__heading h1{margin:0;font-size:clamp(24px,3vw,32px);letter-spacing:-1px}.course-detail-page__eyebrow{margin:0 0 7px;color:#666;font-size:12px}.course-detail-page__instructor{margin:9px 0 0;color:#555;font-size:13px}.course-detail-page__actions{display:flex;gap:10px}.course-detail-page__actions button{padding:9px 12px;border:0;border-radius:7px;background:#f5f5f5;color:#222;font:inherit;font-size:12px;text-decoration:underline;cursor:pointer}.course-detail__body{display:grid;grid-template-columns:minmax(0,1fr) 350px;gap:60px;margin:33px auto 0;max-width:1080px}.course-detail__copy h2{margin:0;font-size:20px}.course-detail__copy p,.course-detail__copy li{color:#444;font-size:14px;line-height:1.8}.course-detail__copy p{white-space:pre-line}.course-detail__copy ul{padding-left:20px}.course-detail__rule{height:1px;margin:24px 0;background:#e8e8e8}.course-detail-page__state{min-height:360px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.course-detail-page__state h1{font-size:20px}.course-detail-page__state p{color:#666;font-size:13px}.course-detail-page__state button{margin-top:12px;padding:10px 16px;border:0;border-radius:7px;background:#ffff00;font:inherit;font-size:12px;font-weight:700;cursor:pointer}.course-detail-page__spinner{width:26px;height:26px;border:2px solid #eee;border-top-color:#222;border-radius:50%;animation:detail-spin .8s linear infinite}@keyframes detail-spin{to{transform:rotate(360deg)}}@media(max-width:800px){.course-detail__body{grid-template-columns:1fr;gap:28px}.course-detail__body :deep(.course-enrollment){order:-1}}@media(max-width:560px){.course-detail-page__heading{align-items:flex-start;flex-direction:column}.course-detail-page__actions{align-self:flex-end;margin-top:-4px}}@media(prefers-reduced-motion:reduce){.course-detail-page__spinner{animation-duration:.01ms}}
</style>
