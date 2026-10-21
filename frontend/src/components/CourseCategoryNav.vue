<script setup>
defineProps({
  categories: { type: Array, default: () => ['전체', '프로그래밍', '데이터', '디자인', '비즈니스', '커리어'] },
  modelValue: { type: String, default: '전체' },
})

const emit = defineEmits(['update:modelValue', 'select'])
</script>

<template>
  <nav class="course-categories" aria-label="강의 분야">
    <button v-for="category in categories" :key="category" class="course-categories__item" :class="{ 'is-active': modelValue === category }" type="button" :aria-pressed="modelValue === category" @click="emit('update:modelValue', category); emit('select', category)">
      <span class="course-categories__icon" aria-hidden="true">{{ category === '전체' ? '▦' : '◈' }}</span><span>{{ category }}</span>
    </button>
  </nav>
</template>

<style scoped>
.course-categories{display:flex;gap:9px;overflow-x:auto;padding:2px 1px 7px;scrollbar-width:none}.course-categories::-webkit-scrollbar{display:none}.course-categories__item{display:flex;min-width:max-content;align-items:center;gap:8px;padding:10px 15px;border:1px solid #e4e6e8;border-radius:999px;background:#fff;color:#5f6368;font:inherit;font-size:12px;cursor:pointer;transition:border-color .16s ease,background .16s ease,color .16s ease}.course-categories__icon{display:grid;width:20px;height:20px;place-items:center;border-radius:50%;background:#f0f1f2;color:#4a4d50;font-size:11px;line-height:1}.course-categories__item:hover{border-color:#b8bbc0;color:#222}.course-categories__item.is-active{border-color:#222;background:#222;color:#fff;font-weight:700}.course-categories__item.is-active .course-categories__icon{background:#ffff00;color:#222}.course-categories__item:focus-visible{outline:3px solid #222;outline-offset:3px}@media(prefers-reduced-motion:reduce){.course-categories__item{transition:none}}
</style>
