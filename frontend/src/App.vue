  <script setup>
import * as PortOne from '@portone/browser-sdk/v2'
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { API_BASE_URL } from './api/client'
import { completeKakaoLogin as exchangeKakaoLogin, getCurrentUser, getKakaoLoginState, logoutUser } from './api/auth'
import { getCourse, listCourses } from './api/courses'
import { confirmPayment, createCheckout, getEnrollment, listEnrollments } from './api/payments'
import { resolveRoute } from './router'
import { useSavedCoursesStore } from './stores/savedCourses'
import CourseAuthView from './views/CourseAuthView.vue'
import CourseCatalogView from './views/CourseCatalogView.vue'
import CourseDetailView from './views/CourseDetailView.vue'
import CheckoutView from './views/CheckoutView.vue'
import LearningView from './views/LearningView.vue'
import MyCoursesView from './views/MyCoursesView.vue'
import PaymentSuccessView from './views/PaymentSuccessView.vue'

const route = ref(window.location.pathname)
const courses = ref([])
const course = ref(null)
const loading = ref(false)
const loadError = ref('')
const requestId = ref(0)
const currentUser = ref(null)
const authBusy = ref(false)
const authMessage = ref('')
const paymentBusy = ref(false)
const paymentMessage = ref('')
const isEnrolled = ref(false)
const myCourses = ref([])
const { savedCourseIds, toggle: toggleSavedCourse } = useSavedCoursesStore()
const myCoursesLoading = ref(false)
const myCoursesError = ref('')
const completedCourse = ref(null)
const learningCourse = ref(null)
const activeLessonIndex = ref(0)
const learningError = ref('')

const lessonCatalog = [
  { title: '강의 시작하기', duration: '05:20', note: '이번 강의에서 다룰 내용과 학습 순서를 살펴봅니다. 각 단원을 따라가며 핵심 개념을 정리해 보세요.' },
  { title: '핵심 개념 이해하기', duration: '12:40', note: '기본 개념을 작은 예제로 확인합니다. 먼저 입력과 출력의 관계를 이해하고, 각 단계가 어떤 역할을 하는지 직접 적어 보세요.' },
  { title: '첫 번째 실습', duration: '18:15', note: '배운 내용을 간단한 실습으로 적용합니다. 코드를 실행한 뒤 결과를 확인하고, 값을 바꿔 보며 동작 차이를 비교해 보세요.' },
  { title: '정리와 다음 단계', duration: '08:30', note: '이번 단원의 핵심을 복습하고 다음 학습으로 이어갑니다. 모르는 부분은 앞 단원으로 돌아가 다시 확인해도 좋습니다.' },
]
const activeLessons = computed(() => {
  const title = learningCourse.value?.title?.toLocaleLowerCase('ko-KR') || ''
  if (title.includes('fastapi')) return [
    { title: 'FastAPI와 첫 번째 API', duration: '08:10', note: 'FastAPI는 Python 타입 힌트를 바탕으로 요청과 응답을 다루는 웹 프레임워크입니다. 앱 인스턴스를 만들고 경로 함수에 HTTP 메서드와 URL을 연결해 첫 API를 구성해 봅니다.' },
    { title: '요청 데이터와 Pydantic', duration: '14:25', note: '요청 본문을 Pydantic 모델로 선언하면 데이터 형식을 검증하고 API 문서에도 구조를 표시할 수 있습니다. 필수 값과 기본값을 나누어 요청 모델을 설계해 보세요.' },
    { title: '응답 모델과 오류 처리', duration: '12:40', note: '응답 모델로 반환 데이터의 형태를 명확하게 하고, HTTPException으로 찾을 수 없는 데이터나 잘못된 요청을 알맞은 상태 코드와 함께 처리합니다.' },
    { title: '라우터와 API 문서', duration: '16:05', note: '기능별 APIRouter로 엔드포인트를 나누고 메인 앱에 등록합니다. 자동 생성되는 OpenAPI 문서에서 요청과 응답을 확인하며 API를 점검해 보세요.' },
  ]
  if (title.includes('sql')) return [
    { title: '데이터베이스와 테이블', duration: '07:30', note: '데이터베이스는 정보를 테이블과 행으로 정리합니다. 컬럼의 이름과 자료형, 기본 키를 정해 작은 학습 데이터 테이블을 설계해 보세요.' },
    { title: 'SELECT로 데이터 조회하기', duration: '13:20', note: 'SELECT와 WHERE 조건으로 필요한 행을 찾고 ORDER BY로 결과 순서를 정합니다. 조건을 하나씩 바꾸며 조회 결과가 어떻게 달라지는지 비교해 보세요.' },
    { title: '데이터 추가·수정·삭제', duration: '15:45', note: 'INSERT, UPDATE, DELETE 문으로 데이터를 관리합니다. UPDATE와 DELETE에는 WHERE 조건을 확인하고, 변경 전 대상 행을 조회하는 습관을 들여 보세요.' },
    { title: 'JOIN으로 테이블 연결하기', duration: '18:10', note: '관련된 테이블을 공통 키로 연결하면 여러 곳에 중복 저장하지 않고도 필요한 정보를 함께 조회할 수 있습니다. INNER JOIN과 LEFT JOIN의 결과를 비교해 보세요.' },
  ]
  return lessonCatalog
})

