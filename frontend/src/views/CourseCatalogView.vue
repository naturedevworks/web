<script setup>
import { computed, ref } from 'vue'
import CourseCard from '../components/CourseCard.vue'
import CourseCategoryNav from '../components/CourseCategoryNav.vue'
import CoursePageShell from '../components/CoursePageShell.vue'
import CourseSearchBar from '../components/CourseSearchBar.vue'

const props = defineProps({ courses: { type: Array, default: () => [] }, loading: { type: Boolean, default: false }, error: { type: String, default: '' }, currentUser: { type: Object, default: null }, savedCourseIds: { type: Array, default: () => [] } })
const emit = defineEmits(['navigate', 'retry', 'logout', 'toggle-save'])
const category = ref('전체')
const query = ref('')
const categories = computed(() => ['전체', ...new Set(props.courses.map((course) => course.level).filter(Boolean))])
const filteredCourses = computed(() => props.courses.filter((course) => {
  const matchesCategory = category.value === '전체' || course.level === category.value
  const searchable = `${course.title || ''} ${course.description || ''} ${course.instructor_name || ''} ${course.category || ''}`.toLocaleLowerCase('ko-KR')
  return matchesCategory && (!query.value || searchable.includes(query.value.toLocaleLowerCase('ko-KR')))
}))

function searchCourses(value) { query.value = value }
function scrollToCourses() {
  document.getElementById('course-list')?.scrollIntoView({
    behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
  })
}
function showBeginnerCourses() {
  category.value = categories.value.find((item) => item.includes('입문')) || '전체'
  scrollToCourses()
}
</script>

<template>
  <CoursePageShell :current-user="currentUser" @navigate="emit('navigate', $event)" @logout="emit('logout')">
    <template #search><CourseSearchBar @search="searchCourses" /></template>
    <section class="course-catalog">
      <div class="course-catalog__spotlight">
        <div class="course-catalog__welcome">
          <p class="course-catalog__kicker"><span aria-hidden="true"></span> 배움 클래스</p>
          <h1>배우고 싶은 순간,<br />지금 시작해요.</h1>
          <p class="course-catalog__lead">관심 있던 분야의 지식을 내 것으로 만드는 강의를 만나보세요.</p>
          <a href="#course-list" @click.prevent="scrollToCourses">강의 둘러보기 <span aria-hidden="true">↓</span></a>
          <div class="course-catalog__scribble" aria-hidden="true">배움<span>→</span>실력</div>
        </div>
        <div class="course-catalog__side-promos" aria-label="강의 안내">
          <a class="course-catalog__promo course-catalog__promo--yellow" href="#course-list" @click.prevent="scrollToCourses">
            <span>지금 들을 수 있는 강의</span><strong>{{ courses.length }}개</strong><span class="course-catalog__promo-link">모든 강의 보기 <b aria-hidden="true">↗</b></span>
            <span class="course-catalog__promo-stamp" aria-hidden="true">배</span>
          </a>
          <a class="course-catalog__promo course-catalog__promo--ink" href="#course-list" @click.prevent="showBeginnerCourses">
            <span>처음 배우는 분이라면</span><strong>입문 강의부터<br />가볍게 시작해요</strong><span class="course-catalog__promo-link">입문 강의 보기 <b aria-hidden="true">↗</b></span>
          </a>
        </div>
      </div>
      <section id="course-list" class="course-catalog__listing" aria-labelledby="course-list-title">
        <div class="course-catalog__section-heading"><div><p>관심 분야를 선택해 보세요</p><h2 id="course-list-title">배우고 싶은 강의</h2></div><span v-if="!loading && !error">{{ filteredCourses.length }}개 강의</span></div>
        <div class="course-catalog__filters"><CourseCategoryNav v-model="category" :categories="categories" /></div>
      <div v-if="loading" class="course-catalog__state" role="status"><span class="course-catalog__spinner"></span><p>강의를 불러오고 있어요.</p></div>
      <div v-else-if="error" class="course-catalog__state" role="alert"><h2>강의 목록을 불러오지 못했어요</h2><p>{{ error }}</p><button type="button" @click="emit('retry')">다시 불러오기</button></div>
      <div v-else-if="courses.length === 0" class="course-catalog__state"><h2>아직 등록된 강의가 없어요</h2><p>새로운 강의가 준비되면 이곳에서 만날 수 있어요.</p></div>
      <div v-else-if="filteredCourses.length === 0" class="course-catalog__state"><h2>검색 결과가 없어요</h2><p>다른 검색어나 분야를 선택해 보세요.</p><button type="button" @click="query = ''; category = '전체'">검색 초기화</button></div>
      <section v-else class="course-catalog__grid" aria-label="강의 목록">
        <CourseCard v-for="course in filteredCourses" :key="course.id" :course="course" :saved="savedCourseIds.includes(course.id)" @select="emit('navigate', `/courses/${$event.id}`)" @toggle-save="emit('toggle-save', $event)" />
      </section>
      </section>
    </section>
  </CoursePageShell>
</template>

