<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({ course: { type: Object, required: true }, saved: { type: Boolean, default: false } })
const emit = defineEmits(['select', 'toggle-save'])
const imageFailed = ref(false)
watch(() => props.course.id, () => { imageFailed.value = false })
const hasPrice = computed(() => props.course.price !== null && props.course.price !== undefined && props.course.price !== '' && Number.isFinite(Number(props.course.price)))
const price = computed(() => hasPrice.value ? `${new Intl.NumberFormat('ko-KR').format(Number(props.course.price))}원` : '가격 정보 없음')
const duration = computed(() => {
  const value = props.course.duration
  if (!value) return '온라인 강의'
  const hours = Math.floor(Number(value) / 60)
  const minutes = Number(value) % 60
  return typeof value === 'number' ? `${[hours ? `${hours}시간` : '', minutes ? `${minutes}분` : ''].filter(Boolean).join(' ') || '온라인 강의'}` : `${value} 강의`
})
</script>

<template>
  <article class="course-card">
    <button class="course-card__image-button" type="button" :aria-label="`${course.title} 상세 보기`" @click="emit('select', course)">
      <img v-if="course.thumbnail_url && !imageFailed" class="course-card__image" :src="course.thumbnail_url" :alt="`${course.title} 강의 이미지`" loading="lazy" @error="imageFailed = true" />
      <div v-else class="course-card__placeholder" aria-hidden="true"><span>{{ course.level || '온라인 클래스' }}</span><strong>배움</strong></div>
      <span v-if="course.level" class="course-card__level">{{ course.level }}</span>
    </button>
    <button class="course-card__save" type="button" :aria-pressed="saved" :aria-label="saved ? '찜 취소' : '강의 찜하기'" @click="emit('toggle-save', course)">{{ saved ? '♥' : '♡' }}</button>
    <div class="course-card__details">
      <div class="course-card__meta"><span>{{ course.instructor_name || '강사 정보 준비 중' }}</span><span>{{ duration }}</span></div>
      <h3><button type="button" @click="emit('select', course)">{{ course.title }}</button></h3>
      <p>{{ course.description || '강의 상세에서 커리큘럼과 학습 내용을 확인해 보세요.' }}</p>
      <div class="course-card__footer"><strong>{{ price }}</strong><span>상세 보기 <b aria-hidden="true">→</b></span></div>
    </div>
  </article>
</template>

<style scoped>
.course-card{position:relative;min-width:0;transition:transform .2s ease}.course-card:hover{transform:translateY(-3px)}.course-card__image-button{position:relative;display:block;width:100%;aspect-ratio:1.58;overflow:hidden;padding:0;border:0;border-radius:15px;background:#f2f3f4;text-align:left;cursor:pointer}.course-card__image{width:100%;height:100%;object-fit:cover;transition:transform .28s ease}.course-card__image-button:hover .course-card__image{transform:scale(1.035)}.course-card__placeholder{position:relative;display:flex;width:100%;height:100%;flex-direction:column;align-items:center;justify-content:center;overflow:hidden;gap:10px;background:#f2f3f4;color:#555}.course-card__placeholder:before,.course-card__placeholder:after{position:absolute;width:170px;height:170px;border:1px solid #22222210;border-radius:50%;content:""}.course-card__placeholder:before{top:-100px;right:-48px}.course-card__placeholder:after{bottom:-125px;left:-65px;width:230px;height:230px}.course-card__placeholder span{position:relative;z-index:1;padding:6px 10px;border-radius:999px;background:#fff;font-size:10px;font-weight:700}.course-card__placeholder strong{position:relative;z-index:1;color:#222;font-size:clamp(23px,3vw,34px);font-weight:900;letter-spacing:-1.7px}.course-card__level{position:absolute;top:11px;left:11px;padding:6px 9px;border-radius:999px;background:#ffff00;color:#222;font-size:10px;font-weight:700}.course-card__save{position:absolute;top:10px;right:10px;width:36px;height:36px;border:0;border-radius:50%;background:#fff;color:#222;font-size:21px;line-height:1;cursor:pointer;box-shadow:0 2px 9px #0000001a;transition:transform .16s ease,background .16s ease}.course-card__save:hover{transform:scale(1.06);background:#ffff00}.course-card__details{padding:13px 1px 0;color:#717171;font-size:13px}.course-card__meta{display:flex;justify-content:space-between;gap:8px;font-size:11px}.course-card__meta span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.course-card__meta span:last-child{flex:none}.course-card h3{display:-webkit-box;min-height:45px;overflow:hidden;margin:8px 0 4px;color:#222;font-size:15px;line-height:1.5;letter-spacing:-.25px;-webkit-box-orient:vertical;-webkit-line-clamp:2}.course-card h3 button{display:-webkit-box;overflow:hidden;padding:0;border:0;background:none;color:inherit;font:inherit;font-weight:700;text-align:left;-webkit-box-orient:vertical;-webkit-line-clamp:2;cursor:pointer}.course-card__details>p{display:-webkit-box;min-height:38px;overflow:hidden;margin:0;color:#717171;font-size:12px;line-height:1.6;-webkit-box-orient:vertical;-webkit-line-clamp:2}.course-card__footer{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:12px;padding-top:11px;border-top:1px solid #eceef0;color:#222}.course-card__footer strong{font-size:14px}.course-card__footer>span{color:#5c6064;font-size:11px}.course-card button:focus-visible{outline:3px solid #222;outline-offset:3px}@media(max-width:520px){.course-card__details{padding-top:10px}.course-card__meta{font-size:9px}.course-card h3{font-size:13px}.course-card__details>p{font-size:10px}.course-card__footer strong{font-size:12px}.course-card__footer>span{font-size:9px}}@media(prefers-reduced-motion:reduce){.course-card,.course-card__image,.course-card__save{transition:none}}
</style>