const routeInfo = computed(() => resolveRoute(route.value))
const currentCourseId = computed(() => routeInfo.value.courseId || '')
const currentPage = computed(() => routeInfo.value.name)

function navigate(path) {
  if (path === route.value) return
  const update = async () => {
    window.history.pushState({}, '', path)
    route.value = window.location.pathname
    authMessage.value = ''
    await nextTick()
    const behavior = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
    if (window.location.hash) document.getElementById(decodeURIComponent(window.location.hash.slice(1)))?.scrollIntoView({ behavior })
    else window.scrollTo({ top: 0, behavior })
  }
  transitionPage(update)
}

function onPopState() {
  const update = async () => {
    route.value = window.location.pathname
    authMessage.value = ''
    await nextTick()
    const behavior = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
    if (window.location.hash) document.getElementById(decodeURIComponent(window.location.hash.slice(1)))?.scrollIntoView({ behavior })
    else window.scrollTo({ top: 0, behavior })
  }
  transitionPage(update)
}

function transitionPage(update) {
  if (document.startViewTransition) {
    try {
      document.startViewTransition(update)
      return
    } catch {
      // Continue navigation if the browser cannot start a view transition.
    }
  }
  update()
}

async function requestCourses(path) {
  const request = ++requestId.value
  loading.value = true
  loadError.value = ''
  course.value = null
  try {
    const courseMatch = path.match(/^\/courses\/([^/]+)$/)
    const response = path === '/courses'
      ? await listCourses()
      : await getCourse(courseMatch ? decodeURIComponent(courseMatch[1]) : currentCourseId.value)
    const payload = await response.json()
    if (!response.ok || payload.code !== 200) {
      throw new Error(payload.message || (response.status === 404 ? '요청한 강의를 찾을 수 없습니다.' : '강의 정보를 불러오지 못했습니다.'))
    }
    if (request !== requestId.value) return
    if (path === '/courses') {
      if (!Array.isArray(payload.result)) throw new Error('강의 목록 응답 형식이 올바르지 않습니다.')
      courses.value = payload.result
    } else {
      if (!payload.result || typeof payload.result !== 'object') throw new Error('강의 상세 응답 형식이 올바르지 않습니다.')
      course.value = payload.result
    }
  } catch (error) {
    if (request !== requestId.value) return
    loadError.value = error instanceof TypeError
      ? `서버(${API_BASE_URL})에 연결할 수 없습니다. 백엔드가 실행 중인지 확인해 주세요.`
      : error.message || '강의 정보를 불러오지 못했습니다.'
  } finally {
    if (request === requestId.value) loading.value = false
  }
}

