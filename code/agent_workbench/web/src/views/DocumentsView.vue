<script setup lang="ts">
import { onMounted, ref } from "vue";
import { ArrowRight, FileText, LibraryBig } from "@lucide/vue";
import { getJson, type DocumentInfo } from "../lib/api";
const sample = ref<{
  file_name: string;
  content: string;
  metadata: Record<string, unknown>;
  fictional: boolean;
} | null>(null);
const docs = ref<DocumentInfo[]>([]);
const busy = ref(false);
const message = ref("");
onMounted(async () => {
  try {
    sample.value = await getJson("/api/rag/sample");
  } catch (e) {
    message.value = (e as Error).message;
  }
});
async function importFile() {
  busy.value = true;
  message.value = "";
  docs.value = [];
  try {
    docs.value = (
      await getJson<{ documents: DocumentInfo[] }>("/api/rag/import", {
        method: "POST",
      })
    ).documents;
  } catch (e) {
    message.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
</script>
<template>
  <div class="page-intro">
    <div>
      <span class="eyebrow">ENGINEERING DOCUMENTS</span>
      <h1>从文件，走向有依据的回答。</h1>
      <p>当前目标：用 LangChain 读取文件，再通过 LangGraph 返回资料卡片。</p>
    </div>
    <span class="subtle-pill">当前学习：R6-01 · G3</span>
  </div>
  <div class="learning-callout">
    <LibraryBig :size="22" />
    <div>
      <strong>这张页面，已经为你的读取节点准备好了。</strong>
      <p>
        完成 ingest.py 的 load_documents 与 build_ingest_graph
        后，再点一次导入。页面会展示你的代码实际返回的正文与来源。
      </p>
    </div>
  </div>
  <div class="document-flow">
    <span>样本文件</span><ArrowRight :size="16" /><span>LangChain Loader</span
    ><ArrowRight :size="16" /><span>LangGraph 状态</span
    ><ArrowRight :size="16" /><span>资料卡片</span>
  </div>
  <div class="document-grid">
    <section class="panel">
      <div class="panel-heading">
        <h2><FileText :size="18" /> {{ sample?.file_name ?? "教学资料" }}</h2>
        <ElTag size="small" type="info">文件预览</ElTag>
      </div>
      <p class="field-help">
        以下为后端读取的原文件预览，不代表 G3 的导入流程已经完成。
      </p>
      <pre class="document-source">{{
        sample?.content ?? "正在读取样本…"
      }}</pre>
      <ElButton
        type="primary"
        size="large"
        :loading="busy"
        :disabled="!sample"
        @click="importFile"
        >通过工作流导入 <ArrowRight :size="16"
      /></ElButton>
    </section>
    <section class="panel">
      <div class="panel-heading">
        <h2>工作流返回的资料</h2>
        <span class="counter">{{ docs.length }} 张卡片</span>
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
        <h3>等待真实导入结果</h3>
        <p>
          读取节点尚未完成时，后端会明确返回未就绪。<br />完成后，结果将直接出现在这里。
        </p>
      </div>
      <article v-for="(doc, index) in docs" :key="index" class="document-card">
        <ElTag size="small">Document {{ index + 1 }}</ElTag>
        <pre>{{ doc.page_content }}</pre>
        <div class="metadata">
          <strong>来源与版本</strong>
          <pre>{{ JSON.stringify(doc.metadata, null, 2) }}</pre>
        </div>
      </article>
    </section>
  </div>
</template>
