<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const route = ref(window.location.pathname)
const posts = ref([])
const loading = ref(false)
const loadError = ref('')
const formMessage = ref('')
const title = ref('')
const content = ref('')
const email = ref('')
const password = ref('')
const displayName = ref('')

const currentPage = computed(() => {
  if (route.value === '/login') return 'login'
  if (route.value === '/signup') return 'signup'
  if (route.value === '/posts/new') return 'compose'
  if (/^\/posts\/[^/]+$/.test(route.value)) return 'detail'
  return 'posts'
})
const detailId = computed(() => route.value.split('/')[2] || '')

function navigate(path) {
  if (path === route.value) return
  window.history.pushState({}, '', path)
  route.value = path
  formMessage.value = ''
  if (path === '/') navigate('/posts')
}

function followLink(event, path) {
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return
  event.preventDefault()
  navigate(path)
}

function onPopState() {
  route.value = window.location.pathname
}

async function fetchPosts() {
  loading.value = true
  loadError.value = ''
  try {
    const response = await fetch('/api/posts', { headers: { Accept: 'application/json' } })
    const payload = await response.json()
    if (!response.ok || payload.code !== 200 || !Array.isArray(payload.result)) {
      throw new Error(payload.message || '게시글을 불러오지 못했습니다.')
    }
    posts.value = payload.result
  } catch (error) {
    loadError.value = error instanceof TypeError
      ? '서버에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인해 주세요.'
      : error.message || '게시글을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function submitUnavailable(feature) {
  formMessage.value = `현재 백엔드에 ${feature} 기능이 연결되어 있지 않습니다.`
}

function formatDate(value) {
  if (!value) return '날짜 정보 없음'
  const date = new Date(value.replace(' ', 'T') + (value.endsWith('Z') ? '' : 'Z'))
  if (Number.isNaN(date.getTime())) return value
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit',
  }).format(date)
}

function toDateTime(value) {
  if (!value) return undefined
  const date = new Date(value.replace(' ', 'T') + (value.endsWith('Z') ? '' : 'Z'))
  return Number.isNaN(date.getTime()) ? undefined : date.toISOString()
}

onMounted(() => {
  window.addEventListener('popstate', onPopState)
  fetchPosts()
})
onUnmounted(() => window.removeEventListener('popstate', onPopState))
</script>