function loadCurrentRoute() {
  if (currentPage.value === 'detail') requestCourses(`/courses/${encodeURIComponent(currentCourseId.value)}`)
  else if (currentPage.value === 'catalog') requestCourses('/courses')
  else if (currentPage.value === 'kakao-callback') completeKakaoLogin()
  else if (currentPage.value === 'my-courses') loadMyCourses()
  else if (currentPage.value === 'learning') loadLearningCourse()
  else if (currentPage.value === 'checkout') loadCheckoutCourse()
  else if (currentPage.value === 'payment-success') loadPaymentSuccessCourse()
}

async function loadMyCourses() {
  myCoursesLoading.value = true
  myCoursesError.value = ''
  try {
    const response = await listEnrollments()
    const payload = await response.json()
    if (!response.ok || payload.code !== 200) throw new Error(payload.message || '수강 목록을 불러오지 못했습니다.')
    myCourses.value = Array.isArray(payload.result) ? payload.result : []
  } catch (error) {
    myCoursesError.value = error.message || '수강 목록을 불러오지 못했습니다.'
  } finally {
    myCoursesLoading.value = false
  }
}

async function loadPaymentSuccessCourse() {
  const courseId = new URLSearchParams(window.location.search).get('courseId')
  if (!courseId) return
  try {
    const response = await getCourse(courseId)
    const payload = await response.json()
    if (response.ok && payload.code === 200) completedCourse.value = payload.result
  } catch {
    completedCourse.value = null
  }
}

async function loadCheckoutCourse() {
  const courseId = new URLSearchParams(window.location.search).get('courseId')
  if (!courseId) { navigate('/courses'); return }
  if (!currentUser.value) await checkCurrentUser()
  if (!currentUser.value) { navigate('/login'); return }
  await requestCourses(`/courses/${encodeURIComponent(courseId)}`)
}

async function loadLearningCourse() {
  const match = route.value.match(/^\/my\/courses\/(\d+)\/learn\/?$/)
  if (!match) return
  learningError.value = ''
  learningCourse.value = null
  if (!currentUser.value) await checkCurrentUser()
  if (!currentUser.value) { navigate('/login'); return }
  try {
    const enrollmentResponse = await getEnrollment(match[1])
    const enrollment = await enrollmentResponse.json()
    if (!enrollmentResponse.ok || enrollment.code !== 200 || !enrollment.result) throw new Error('이 강의의 수강 권한을 확인할 수 없습니다. 마이페이지에서 구매 내역을 확인해 주세요.')
    const courseResponse = await getCourse(match[1])
    const payload = await courseResponse.json()
    if (!courseResponse.ok || payload.code !== 200) throw new Error(payload.message || '강의 정보를 불러오지 못했습니다.')
    learningCourse.value = payload.result
  } catch (error) { learningError.value = error.message || '강의를 불러오지 못했습니다.' }
}

async function checkCurrentUser() {
  try {
    const response = await getCurrentUser()
    if (!response.ok) return
    const payload = await response.json()
    if (payload.code === 200) {
      currentUser.value = payload.result
      if (currentCourseId.value) checkEnrollment(currentCourseId.value)
    }
  } catch {
    // Browsing courses remains available when authentication is not configured.
  }
}

async function checkEnrollment(courseId) {
  if (!currentUser.value) {
    isEnrolled.value = false
    return
  }
  try {
    const response = await getEnrollment(courseId)
    const payload = await response.json()
    if (response.ok && payload.code === 200) isEnrolled.value = Boolean(payload.result)
  } catch {
    isEnrolled.value = false
  }
}

async function confirmPortOnePayment(paymentId) {
  const response = await confirmPayment(paymentId)
  const payload = await response.json()
  if (!response.ok || payload.code !== 200) throw new Error(payload.message || '결제를 확인하지 못했습니다.')
  isEnrolled.value = true
  paymentMessage.value = '결제가 완료되어 강의 수강이 등록되었습니다.'
}

