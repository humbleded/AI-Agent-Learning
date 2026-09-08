<script setup lang="ts">
import { computed } from "vue";
import { renderMarkdown } from "../lib/markdown";

const props = defineProps<{ content: string }>();
const rendered = computed(() => renderMarkdown(props.content));
</script>

<template>
  <div class="markdown-text" v-html="rendered" />
</template>

<style scoped>
.markdown-text { line-height: 1.9; overflow-wrap: anywhere; min-width: 0; font-size: 14px; }
.markdown-text :deep(> :first-child) { margin-top: 0; }
.markdown-text :deep(> :last-child) { margin-bottom: 0; }
.markdown-text :deep(p) { margin: 0 0 1em; }
.markdown-text :deep(h1), .markdown-text :deep(h2), .markdown-text :deep(h3), .markdown-text :deep(h4) { font-size: 1.15em; line-height: 1.5; margin: 1.4em 0 .65em; }
.markdown-text :deep(ul), .markdown-text :deep(ol) { padding-left: 1.6em; margin: .7em 0 1em; }
.markdown-text :deep(li) { margin: .35em 0; }
.markdown-text :deep(code) { font-family: Consolas, monospace; font-size: .88em; background: color-mix(in srgb, currentColor 8%, transparent); padding: .12em .35em; border-radius: 4px; }
.markdown-text :deep(pre) { overflow-x: auto; white-space: pre; padding: 16px; border-radius: 10px; background: color-mix(in srgb, currentColor 5%, transparent); line-height: 1.7; }
.markdown-text :deep(pre code) { padding: 0; background: none; }
.markdown-text :deep(blockquote) { margin: 1em 0; padding: .3em 1em; border-left: 3px solid var(--wb-accent, #41bea8); opacity: .85; }
.markdown-text :deep(blockquote p) { margin: .4em 0; }
.markdown-text :deep(table) { display: block; overflow-x: auto; border-collapse: collapse; width: 100%; }
.markdown-text :deep(th), .markdown-text :deep(td) { border: 1px solid color-mix(in srgb, currentColor 15%, transparent); padding: 8px 12px; text-align: left; }
.markdown-text :deep(hr) { border: 0; border-top: 1px solid color-mix(in srgb, currentColor 15%, transparent); margin: 1.5em 0; }
</style>
