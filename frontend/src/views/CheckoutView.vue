<script setup>
import { computed } from 'vue'
import CoursePageShell from '../components/CoursePageShell.vue'

const props = defineProps({ course: { type: Object, default: null }, loading: { type: Boolean, default: false }, paymentBusy: { type: Boolean, default: false }, message: { type: String, default: '' }, currentUser: { type: Object, default: null } })
const emit = defineEmits(['navigate', 'pay', 'logout'])
const price = computed(() => Number.isFinite(Number(props.course?.price)) ? new Intl.NumberFormat('ko-KR').format(Number(props.course.price)) : '가격 정보 없음')
</script>

<template>
  <CoursePageShell :current-user="currentUser" @navigate="emit('navigate', $event)" @logout="emit('logout')">
    <section class="checkout-view">
      <a class="checkout-view__back" href="/courses" @click.prevent="emit('navigate', course ? `/courses/${course.id}` : '/courses')">← 강의로 돌아가기</a>
      <div class="checkout-view__layout">
        <div class="checkout-view__main"><p class="checkout-view__eyebrow">결제</p><h1>주문 내용을 확인해 주세요</h1><p class="checkout-view__intro">결제가 완료되면 바로 강의를 수강할 수 있습니다.</p>
          <div v-if="course" class="checkout-view__course"><div class="checkout-view__cover"><img v-if="course.thumbnail_url" :src="course.thumbnail_url" :alt="`${course.title} 강의 이미지`" /><span v-else>{{ course.level || '온라인 클래스' }}</span></div><div><p>{{ course.instructor_name || '강사 정보 준비 중' }}</p><h2>{{ course.title }}</h2><span>{{ course.level || '온라인 수강' }} · 평생 수강</span></div></div>
          <div class="checkout-view__method"><span aria-hidden="true">▣</span><div><strong>안전한 온라인 결제</strong><small>결제 정보는 결제 제공사를 통해 처리됩니다.</small></div></div>
        </div>
        <aside class="checkout-view__summary"><h2>결제 금액</h2><div class="checkout-view__row"><span>강의 금액</span><strong>{{ price }}원</strong></div><div class="checkout-view__row checkout-view__total"><span>최종 결제 금액</span><strong>{{ price }}원</strong></div><div v-if="Number(course?.price) === 100" class="checkout-view__test-note"><strong>테스트 결제</strong><p>결제 연동 확인용 100원 테스트 강의입니다.</p></div><button type="button" :disabled="!course || loading || paymentBusy" @click="emit('pay')">{{ paymentBusy ? '결제창을 여는 중…' : `${price}원 결제하기` }}</button><p v-if="message" class="checkout-view__error" role="alert">{{ message }}</p><p class="checkout-view__terms">결제 진행 전 주문 내용과 금액을 확인해 주세요.</p></aside>
      </div>
      <div v-if="loading" class="checkout-view__loading" role="status">강의 정보를 불러오고 있어요.</div>
    </section>
  </CoursePageShell>
</template>

<style scoped>
.checkout-view__back{display:inline-block;margin-bottom:22px;color:#444;font-size:13px}.checkout-view__layout{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:56px;max-width:1040px;margin:0 auto}.checkout-view__main{padding:12px 0}.checkout-view__eyebrow{margin:0 0 8px;color:#666;font-size:12px}.checkout-view h1{margin:0;font-size:clamp(25px,3vw,34px);letter-spacing:-1px}.checkout-view__intro{color:#666;font-size:13px;line-height:1.7}.checkout-view__course{display:flex;align-items:center;gap:18px;margin-top:32px;padding:20px 0;border-top:1px solid #eee;border-bottom:1px solid #eee}.checkout-view__cover{width:140px;height:96px;display:grid;flex:none;place-items:center;overflow:hidden;background:#f2f0c2;color:#394638;font-size:12px;font-weight:700}.checkout-view__cover img{width:100%;height:100%;object-fit:cover}.checkout-view__course p,.checkout-view__course span{margin:0;color:#666;font-size:11px}.checkout-view__course h2{margin:6px 0;font-size:17px}.checkout-view__method{display:flex;align-items:center;gap:14px;margin-top:24px;padding:16px;border:1px solid #ddd;border-radius:8px}.checkout-view__method>span{font-size:21px}.checkout-view__method div{display:grid;gap:5px}.checkout-view__method strong{font-size:13px}.checkout-view__method small{color:#666;font-size:11px}.checkout-view__summary{align-self:start;padding:24px;border:1px solid #ddd;border-radius:12px;background:#fff;box-shadow:0 5px 22px #0000000d}.checkout-view__summary h2{margin:0 0 20px;font-size:19px}.checkout-view__row{display:flex;justify-content:space-between;gap:12px;padding:14px 0;border-top:1px solid #eee;color:#555;font-size:12px}.checkout-view__row strong{color:#222}.checkout-view__total{margin-top:4px;color:#222;font-weight:700}.checkout-view__total strong{font-size:17px}.checkout-view__summary button{width:100%;min-height:49px;margin-top:15px;border:0;border-radius:8px;background:#ffff00;color:#111;font:inherit;font-size:13px;font-weight:700;cursor:pointer}.checkout-view__summary button:disabled{cursor:wait;opacity:.65}.checkout-view__test-note{margin:12px 0;padding:12px;border-radius:7px;background:#fffde0}.checkout-view__test-note strong{font-size:11px}.checkout-view__test-note p,.checkout-view__terms{color:#666;font-size:10px;line-height:1.6}.checkout-view__test-note p{margin:5px 0 0}.checkout-view__terms{margin:13px 0 0}.checkout-view__error{color:#b42318;font-size:12px}.checkout-view__loading{padding:35px;color:#666;text-align:center;font-size:13px}@media(max-width:800px){.checkout-view__layout{grid-template-columns:1fr;gap:20px}.checkout-view__summary{max-width:none}}@media(max-width:560px){.checkout-view__layout{gap:14px}.checkout-view__course{gap:12px}.checkout-view__cover{width:100px;height:78px}.checkout-view__course h2{font-size:14px}.checkout-view__summary{padding:20px}}
</style>