async function purchaseCourse() {
  if (!currentUser.value) {
    paymentMessage.value = '구매하려면 먼저 로그인해 주세요.'
    navigate('/login')
    return
  }
  if (isEnrolled.value) {
    navigate(`/my/courses/${course.value.id}/learn`)
    return
  }
  if (!course.value || paymentBusy.value) return
  navigate(`/checkout?courseId=${encodeURIComponent(course.value.id)}`)
}

async function startCheckoutPayment() {
  if (!course.value || paymentBusy.value) return
  paymentBusy.value = true
  paymentMessage.value = ''
  try {
    const orderResponse = await createCheckout(course.value.id)
    const orderPayload = await orderResponse.json()
    if (!orderResponse.ok || orderPayload.code !== 200) throw new Error(orderPayload.message || '결제 준비에 실패했습니다.')
    const order = orderPayload.result
    const result = await PortOne.requestPayment({
      storeId: order.store_id,
      channelKey: order.channel_key,
      paymentId: order.payment_id,
      orderName: order.order_name,
      totalAmount: order.amount,
      currency: 'KRW',
      payMethod: 'CARD',
      redirectUrl: `${window.location.origin}/payment/success?courseId=${encodeURIComponent(course.value.id)}`,
    })
    if (result?.code) throw new Error(result.message || '결제가 취소되었거나 실패했습니다.')
    if (result?.paymentId) {
      await confirmPortOnePayment(result.paymentId)
      navigate(`/payment/success?courseId=${encodeURIComponent(course.value.id)}`)
    }
  } catch (error) {
    paymentMessage.value = error instanceof TypeError
      ? `결제 서버(${API_BASE_URL})에 연결할 수 없습니다.`
      : error.message || '결제를 완료하지 못했습니다.'
  } finally {
    paymentBusy.value = false
  }
}

async function completePaymentRedirect() {
  const params = new URLSearchParams(window.location.search)
  const paymentId = params.get('paymentId')
  if (!paymentId) return
  paymentBusy.value = true
  paymentMessage.value = ''
  try {
    const code = params.get('code')
    if (code) throw new Error(params.get('message') || '결제가 취소되었거나 실패했습니다.')
    await confirmPortOnePayment(paymentId)
    await loadPaymentSuccessCourse()
  } catch (error) {
    paymentMessage.value = error.message || '결제 결과를 확인하지 못했습니다.'
  } finally {
    const courseId = params.get('courseId')
    window.history.replaceState({}, '', courseId ? `/payment/success?courseId=${encodeURIComponent(courseId)}` : '/payment/success')
    paymentBusy.value = false
  }
}

async function startKakaoLogin() {
  authBusy.value = true
  authMessage.value = ''
  try {
    const response = await getKakaoLoginState()
    const payload = await response.json()
    if (!response.ok || payload.code !== 200) throw new Error(payload.message || '카카오 로그인을 시작하지 못했습니다.')
    if (!window.Kakao?.Auth?.authorize) throw new Error('카카오 로그인을 사용할 수 없습니다. JavaScript 키 설정을 확인해 주세요.')
    window.Kakao.Auth.authorize({ redirectUri: payload.result.redirect_uri, state: payload.result.state })
  } catch (error) {
    authMessage.value = error instanceof TypeError
      ? `서버(${API_BASE_URL})에 연결할 수 없습니다. 백엔드가 실행 중인지 확인해 주세요.`
      : error.message || '카카오 로그인을 시작하지 못했습니다.'
    authBusy.value = false
  }
}

