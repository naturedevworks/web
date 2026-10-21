<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  mode: { type: String, default: 'login', validator: (value) => ['login', 'signup'].includes(value) },
  busy: { type: Boolean, default: false },
  error: { type: String, default: '' },
  socialLabel: { type: String, default: '다른 방법으로 계속하기' },
})

const emit = defineEmits(['submit', 'social-login', 'switch-mode'])
const name = ref('')
const email = ref('')
const password = ref('')
const isSignup = computed(() => props.mode === 'signup')

function submit() {
  emit('submit', { name: name.value, email: email.value, password: password.value })
}
</script>

<template>
  <section class="account-card">
    <div class="account-card__heading">
      <h1>{{ isSignup ? '회원가입' : '로그인' }}</h1>
      <p>{{ isSignup ? '계정을 만들고 새로운 배움을 시작하세요.' : '계속하려면 계정에 로그인하세요.' }}</p>
    </div>
    <form class="account-form" @submit.prevent="submit">
      <label v-if="isSignup">이름<input v-model="name" name="name" autocomplete="name" required maxlength="100" placeholder="이름 입력" /></label>
      <label>이메일<input v-model="email" name="email" type="email" autocomplete="email" required placeholder="name@example.com" /></label>
      <label>비밀번호<input v-model="password" name="password" type="password" :autocomplete="isSignup ? 'new-password' : 'current-password'" required minlength="8" maxlength="128" placeholder="8자 이상 입력" /></label>
      <p v-if="error" class="account-form__error" role="alert">{{ error }}</p>
      <button class="account-form__submit" type="submit" :disabled="busy">{{ busy ? '처리 중…' : isSignup ? '계정 만들기' : '로그인' }}</button>
    </form>
    <div class="account-card__divider"><span>또는</span></div>
    <button class="account-card__social" type="button" :disabled="busy" @click="emit('social-login')">{{ socialLabel }}</button>
    <p class="account-card__switch">
      {{ isSignup ? '이미 계정이 있나요?' : '아직 계정이 없나요?' }}
      <button type="button" @click="emit('switch-mode', isSignup ? 'login' : 'signup')">{{ isSignup ? '로그인' : '회원가입' }}</button>
    </p>
    <p class="account-card__terms">계속하면 이용약관과 개인정보 처리방침에 동의하게 됩니다.</p>
  </section>
</template>

<style scoped>
.account-card{width:min(100%,480px);margin:0 auto;padding:30px;border:1px solid #ddd;border-radius:12px;background:#fff;box-shadow:0 8px 28px #0000000d;color:#222}.account-card__heading h1{margin:0;font-size:23px;letter-spacing:-.5px}.account-card__heading p{margin:9px 0 24px;color:#666;font-size:13px;line-height:1.6}.account-form{display:flex;flex-direction:column;gap:15px}.account-form label{display:flex;flex-direction:column;gap:7px;font-size:13px;font-weight:600}.account-form input{min-height:47px;padding:0 13px;border:1px solid #aaa;border-radius:7px;background:#fff;color:#222;font:inherit;font-size:14px}.account-form input::placeholder{color:#888}.account-form input:focus-visible{outline:3px solid #222;outline-offset:2px}.account-form__submit,.account-card__social{min-height:49px;border:0;border-radius:7px;font:inherit;font-size:14px;font-weight:700;cursor:pointer}.account-form__submit{margin-top:3px;background:#ffff00;color:#111}.account-form__submit:hover{background:#eded00}.account-form__submit:disabled,.account-card__social:disabled{cursor:wait;opacity:.65}.account-form__error{margin:0;color:#b42318;font-size:12px}.account-card__divider{display:flex;align-items:center;gap:14px;margin:20px 0;color:#717171;font-size:12px}.account-card__divider:before,.account-card__divider:after{height:1px;flex:1;background:#e5e5e5;content:""}.account-card__social{width:100%;border:1px solid #222;background:#fff;color:#222}.account-card__social:hover{background:#fafafa}.account-card__switch{margin:22px 0 0;text-align:center;font-size:13px}.account-card__switch button{margin-left:5px;padding:0;border:0;background:none;color:#222;font:inherit;font-weight:700;text-decoration:underline;cursor:pointer}.account-card__terms{margin:20px 0 0;padding-top:16px;border-top:1px solid #eee;color:#717171;font-size:11px;line-height:1.6}.account-card button:focus-visible{outline:3px solid #222;outline-offset:3px}@media(max-width:520px){.account-card{padding:24px 20px;border-radius:0;border-right:0;border-left:0;box-shadow:none}}
</style>
