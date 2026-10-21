<script setup>
import AccountForm from '../components/AccountForm.vue'
import CoursePageShell from '../components/CoursePageShell.vue'

defineProps({ mode: { type: String, default: 'login' }, busy: { type: Boolean, default: false }, error: { type: String, default: '' }, callback: { type: Boolean, default: false } })
const emit = defineEmits(['navigate', 'submit', 'social-login'])
</script>

<template>
  <CoursePageShell active="account" @navigate="emit('navigate', $event)">
    <div v-if="callback" class="course-auth"><section class="course-auth__callback"><span v-if="busy" class="course-auth__spinner"></span><h1>{{ busy ? '로그인을 확인하고 있어요' : '로그인을 완료할 수 없어요' }}</h1><p v-if="busy">잠시만 기다려 주세요.</p><p v-else-if="error" role="alert">{{ error }}</p><a v-if="!busy" href="/login" @click.prevent="emit('navigate', '/login')">로그인으로 돌아가기</a></section></div>
    <div v-else class="course-auth"><AccountForm :mode="mode" :busy="busy" :error="error" social-label="카카오로 계속하기" @submit="emit('submit', $event)" @social-login="emit('social-login')" @switch-mode="emit('navigate', `/${$event}`)" /></div>
  </CoursePageShell>
</template>

<style scoped>
.course-auth{display:grid;min-height:570px;place-items:center;padding:26px 0}.course-auth__callback{width:min(100%,480px);padding:38px;border:1px solid #e5e5e5;border-radius:12px;text-align:center}.course-auth__callback h1{font-size:21px}.course-auth__callback p{color:#666;font-size:13px;line-height:1.7}.course-auth__callback a{font-size:13px;text-decoration:underline}.course-auth__spinner{width:28px;height:28px;display:block;margin:0 auto 15px;border:2px solid #eee;border-top-color:#222;border-radius:50%;animation:auth-spin .8s linear infinite}@keyframes auth-spin{to{transform:rotate(360deg)}}@media(prefers-reduced-motion:reduce){.course-auth__spinner{animation-duration:.01ms}}
</style>
