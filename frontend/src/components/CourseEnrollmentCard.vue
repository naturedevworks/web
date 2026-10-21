<script setup>
import { computed } from 'vue'

const props = defineProps({
  price: { type: [String, Number], required: true },
  duration: { type: String, default: '온라인 강의' },
  level: { type: String, default: '' },
  actionLabel: { type: String, default: '수강 신청하기' },
  disabled: { type: Boolean, default: false },
})
const emit = defineEmits(['enroll'])
const priceLabel = computed(() => typeof props.price === 'number' || (props.price !== '' && Number.isFinite(Number(props.price))) ? new Intl.NumberFormat('ko-KR').format(Number(props.price)) : String(props.price))
const hasCurrency = computed(() => priceLabel.value !== '가격 정보 없음')
</script>

<template>
  <aside class="course-enrollment">
    <p class="course-enrollment__label">강의 수강권</p>
    <p class="course-enrollment__price"><strong>{{ priceLabel }}</strong><span v-if="hasCurrency">원</span></p>
    <dl><div><dt>수강 방식</dt><dd>온라인 수강</dd></div><div><dt>강의 시간</dt><dd>{{ duration }}</dd></div><div v-if="level"><dt>난이도</dt><dd>{{ level }}</dd></div></dl>
    <button class="course-enrollment__action" type="button" :disabled="disabled" @click="emit('enroll')">{{ actionLabel }}</button>
    <p class="course-enrollment__note">결제 후 바로 강의를 시작할 수 있습니다.</p>
  </aside>
</template>

<style scoped>
.course-enrollment{position:sticky;top:24px;align-self:start;padding:24px;border:1px solid #e2e4e7;border-radius:16px;background:#fff}.course-enrollment__label{margin:0;color:#666;font-size:12px}.course-enrollment__price{margin:6px 0 19px}.course-enrollment__price strong{font-size:27px;letter-spacing:-.7px}.course-enrollment__price span{margin-left:3px;font-size:13px}.course-enrollment dl{margin:0;border-top:1px solid #eceef0}.course-enrollment dl div{display:flex;justify-content:space-between;gap:12px;padding:13px 0;border-bottom:1px solid #eceef0;font-size:12px}.course-enrollment dt{color:#717171}.course-enrollment dd{margin:0;color:#222;font-weight:600;text-align:right}.course-enrollment__action{width:100%;min-height:50px;margin-top:19px;border:0;border-radius:999px;background:#ffff00;color:#111;font:inherit;font-size:14px;font-weight:700;cursor:pointer;transition:transform .16s ease,background .16s ease}.course-enrollment__action:hover:not(:disabled){transform:translateY(-1px);background:#eded00}.course-enrollment__action:disabled{cursor:wait;opacity:.65}.course-enrollment__action:focus-visible{outline:3px solid #222;outline-offset:3px}.course-enrollment__note{margin:12px 0 0;color:#717171;text-align:center;font-size:11px;line-height:1.6}@media(max-width:800px){.course-enrollment{position:static}}@media(prefers-reduced-motion:reduce){.course-enrollment__action{transition:none}}
</style>
