<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search'])
const query = ref('')

function submitSearch() {
  emit('search', query.value.trim())
}
</script>

<template>
  <form class="course-search" role="search" @submit.prevent="submitSearch">
    <svg class="course-search__symbol" aria-hidden="true" viewBox="0 0 24 24"><circle cx="10.8" cy="10.8" r="6.2" /><path d="m15.4 15.4 4.2 4.2" /></svg>
    <label class="course-search__label" for="course-search-input">강의 검색</label>
    <input id="course-search-input" v-model="query" name="q" type="search" placeholder="관심 있는 강의나 주제를 검색해 보세요" />
    <button class="course-search__submit" type="submit" aria-label="강의 검색"><svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="10.8" cy="10.8" r="6.2" /><path d="m15.4 15.4 4.2 4.2" /></svg></button>
  </form>
</template>

<style scoped>
.course-search{position:relative;display:flex;align-items:center;gap:13px;width:min(100%,650px);height:60px;margin:0 auto;padding:5px 6px 5px 20px;border:1px solid #dfe2e5;border-radius:999px;background:#fff;transition:border-color .18s ease,box-shadow .18s ease}.course-search:focus-within{border-color:#b7b9bc;box-shadow:0 0 0 3px #2222220a}.course-search__symbol{width:21px;height:21px;flex:none;fill:none;stroke:#686c70;stroke-width:1.7;stroke-linecap:round}.course-search__label{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;clip-path:inset(50%)}.course-search input{width:100%;min-width:0;flex:1;border:0;outline:0;background:transparent;color:#222;font:inherit;font-size:14px}.course-search input::placeholder{color:#8a8d91}.course-search input:focus-visible{outline:none}.course-search__submit{width:48px;height:48px;display:grid;flex:none;place-items:center;border:0;border-radius:50%;background:#ffff00;color:#222;font:inherit;cursor:pointer;transition:background .18s ease,transform .18s ease}.course-search__submit svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round}.course-search__submit:hover{transform:scale(1.04);background:#eded00}.course-search__submit:focus-visible{outline:3px solid #222;outline-offset:3px}@media(max-width:620px){.course-search{height:54px;padding-left:16px}.course-search input{font-size:12px}.course-search__submit{width:42px;height:42px}}
</style>