<template>
  <div class="app-shell">
    <a class="skip-link" href="#main-content">본문으로 건너뛰기</a>
    <header class="topbar">
      <a class="brand" href="/posts" @click="followLink($event, '/posts')" aria-label="모아 홈">
        <span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span>
        <span>모아<span class="brand-dot">.</span></span>
      </a>
      <nav class="nav-links" aria-label="주요 메뉴">
        <a :class="{ selected: currentPage === 'posts' || currentPage === 'detail' }" href="/posts" @click="followLink($event, '/posts')">게시글</a>
        <a class="nav-write" href="/posts/new" @click="followLink($event, '/posts/new')"><span aria-hidden="true">＋</span> 글쓰기</a>
      </nav>
      <div class="account-links">
        <a href="/login" @click="followLink($event, '/login')">로그인</a>
        <a class="signup-link" href="/signup" @click="followLink($event, '/signup')">회원가입</a>
      </div>
    </header>

    <Transition name="route" mode="out-in">
      <main id="main-content" :key="route" class="page-content">
        <template v-if="currentPage === 'posts'">
          <section class="intro-row">
            <div>
              <p class="section-label"><span class="label-seed" aria-hidden="true"></span> 모아의 이야기</p>
              <h1>생각을 나누고,<br class="mobile-break" /> 함께 자라요.</h1>
              <p class="intro-copy">오늘의 작은 기록이 누군가에게 새로운 영감이 됩니다.</p>
            </div>
            <button class="primary-button intro-write" type="button" @click="navigate('/posts/new')">게시글 작성 <span aria-hidden="true">↗</span></button>
          </section>

          <section class="feed" aria-labelledby="feed-title">
            <div class="feed-heading"><h2 id="feed-title">최근 게시글</h2><span v-if="!loading && !loadError" class="post-count">{{ posts.length }}개의 이야기</span></div>
            <div v-if="loading" class="state-panel" role="status" aria-live="polite">
              <span class="loader" aria-hidden="true"></span><p>게시글을 불러오고 있어요…</p>
            </div>
            <div v-else-if="loadError" class="state-panel error-panel" role="alert">
              <span class="state-icon" aria-hidden="true">!</span><h3>목록을 불러오지 못했어요</h3><p>{{ loadError }}</p><button class="outline-button" type="button" @click="fetchPosts">다시 불러오기</button>
            </div>
            <div v-else-if="posts.length === 0" class="state-panel empty-panel">
              <span class="empty-illustration" aria-hidden="true"><i></i><i></i><i></i></span><h3>아직 게시글이 없어요</h3><p>첫 이야기를 남겨 이 공간을 시작해 보세요.</p><button class="outline-button" type="button" @click="navigate('/posts/new')">첫 게시글 작성</button>
            </div>
            <div v-else class="post-list">
              <article v-for="(post, index) in posts" :key="post.id" class="post-row">
                <button class="post-open" type="button" :aria-label="`${post.title}, 게시글 상세 보기`" @click="navigate(`/posts/${post.id}`)">
                  <span class="post-number">{{ String(index + 1).padStart(2, '0') }}</span>
                  <span class="post-copy"><span class="post-title">{{ post.title }}</span><span class="post-excerpt">{{ post.content }}</span><time class="post-date" :datetime="toDateTime(post.created_at)">{{ formatDate(post.created_at) }}</time></span>
                  <span class="post-arrow" aria-hidden="true">↗</span>
                </button>
              </article>
            </div>
          </section>
          <aside class="api-note"><span class="note-mark" aria-hidden="true">i</span><p>게시글 목록은 백엔드 API에서 불러옵니다. 작성 및 상세 API가 연결되면 해당 기능을 사용할 수 있어요.</p></aside>
        </template>

        <section v-else-if="currentPage === 'login' || currentPage === 'signup'" class="form-page">
          <a class="back-link" href="/posts" @click="followLink($event, '/posts')">← 게시글 목록</a>
          <div class="form-card">
            <span class="form-symbol" aria-hidden="true">{{ currentPage === 'login' ? '↗' : '✳' }}</span>
            <p class="section-label">모아와 함께하기</p>
            <h1>{{ currentPage === 'login' ? '다시 만나 반가워요' : '모아에 오신 걸 환영해요' }}</h1>
            <p class="form-intro">{{ currentPage === 'login' ? '계정에 로그인해 이야기를 이어가세요.' : '계정을 만들고 나만의 이야기를 나눠보세요.' }}</p>
            <form @submit.prevent="submitUnavailable(currentPage === 'login' ? '로그인' : '회원가입')">
              <label v-if="currentPage === 'signup'" for="display-name">이름</label>
              <input v-if="currentPage === 'signup'" id="display-name" v-model="displayName" name="name" autocomplete="name" placeholder="이름을 입력해 주세요…" />
              <label for="email">이메일</label><input id="email" v-model="email" name="email" type="email" autocomplete="email" placeholder="예: name@example.com" />
              <label for="password">비밀번호</label><input id="password" v-model="password" name="password" type="password" :autocomplete="currentPage === 'login' ? 'current-password' : 'new-password'" placeholder="비밀번호를 입력해 주세요…" />
              <p v-if="formMessage" class="form-message" role="status" aria-live="polite">{{ formMessage }}</p>
              <button class="primary-button form-submit" type="submit">{{ currentPage === 'login' ? '로그인' : '회원가입' }}</button>
            </form>
            <p class="form-switch">{{ currentPage === 'login' ? '아직 계정이 없으신가요?' : '이미 계정이 있으신가요?' }} <button type="button" @click="navigate(currentPage === 'login' ? '/signup' : '/login')">{{ currentPage === 'login' ? '회원가입' : '로그인' }}</button></p>
          </div>
          <p class="api-unavailable">인증 API가 아직 백엔드에 연결되지 않아 계정 기능은 사용할 수 없습니다.</p>
        </section>

        <section v-else-if="currentPage === 'compose'" class="form-page compose-page">
          <a class="back-link" href="/posts" @click="followLink($event, '/posts')">← 게시글 목록</a>
          <div class="compose-heading"><p class="section-label">나의 이야기</p><h1>새 게시글 작성</h1><p>함께 나누고 싶은 생각을 적어보세요.</p></div>
          <form class="compose-card" @submit.prevent="submitUnavailable('게시글 작성')">
            <label for="post-title">제목</label><input id="post-title" v-model="title" name="title" maxlength="120" placeholder="어떤 이야기를 나누고 싶나요…" />
            <label for="post-content">내용</label><textarea id="post-content" v-model="content" name="content" rows="9" placeholder="생각을 자유롭게 적어주세요…"></textarea>
            <p v-if="formMessage" class="form-message" role="status" aria-live="polite">{{ formMessage }}</p>
            <div class="compose-actions"><button class="outline-button" type="button" @click="navigate('/posts')">취소</button><button class="primary-button" type="submit">게시글 등록</button></div>
          </form>
          <p class="api-unavailable">게시글 작성 API가 아직 백엔드에 연결되지 않아 등록할 수 없습니다.</p>
        </section>

        <section v-else class="detail-page">
          <a class="back-link" href="/posts" @click="followLink($event, '/posts')">← 게시글 목록</a>
          <article class="detail-card"><span class="detail-index">게시글 {{ detailId }}</span><h1>상세 내용을 불러올 수 없어요</h1><p>현재 백엔드에는 게시글 목록 조회 API만 있습니다. 게시글 상세 조회 API가 연결되면 여기에서 내용을 확인할 수 있어요.</p><button class="primary-button" type="button" @click="navigate('/posts')">목록으로 돌아가기</button></article>
        </section>
      </main>
    </Transition>

    <footer class="site-footer"><a class="brand footer-brand" href="/posts" @click="followLink($event, '/posts')"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>모아<span class="brand-dot">.</span></span></a><span>작은 기록이 모여 이야기가 됩니다.</span><span>© 2026 moa</span></footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