<style scoped>
.course-catalog{padding-top:8px}.course-catalog__spotlight{display:grid;grid-template-columns:minmax(0,1.85fr) minmax(260px,.92fr);gap:14px;margin-bottom:49px}.course-catalog__welcome{position:relative;min-height:360px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;overflow:hidden;padding:44px clamp(30px,5vw,72px);border-radius:18px;background:#ffff00;color:#222}.course-catalog__kicker{display:flex;align-items:center;gap:9px;margin:0 0 22px;font-size:13px;font-weight:700}.course-catalog__kicker span{width:9px;height:9px;border:2px solid currentColor;border-radius:50%}.course-catalog__welcome h1{position:relative;z-index:1;margin:0;font-size:clamp(34px,4.25vw,58px);line-height:1.2;letter-spacing:-2.6px}.course-catalog__lead{position:relative;z-index:1;max-width:470px;margin:16px 0 24px;color:#383838;font-size:15px;line-height:1.8}.course-catalog__welcome>a{position:relative;z-index:1;display:flex;align-items:center;gap:24px;padding:13px 17px;border-radius:999px;background:#222;color:#fff;font-size:12px;font-weight:700;text-decoration:none;transition:transform .18s ease,background .18s ease}.course-catalog__welcome>a:hover{transform:translateY(-2px);background:#3b3b3b}.course-catalog__welcome>a span{color:#ffff00;font-size:18px;line-height:12px}.course-catalog__scribble{position:absolute;right:5%;bottom:5%;color:#222;font-size:clamp(30px,5vw,68px);font-weight:900;letter-spacing:-5px;opacity:.11;transform:rotate(-8deg);user-select:none}.course-catalog__scribble span{padding:0 8px}.course-catalog__side-promos{display:grid;grid-template-rows:1fr 1fr;gap:14px}.course-catalog__promo{position:relative;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;overflow:hidden;padding:24px 27px;border-radius:16px;text-decoration:none;transition:transform .18s ease}.course-catalog__promo:hover{transform:translateY(-2px)}.course-catalog__promo--yellow{background:#f3f4f5;color:#222}.course-catalog__promo--ink{background:#202124;color:#fff}.course-catalog__promo>span:first-child{margin-bottom:7px;font-size:11px;opacity:.72}.course-catalog__promo strong{font-size:clamp(19px,2vw,25px);line-height:1.28;letter-spacing:-.7px}.course-catalog__promo-link{display:flex;align-items:center;gap:8px;margin-top:13px;font-size:11px;font-weight:700}.course-catalog__promo-link b{font-size:15px}.course-catalog__promo-stamp{position:absolute;right:18px;bottom:-29px;color:#ffff00;font-size:104px;font-weight:900;line-height:1;opacity:.62;transform:rotate(-12deg)}.course-catalog__section-heading{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin:0 0 21px}.course-catalog__section-heading p{margin:0 0 7px;color:#717171;font-size:12px}.course-catalog__section-heading h2{margin:0;font-size:25px;letter-spacing:-.8px}.course-catalog__section-heading>span{flex:none;padding-bottom:3px;color:#717171;font-size:12px}.course-catalog__filters{margin-bottom:23px}.course-catalog__grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:34px 22px}.course-catalog__state{min-height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:32px 18px;text-align:center}.course-catalog__state h2{margin:0;font-size:20px}.course-catalog__state p{max-width:540px;margin:10px 0 0;color:#717171;font-size:13px;line-height:1.7}.course-catalog__state button{min-height:40px;margin-top:18px;padding:0 16px;border:0;border-radius:999px;background:#ffff00;font:inherit;font-size:12px;font-weight:700;cursor:pointer}.course-catalog__spinner{width:26px;height:26px;border:2px solid #eee;border-top-color:#222;border-radius:50%;animation:course-spin .8s linear infinite}.course-catalog__spinner+p{margin-top:12px}@keyframes course-spin{to{transform:rotate(360deg)}}@media(max-width:1000px){.course-catalog__spotlight{grid-template-columns:minmax(0,1.45fr) minmax(230px,.8fr)}.course-catalog__welcome{min-height:330px}.course-catalog__grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 18px}}@media(max-width:700px){.course-catalog__spotlight{grid-template-columns:1fr;gap:11px;margin-bottom:38px}.course-catalog__welcome{min-height:310px;padding:34px 27px}.course-catalog__welcome h1{font-size:clamp(34px,8vw,47px)}.course-catalog__lead{max-width:350px;font-size:13px}.course-catalog__side-promos{grid-template-columns:1fr 1fr;grid-template-rows:150px;gap:10px}.course-catalog__promo{padding:17px;border-radius:13px}.course-catalog__promo strong{font-size:18px}.course-catalog__promo>span:first-child,.course-catalog__promo-link{font-size:10px}.course-catalog__grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:27px 14px}.course-catalog__section-heading h2{font-size:22px}}@media(max-width:420px){.course-catalog__welcome{min-height:290px;padding:30px 22px}.course-catalog__side-promos{grid-template-columns:1fr;grid-template-rows:135px 150px}.course-catalog__grid{gap:25px 11px}.course-catalog__section-heading h2{font-size:20px}}@media(prefers-reduced-motion:reduce){.course-catalog__spinner{animation-duration:.01ms}.course-catalog__welcome>a,.course-catalog__promo{transition:none}}
</style>
