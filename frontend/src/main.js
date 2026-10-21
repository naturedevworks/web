import { createApp } from 'vue'
import App from './App.vue'
import './discovery.css'
import './assets/course-theme.css'

const kakaoKey = import.meta.env.VITE_KAKAO_JS_KEY
if (window.Kakao && kakaoKey && !window.Kakao.isInitialized()) {
  window.Kakao.init(kakaoKey)
}

createApp(App).mount('#app')
