<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ArrowRight, FileText, LibraryBig } from "@lucide/vue";
import { getJson, type DocumentInfo } from "../lib/api";
const sample = ref<{
  file_name: string;
  content: string;
  metadata: Record<string, unknown>;
  fictional: boolean;
} | null>(null);
const docs = ref<DocumentInfo[]>([]);
const importState = ref<"idle" | "loading" | "success" | "failed">("idle");
const busy = computed(() => importState.value === "loading");
const importStatus = computed(() => ({
  idle: "待导入",
  loading: "正在导入",
  success: `导入成功 · ${docs.value.length} 张资料卡片`,
  failed: "导入失败",
})[importState.value]);
const message = ref("");
const sampleError = ref("");
onMounted(async () => {
  try {
    sample.value = await getJson("/api/rag/sample");
  } catch (e) {
    sampleError.value = (e as Error).message;
  }
});
async function importFile() {
  if (busy.value) return;
  importState.value = "loading";
  message.value = "";
  docs.value = [];
  try {
    docs.value = (
      await getJson<{ documents: DocumentInfo[] }>("/api/rag/import", {
        method: "POST",
      })
    ).documents;
    if (!docs.value.length) throw new Error("工作流没有返回资料，请检查导入结果后重试。");
    importState.value = "success";
  } catch (e) {
    message.value = (e as Error).message;
    importState.value = "failed";
  }
}
</script>
<template>
  <div class="page-intro">
    <div>
      <span class="eyebrow">ENGINEERING DOCUMENTS</span>
      <h1>从文件，走向有依据的回答。</h1>
      <p>当前目标：用 Docling 解析文件，再通过 LangGraph 返回资料卡片。</p>
    </div>
    <span class="subtle-pill" role="status">{{ importStatus }}</span>
  </div>
  <div class="learning-callout">
    <LibraryBig :size="22" />
    <div>
      <strong>查看当前工作流实际读到了什么。</strong>
      <p>
        点击导入后，页面会展示工作流实际返回的正文与来源。导入成功表示资料已被读取；是否进入检索，需要在后续建立索引后核验。
      </p>
    </div>
  </div>
  <div class="document-flow">
    <span>样本文件</span><ArrowRight :size="16" /><span>DoclingLoader</span
    ><ArrowRight :size="16" /><span>LangGraph 状态</span
    ><ArrowRight :size="16" /><span>资料卡片</span>
  </div>
  <div class="document-grid">
    <section class="panel">
      <div class="panel-heading">
        <h2><FileText :size="18" /> {{ sample?.file_name ?? "教学资料" }}</h2>
        <ElTag size="small" type="info">解析预览</ElTag>
      </div>
      <p class="field-help">
        以下为 Docling 解析后的 Markdown，标题和空白可能重新排版；这份预览与下方工作流导入分别执行。
      </p>
      <ElAlert v-if="sampleError" :title="sampleError" type="warning" :closable="false" show-icon />
      <pre class="document-source">{{
        sample?.content ?? (sampleError ? "样本预览暂不可用。仍可尝试运行当前导入工作流。" : "正在解析样本…")
      }}</pre>
      <ElButton
        type="primary"
        size="large"
        :loading="busy"
        :disabled="busy"
        @click="importFile"
        >{{ busy ? "正在导入" : "通过工作流导入" }} <ArrowRight :size="16"
      /></ElButton>
    </section>
    <section class="panel">
      <div class="panel-heading">
        <h2>工作流返回的资料</h2>
        <span class="counter">{{ importStatus }}</span>
      </div>
      <ElAlert
        v-if="message"
        :title="message"
        type="warning"
        :closable="false"
        show-icon
      />
      <div v-if="!docs.length" class="empty-state">
        <LibraryBig :size="38" />
        <h3>{{ importState === "loading" ? "工作流正在读取资料" : importState === "failed" ? "本次没有导入成功" : "等待真实导入结果" }}</h3>
        <p>{{ importState === "loading" ? "收到真实结果后，这里会展示正文与来源。" : importState === "failed" ? "请根据上方错误检查文件或工作流，再点击导入重试。" : "点击“通过工作流导入”，运行当前的文档读取流程。" }}</p>
      </div>
      <article v-for="(doc, index) in docs" :key="index" class="document-card">
        <ElTag size="small">Document {{ index + 1 }}</ElTag>
        <pre>{{ doc.page_content }}</pre>
        <div class="metadata">
          <strong>来源、版本与位置</strong>
          <pre>{{ JSON.stringify(doc.metadata, null, 2) }}</pre>
        </div>
      </article>
    </section>
  </div>
</template>