async function completeKakaoLogin() {
  const params = new URLSearchParams(window.location.search)
  const code = params.get('code')
  const state = params.get('state')
  if (params.has('error')) {
    authMessage.value = params.get('error_description') || '카카오 로그인이 취소되었습니다.'
    return
  }
  if (!code || !state) {
    authMessage.value = '로그인 응답을 확인할 수 없습니다. 다시 시도해 주세요.'
    return
  }
  authBusy.value = true
  try {
    const response = await exchangeKakaoLogin(code, state)
    const payload = await response.json()
    if (!response.ok || payload.code !== 200) throw new Error(payload.message || '카카오 로그인에 실패했습니다.')
    currentUser.value = payload.result
    window.history.replaceState({}, '', '/auth/kakao/callback')
    navigate('/courses')
  } catch (error) {
    authMessage.value = error instanceof TypeError
      ? `서버(${API_BASE_URL})에 연결할 수 없습니다. 백엔드가 실행 중인지 확인해 주세요.`
      : error.message || '카카오 로그인에 실패했습니다.'
    window.history.replaceState({}, '', '/auth/kakao/callback')
  } finally {
    authBusy.value = false
  }
}

async function logout() {
  try {
    const response = await logoutUser()
    if (!response.ok) throw new Error('로그아웃하지 못했습니다. 다시 시도해 주세요.')
    currentUser.value = null
  } catch (error) {
    authMessage.value = error.message || '로그아웃하지 못했습니다.'
  }
}

function showEmailAuthNotice() {
  authMessage.value = '이메일 계정 로그인과 가입은 아직 연결되지 않았습니다. 카카오로 계속해 주세요.'
}

watch(route, loadCurrentRoute)
watch([course, currentUser], ([selectedCourse, user]) => {
  if (selectedCourse && user) checkEnrollment(selectedCourse.id)
  else isEnrolled.value = false
})
onMounted(() => {
  window.addEventListener('popstate', onPopState)
  checkCurrentUser()
  loadCurrentRoute()
  completePaymentRedirect()
})
onUnmounted(() => window.removeEventListener('popstate', onPopState))
</script>

<template>
  <template v-if="currentPage === 'catalog'">
    <CourseCatalogView :courses="courses" :loading="loading" :error="loadError" :current-user="currentUser" :saved-course-ids="savedCourseIds" @navigate="navigate" @retry="loadCurrentRoute" @logout="logout" @toggle-save="toggleSavedCourse" />
  </template>
  <template v-else-if="currentPage === 'detail'">
    <CourseDetailView :course="course" :loading="loading" :error="loadError" :payment-busy="paymentBusy" :is-enrolled="isEnrolled" :current-user="currentUser" :saved-course-ids="savedCourseIds" @navigate="navigate" @purchase="purchaseCourse" @retry="loadCurrentRoute" @logout="logout" @toggle-save="toggleSavedCourse" />
  </template>
  <template v-else-if="currentPage === 'login' || currentPage === 'signup' || currentPage === 'kakao-callback'">
    <CourseAuthView :mode="currentPage" :busy="authBusy" :error="authMessage" :callback="currentPage === 'kakao-callback'" @navigate="navigate" @submit="showEmailAuthNotice" @social-login="startKakaoLogin" />
  </template>
  <template v-else-if="currentPage === 'checkout'">
    <CheckoutView :course="course" :loading="loading" :payment-busy="paymentBusy" :message="paymentMessage" :current-user="currentUser" @navigate="navigate" @pay="startCheckoutPayment" @logout="logout" />
  </template>
  <template v-else-if="currentPage === 'my-courses'">
    <MyCoursesView :courses="myCourses" :loading="myCoursesLoading" :error="myCoursesError" :current-user="currentUser" @navigate="navigate" @retry="loadMyCourses" @logout="logout" />
  </template>
  <template v-else-if="currentPage === 'learning'">
    <LearningView :course="learningCourse" :lessons="activeLessons" :active-index="activeLessonIndex" :error="learningError" :current-user="currentUser" @navigate="navigate" @select-lesson="activeLessonIndex = $event" @next-lesson="activeLessonIndex = (activeLessonIndex + 1) % activeLessons.length" @logout="logout" />
  </template>
  <template v-else-if="currentPage === 'payment-success'">
    <PaymentSuccessView :course="completedCourse" :busy="paymentBusy" :enrolled="isEnrolled" :message="paymentMessage" :current-user="currentUser" @navigate="navigate" @logout="logout" />
  </template>
</template>
