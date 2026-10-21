<script setup>
import { ref, watch } from 'vue'
const props = defineProps({ images: { type: Array, default: () => [] }, title: { type: String, default: '강의' } })
const mainImageFailed = ref(false)
watch(() => props.images[0]?.src, () => { mainImageFailed.value = false })
</script>

<template>
  <section class="course-gallery" :aria-label="`${title} 강의 이미지`">
    <img v-if="images[0]?.src && !mainImageFailed" class="course-gallery__main" :src="images[0].src" :alt="images[0].alt || title" @error="mainImageFailed = true" />
    <div v-else class="course-gallery__main course-gallery__placeholder" aria-hidden="true"><span>{{ images[0]?.label || '배우고 성장하는 시간' }}</span></div>
    <div class="course-gallery__side"><div v-for="(image, index) in images.slice(1, 3)" :key="image.src || index" class="course-gallery__tile"><img v-if="image.src" :src="image.src" :alt="image.alt || `${title} 이미지 ${index + 2}`" /><span v-else>{{ image.label || '강의 미리보기' }}</span></div><div v-if="images.length < 3" class="course-gallery__tile"><span>커리큘럼과 강의 자료를 확인해 보세요</span></div></div>
  </section>
</template>

<style scoped>
.course-gallery{display:grid;grid-template-columns:1.55fr 1fr;gap:12px;height:clamp(260px,34vw,420px);overflow:hidden;border-radius:18px}.course-gallery__main,.course-gallery__tile{width:100%;height:100%;object-fit:cover}.course-gallery__placeholder,.course-gallery__tile{display:grid;place-items:center;background:#f3f4f5;color:#303236;text-align:center}.course-gallery__placeholder{position:relative;isolation:isolate;overflow:hidden;font-size:22px;font-weight:800}.course-gallery__placeholder:before{position:absolute;z-index:-1;width:220px;height:220px;border-radius:50%;background:#ffff00;content:""}.course-gallery__placeholder:after{position:absolute;z-index:-1;right:12%;bottom:-115px;width:280px;height:180px;border:1px solid #22222220;border-radius:50%;content:""}.course-gallery__placeholder span{max-width:80%;line-height:1.5}.course-gallery__side{display:grid;grid-template-rows:1fr 1fr;gap:12px;min-height:0}.course-gallery__tile{position:relative;overflow:hidden;padding:18px;border-radius:14px;background:#f3f4f5;color:#4b4e52;font-size:13px}.course-gallery__tile:nth-child(2){background:#222;color:#fff}.course-gallery__tile img{width:100%;height:100%;object-fit:cover}@media(max-width:620px){.course-gallery{grid-template-columns:1fr;height:240px;border-radius:14px}.course-gallery__side{display:none}}@media(prefers-reduced-motion:reduce){.course-gallery *{scroll-behavior:auto}}
</style>