:root{font-family:'DM Sans','Noto Sans KR',sans-serif;color:#26332e;background:#f4f6f2;font-synthesis:none;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;font-optical-sizing:auto;font-weight:400;--ink:#26332e;--muted:#738079;--line:#dfe5df;--green:#246e52;--mint:#dceee2;--paper:#fff}
*{box-sizing:border-box}body{margin:0;min-width:320px;min-height:100vh;background:radial-gradient(ellipse at 12% 5%,#e7f0e8 0,transparent 28rem),#f4f6f2}button,input,textarea{font:inherit}button,a{-webkit-tap-highlight-color:transparent}button{color:inherit}a{color:inherit;text-decoration:none}button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid #79af8d;outline-offset:3px}.app-shell{max-width:1200px;min-height:100vh;margin:auto;padding:0 48px;display:flex;flex-direction:column}.topbar{height:82px;border-bottom:1px solid #dce3dc;display:flex;align-items:center;justify-content:space-between}.brand{display:inline-flex;align-items:center;gap:10px;font-size:22px;font-weight:800;letter-spacing:-1.1px}.brand-dot{color:#65a77b}.brand-mark{width:25px;height:25px;display:flex;align-items:flex-end;gap:2px;padding:4px 3px;border-radius:8px;background:#286e51}.brand-mark i{display:block;width:5px;border-radius:4px;background:#d9eedf}.brand-mark i:nth-child(1){height:9px}.brand-mark i:nth-child(2){height:14px}.brand-mark i:nth-child(3){height:11px}.nav-links,.account-links{display:flex;align-items:center;gap:30px;font-size:14px}.nav-links a,.account-links>a{color:#627068;transition:color .18s ease}.nav-links a:hover,.account-links>a:hover{color:#286e51}.nav-links a.selected{color:#26332e;font-weight:700}.nav-write{color:#286e51!important;font-weight:700}.nav-write span{font-size:18px;margin-right:4px}.signup-link{padding:10px 16px;border:1px solid #cbd9ce;border-radius:999px;color:#286e51!important;font-weight:700}.page-content{flex:1}.intro-row{display:flex;align-items:flex-end;justify-content:space-between;padding:76px 0 66px}.section-label{display:flex;align-items:center;gap:9px;margin:0 0 17px;color:#397655;font-size:13px;font-weight:700}.label-seed{width:9px;height:9px;border-radius:70% 30% 70% 30%;background:#76aa7e;transform:rotate(-30deg)}h1,h2,h3,p{margin-top:0}.intro-row h1,.form-card h1,.compose-heading h1{margin:0;color:#26332e;font-size:clamp(36px,5vw,58px);font-weight:700;letter-spacing:-2.5px;line-height:1.17;text-wrap:balance}.mobile-break{display:none}.intro-copy{margin:17px 0 0;color:#748079;font-size:15px;line-height:1.8}.primary-button,.outline-button{min-height:46px;padding:0 19px;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;transition:background-color .18s ease,border-color .18s ease,transform .18s ease}.primary-button{border:1px solid #286e51;background:#286e51;color:#fff}.primary-button:hover{background:#1e5b42;transform:translateY(-1px)}.primary-button span{padding-left:12px}.feed{border-top:1px solid #d8e0d8}.feed-heading{display:flex;align-items:center;justify-content:space-between;padding:28px 0 15px}.feed-heading h2{margin:0;font-size:19px;letter-spacing:-.5px}.post-count{color:#808c84;font-size:13px}.post-row{border-top:1px solid #e2e7e2}.post-open{width:100%;min-height:120px;display:grid;grid-template-columns:56px 1fr 32px;gap:16px;align-items:center;padding:20px 12px;border:0;background:transparent;text-align:left;cursor:pointer;transition:background-color .18s ease}.post-open:hover{background:#edf3ec}.post-number{align-self:start;padding-top:4px;color:#7e9a86;font-size:12px;font-variant-numeric:tabular-nums}.post-copy{min-width:0;display:flex;flex-direction:column;gap:8px}.post-title{overflow:hidden;color:#28352f;font-size:18px;font-weight:700;text-overflow:ellipsis;white-space:nowrap}.post-excerpt{display:-webkit-box;overflow:hidden;color:#6d7972;font-size:14px;line-height:1.6;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow-wrap:anywhere}.post-date{color:#869189;font-size:12px}.post-arrow{justify-self:end;color:#65806d;font-size:19px;transition:transform .18s ease}.post-open:hover .post-arrow{transform:translate(2px,-2px)}.state-panel{min-height:270px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:38px 18px;text-align:center}.state-panel p{margin:8px 0 0;color:#77827b;font-size:14px;line-height:1.7}.state-panel h3{margin:19px 0 0;font-size:19px;letter-spacing:-.5px}.loader{width:26px;height:26px;border:3px solid #dbe8dc;border-top-color:#397655;border-radius:50%;animation:spin .8s linear infinite}.state-icon{width:34px;height:34px;display:grid;place-items:center;border-radius:50%;background:#fae9e5;color:#a54f3d;font-weight:700}.outline-button{border:1px solid #cbd8ce;background:#fff;color:#356c4f}.outline-button:hover{border-color:#6da17a;background:#f5faf5}.state-panel .outline-button{margin-top:19px}.empty-illustration{height:48px;display:flex;align-items:flex-end;gap:5px;padding:0 4px 6px;border-bottom:2px solid #78a781}.empty-illustration i{width:10px;border-radius:8px 8px 2px 2px;background:#c2dfc6}.empty-illustration i:nth-child(1){height:24px}.empty-illustration i:nth-child(2){height:38px;background:#83b28a}.empty-illustration i:nth-child(3){height:30px}.api-note{display:flex;align-items:flex-start;gap:11px;margin:30px 0 50px;padding:14px 16px;border-radius:9px;background:#e9efe8}.note-mark{flex:none;width:18px;height:18px;display:grid;place-items:center;border:1px solid #76947c;border-radius:50%;color:#56775d;font-family:serif;font-size:12px;font-weight:700}.api-note p{margin:0;color:#68776b;font-size:12px;line-height:1.65}.site-footer{min-height:74px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid #dce3dc;color:#849087;font-size:12px}.footer-brand{color:#334239;font-size:17px}.footer-brand .brand-mark{width:21px;height:21px;border-radius:6px}.footer-brand .brand-mark i{width:4px}.form-page{max-width:600px;margin:0 auto;padding:50px 0 70px}.back-link{display:inline-block;margin-bottom:25px;color:#65736a;font-size:14px}.back-link:hover{color:#286e51}.form-card,.compose-card,.detail-card{padding:38px 42px;border:1px solid #e0e7e0;border-radius:13px;background:#fff}.form-symbol{width:38px;height:38px;display:grid;place-items:center;margin-bottom:26px;border-radius:12px;background:#e5f1e5;color:#33754d;font-size:20px}.form-card .section-label{margin-bottom:12px}.form-card h1{font-size:33px;letter-spacing:-1.4px}.form-intro{margin:10px 0 27px;color:#738079;font-size:14px;line-height:1.7}.form-card form,.compose-card{display:flex;flex-direction:column}.form-card label,.compose-card label{margin:15px 0 8px;color:#3e4b43;font-size:13px;font-weight:700}.form-card input,.compose-card input,.compose-card textarea{width:100%;min-height:48px;padding:12px 14px;border:1px solid #d8e0d9;border-radius:7px;background:#fcfdfb;color:#28352f;font-size:14px}.form-card input::placeholder,.compose-card input::placeholder,.compose-card textarea::placeholder{color:#a1aaa3}.compose-card textarea{min-height:210px;resize:vertical;line-height:1.7}.form-submit{width:100%;margin-top:24px}.form-switch{margin:22px 0 0;color:#77827b;text-align:center;font-size:13px}.form-switch button{padding:4px 0;border:0;background:none;color:#286e51;font-weight:700;cursor:pointer}.form-message{margin:13px 0 0;color:#a44e3f;font-size:13px;line-height:1.55}.api-unavailable{margin:15px 0 0;color:#7c877f;font-size:12px;line-height:1.7;text-align:center}.compose-page{max-width:760px}.compose-heading{margin-bottom:24px}.compose-heading h1{font-size:38px}.compose-heading>p:last-child{margin:10px 0 0;color:#77827b;font-size:14px}.compose-card{padding:28px 32px}.compose-actions{display:flex;justify-content:flex-end;gap:10px;margin-top:24px}.compose-actions .form-message{margin-right:auto}.detail-page{max-width:760px;margin:0 auto;padding:50px 0 100px}.detail-card{padding:48px}.detail-index{color:#397655;font-size:13px;font-weight:700}.detail-card h1{margin:17px 0 13px;font-size:34px;letter-spacing:-1.2px;text-wrap:balance}.detail-card p{max-width:540px;margin-bottom:25px;color:#6f7b73;font-size:15px;line-height:1.8}.route-enter-active,.route-leave-active{transition:opacity .18s ease,transform .18s ease}.route-enter-from{opacity:0;transform:translateY(8px)}.route-leave-to{opacity:0;transform:translateY(-5px)}@keyframes spin{to{transform:rotate(360deg)}}
@media(max-width:760px){.app-shell{padding:0 22px}.topbar{height:70px}.nav-links{gap:16px}.account-links{gap:12px}.nav-links,.account-links{font-size:12px}.signup-link{padding:8px 11px}.brand{font-size:19px}.brand-mark{width:23px;height:23px}.intro-row{align-items:flex-start;gap:24px;flex-direction:column;padding:55px 0 45px}.intro-row h1{font-size:clamp(38px,8vw,52px)}.mobile-break{display:block}.intro-copy{max-width:360px;font-size:14px}.intro-write{min-height:43px}.post-open{grid-template-columns:34px minmax(0,1fr) 20px;gap:10px;padding:19px 3px}.post-title{font-size:16px}.post-excerpt{font-size:13px}.api-note{margin-bottom:35px}.site-footer{gap:9px;flex-wrap:wrap;padding:16px 0;font-size:11px}.footer-brand{font-size:15px}.form-page{padding-top:36px}.form-card{padding:30px 25px}.compose-card{padding:23px 20px}}
@media(max-width:460px){.app-shell{padding:0 17px}.topbar{height:64px}.nav-links{gap:12px}.nav-write span{display:none}.account-links{gap:9px}.account-links>a:first-child{display:none}.signup-link{padding:8px 10px}.intro-row{padding-top:43px}.feed-heading{padding-top:23px}.post-open{min-height:112px}.post-number{font-size:11px}.post-date{font-size:11px}.form-card h1{font-size:29px}.compose-heading h1{font-size:32px}.detail-card{padding:31px 24px}.detail-card h1{font-size:29px}.site-footer>span:nth-child(2){display:none}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
 .skip-link{position:absolute;z-index:10;top:8px;left:8px;transform:translateY(-160%);padding:10px 14px;border-radius:6px;background:#fff;color:#26332e}.skip-link:focus{transform:translateY(0)}
</style>
