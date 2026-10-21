<script setup>
import CoursePageShell from '../components/CoursePageShell.vue'

defineProps({ course: { type: Object, default: null }, busy: { type: Boolean, default: false }, enrolled: { type: Boolean, default: false }, message: { type: String, default: '' }, currentUser: { type: Object, default: null } })
const emit = defineEmits(['navigate', 'logout'])
</script>

<template>
  <CoursePageShell :current-user="currentUser" @navigate="emit('navigate', $event)" @logout="emit('logout')">
    <section class="payment-success-view"><div class="payment-success-view__card"><span class="payment-success-view__icon" :class="{ 'is-error': !enrolled && !busy }">{{ enrolled ? '✓' : busy ? '…' : '!' }}</span><p>결제 결과</p><h1>{{ enrolled ? '결제가 완료됐어요' : busy ? '결제를 확인하고 있어요' : '결제를 확인하지 못했어요' }}</h1><h2 v-if="course">{{ course.title }}</h2><p v-if="busy">잠시만 기다려 주세요.</p><p v-else-if="message" class="payment-success-view__error" role="alert">{{ message }}</p><p v-else-if="enrolled">구매한 강의를 내 강의에서 확인할 수 있습니다.</p><div><button type="button" @click="emit('navigate', enrolled ? `/my/courses/${course?.id}/learn` : '/courses')">{{ enrolled ? '강의 시작하기' : '강의 목록으로' }}</button><a v-if="enrolled && course" :href="`/courses/${course.id}`" @click.prevent="emit('navigate', `/courses/${course.id}`)">강의 상세 보기</a></div></div></section>
  </CoursePageShell>
</template>

<style scoped>
.payment-success-view{min-height:62vh;display:grid;place-items:center;padding:25px 0}.payment-success-view__card{width:min(100%,560px);padding:44px 34px;border:1px solid #e5e5e5;border-radius:13px;text-align:center}.payment-success-view__icon{width:58px;height:58px;display:grid;place-items:center;margin:0 auto 18px;border-radius:50%;background:#ffff00;font-size:25px;font-weight:700}.payment-success-view__icon.is-error{background:#f5e8e5;color:#9c392b}.payment-success-view__card>p:first-of-type{color:#666;font-size:12px}.payment-success-view h1{margin:0;font-size:clamp(23px,3vw,30px)}.payment-success-view h2{margin:17px 0 0;font-size:16px}.payment-success-view__card>p:not(:first-of-type){color:#666;font-size:13px;line-height:1.7}.payment-success-view__error{color:#a33!important}.payment-success-view__card>div{display:flex;flex-direction:column;align-items:center;gap:14px;margin-top:24px}.payment-success-view button{min-height:47px;width:min(100%,320px);border:0;border-radius:8px;background:#ffff00;color:#111;font:inherit;font-size:13px;font-weight:700;cursor:pointer}.payment-success-view a{font-size:12px;text-decoration:underline}
</style>
