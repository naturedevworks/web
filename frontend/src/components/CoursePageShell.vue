<script setup>
defineProps({ active: { type: String, default: 'courses' }, currentUser: { type: Object, default: null } })
const emit = defineEmits(['navigate', 'logout'])
</script>

<template>
  <div class="course-shell">
    <a class="course-shell__skip-link" href="#main-content">본문으로 건너뛰기</a>
    <header class="course-shell__header">
      <a class="course-shell__brand" href="/courses" @click.prevent="emit('navigate', '/courses')"><span class="course-shell__mark" aria-hidden="true"><span></span><span></span><span></span></span><span>배움</span></a>
      <nav aria-label="주요 메뉴">
        <a :aria-current="active === 'courses' || active === 'detail' ? 'page' : undefined" href="/courses" @click.prevent="emit('navigate', '/courses')">강의</a>
        <a href="/courses#course-list" @click.prevent="emit('navigate', '/courses#course-list')">분야별 강의</a>
        <a :aria-current="active === 'my' || active === 'learning' ? 'page' : undefined" href="/my" @click.prevent="emit('navigate', '/my')">내 강의</a>
      </nav>
      <div class="course-shell__account"><template v-if="currentUser"><a href="/my" @click.prevent="emit('navigate', '/my')">{{ currentUser.nickname || '내 강의' }}</a><button type="button" @click="emit('logout')">로그아웃</button></template><template v-else><a href="/login" @click.prevent="emit('navigate', '/login')">로그인</a><a class="course-shell__signup" href="/signup" @click.prevent="emit('navigate', '/signup')">회원가입</a></template></div>
    </header>
    <div v-if="$slots.search" class="course-shell__search"><slot name="search" /></div>
    <main id="main-content" class="course-shell__main" tabindex="-1"><slot /></main>
    <footer class="course-shell__footer"><span>배움 클래스</span><span>배우고 싶은 오늘을 위해</span><span>© {{ new Date().getFullYear() }}</span></footer>
  </div>
</template>

<style scoped>
.course-shell{min-height:100vh;background:#fff;color:#222;font-family:inherit}.course-shell__skip-link{position:absolute;z-index:10;top:8px;left:8px;transform:translateY(-160%);padding:10px 14px;border-radius:7px;background:#222;color:#fff;font-size:12px;text-decoration:none}.course-shell__skip-link:focus{transform:translateY(0)}.course-shell__header{width:min(1480px,100%);height:78px;display:flex;align-items:center;gap:54px;margin:0 auto;padding:0 clamp(24px,5vw,76px);border-bottom:1px solid #eceef0}.course-shell__brand{display:flex;align-items:center;gap:10px;color:#222;font-size:19px;font-weight:800;letter-spacing:-.6px;text-decoration:none}.course-shell__mark{width:34px;height:34px;display:flex;align-items:flex-end;justify-content:center;gap:3px;padding:8px;border-radius:11px;background:#ffff00}.course-shell__mark span{width:3px;border-radius:3px;background:#222}.course-shell__mark span:nth-child(1){height:7px}.course-shell__mark span:nth-child(2){height:13px}.course-shell__mark span:nth-child(3){height:10px}.course-shell nav{display:flex;align-self:stretch;align-items:center;gap:30px}.course-shell nav a,.course-shell__account a,.course-shell__account button{color:#383a3d;font-size:14px;text-decoration:none}.course-shell nav a{position:relative;display:flex;height:100%;align-items:center}.course-shell nav a:hover,.course-shell__account a:hover,.course-shell__account button:hover{color:#111}.course-shell nav a[aria-current=page]{font-weight:700}.course-shell nav a[aria-current=page]:after{position:absolute;right:0;bottom:0;left:0;height:3px;background:#ffff00;content:""}.course-shell__account{display:flex;align-items:center;gap:19px;margin-left:auto}.course-shell__account button{padding:0;border:0;background:none;font:inherit;cursor:pointer}.course-shell__signup{padding:10px 16px;border-radius:999px;background:#ffff00;color:#111!important;font-weight:700}.course-shell__search{width:min(1480px,100%);margin:0 auto;padding:19px clamp(24px,5vw,76px) 0}.course-shell__main{width:min(1480px,100%);min-height:calc(100vh - 150px);margin:0 auto;padding:32px clamp(24px,5vw,76px) 68px}.course-shell__footer{min-height:68px;display:flex;align-items:center;gap:22px;padding:0 clamp(24px,5vw,76px);border-top:1px solid #eceef0;color:#777;font-size:12px}.course-shell__footer span:first-child{color:#222;font-weight:700}.course-shell__footer span:last-child{margin-left:auto}.course-shell a:focus-visible,.course-shell button:focus-visible{outline:3px solid #222;outline-offset:3px}@media(max-width:720px){.course-shell__header{height:auto;min-height:68px;gap:20px;padding:10px 18px}.course-shell__brand{font-size:16px}.course-shell nav{gap:16px}.course-shell nav a,.course-shell__account a,.course-shell__account button{font-size:11px}.course-shell__account{gap:10px}.course-shell__signup{padding:8px 11px}.course-shell__search{padding:14px 18px 0}.course-shell__main{padding:24px 18px 54px}.course-shell__footer{gap:12px;padding:0 18px;font-size:10px}}@media(max-width:460px){.course-shell__header{flex-wrap:wrap;row-gap:6px}.course-shell nav{order:3;width:100%;height:34px}.course-shell nav a{height:34px}.course-shell__account{gap:9px}.course-shell__account a,.course-shell__account button{font-size:10px}.course-shell__brand{margin-right:auto}}
</style>
