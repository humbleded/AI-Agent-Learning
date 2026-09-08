<script setup lang="ts">
import { onMounted, ref } from "vue";
import {
  Search,
  Sparkles,
  FileText,
  ArrowUpRight,
  X,
  BookOpen,
  Workflow,
} from "@lucide/vue";
import { consumeEvents, getJson } from "../lib/api";
import MarkdownText from "../components/MarkdownText.vue";

defineOptions({ name: "KnowledgeView" });
type KnowledgeStatus = {
  available: boolean;
  scopes: string[];
  file_count: number;
  skipped_count: number;
  limits: {
    max_searches: number;
    results_per_search: number;
    max_question_chars: number;
  };
};
type Source = {
  citation_id: string;
  source_id: string;
  title: string;
  relative_path: string;
  excerpt: string;
};
type FinalResult = {
  answer: string;
  sources: Source[];
  search_count: number;
  refused: boolean;
};
type SourceDetail = {
  source_id: string;
  title: string;
  relative_path: string;
  content: string;
};
const status = ref<KnowledgeStatus | null>(null);
const question = ref("");
const busy = ref(false);
const error = ref("");
const result = ref<FinalResult | null>(null);
const sources = ref<Source[]>([]);
const steps = ref<{ label: string; query?: string }[]>([]);
const submittedQuestion = ref("");
const sourceDialog = ref<HTMLDialogElement | null>(null);
const sourceDetail = ref<SourceDetail | null>(null);
const sourceError = ref("");
const examples = [
  "模型发出工具调用请求后，工具由谁真正执行？为什么只会 Tool Calling 还不算多步 Agent？",
  "LangGraph 第二次调用会自动接着上次的状态吗？如果要求进程重启后继续，还需要什么？",
];
async function refreshStatus() {
  try {
    status.value = await getJson<KnowledgeStatus>("/api/knowledge/status");
    error.value = "";
  } catch (e) {
    status.value = null;
    error.value = (e as Error).message;
  }
}
onMounted(refreshStatus);
async function ask() {
  if (busy.value || !question.value.trim()) return;
  busy.value = true;
  error.value = "";
  result.value = null;
  sources.value = [];
  steps.value = [];
  submittedQuestion.value = question.value.trim();
  let terminal = false;
  try {
    const response = await fetch("/api/knowledge/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: submittedQuestion.value }),
    });
    await consumeEvents(response, (event, data) => {
      if (event === "step") {
        const update = data as { label: string };
        steps.value.push({ label: update.label });
      }
      if (event === "retrieval") {
        const update = data as {
          query: string;
          search_count: number;
          sources: Source[];
        };
        steps.value.push({
          label: `第 ${update.search_count} 次检索 · 找到 ${update.sources.length} 个片段`,
          query: update.query,
        });
        for (const source of update.sources) {
          const found = sources.value.findIndex(
            (s) => s.citation_id === source.citation_id,
          );
          if (found < 0) sources.value.push(source);
          else sources.value[found] = source;
        }
      }
      if (event === "final") {
        result.value = data as FinalResult;
        sources.value = result.value.sources;
        terminal = true;
      }
      if (event === "error") {
        error.value = (data as { message: string }).message;
        terminal = true;
      }
    });
    if (!terminal)
      throw new Error(
        "连接已结束，但没有收到最终答案。已找到的片段仍可查看，请稍后重试。",
      );
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
async function openSource(source: Source) {
  sourceDetail.value = null;
  sourceError.value = "";
  sourceDialog.value?.showModal();
  try {
    sourceDetail.value = await getJson<SourceDetail>(
      `/api/knowledge/source/${encodeURIComponent(source.source_id)}`,
    );
  } catch (e) {
    sourceError.value = (e as Error).message;
  }
}
</script>

<template>
  <div class="page-intro">
    <div>
      <span class="eyebrow">YOUR KNOWLEDGE · CONNECTED</span>
      <h1>让你的积累，随问随到。</h1>
      <p>从你写过的笔记中找到答案，让每个结论都能回到原文。</p>
    </div>
    <span class="subtle-pill"><BookOpen :size="15" /> AI-Knowledge</span>
  </div>
  <div class="knowledge-status panel">
    <div>
      <span class="tiny-dot"></span
      ><strong>{{
        status?.available ? "本地知识库已连接" : "等待知识库连接"
      }}</strong
      ><span v-if="status">{{ status.file_count }} 份可检索笔记</span>
    </div>
    <ElButton text @click="refreshStatus" :disabled="busy">刷新范围</ElButton>
    <p>
      当前读取：概念、课程、论文笔记。README/index.md、个人记忆、复盘、原始收件箱及配置目录不参与检索；课程计划不代表已经掌握。
    </p>
  </div>
  <div class="knowledge-layout">
    <div class="knowledge-main">
      <section class="panel knowledge-query">
        <div class="panel-heading">
          <h2><Sparkles :size="19" /> 问问自己的知识库</h2>
          <ElTag size="small" effect="plain">Agent 检索</ElTag>
        </div>
        <label class="field-label" for="knowledge-question"
          >你想从笔记里找到什么？</label
        >
        <textarea
          id="knowledge-question"
          v-model="question"
          :disabled="busy"
          maxlength="1000"
          rows="4"
          placeholder="例如：Tool Calling 和多步 Agent 有什么区别？"
        />
        <div class="knowledge-examples">
          <button
            v-for="(example, index) in examples"
            :key="example"
            :disabled="busy"
            @click="question = example"
          >
            {{ index === 0 ? "工具调用与 Agent" : "LangGraph 如何恢复状态" }}
            <ArrowUpRight :size="13" />
          </button>
        </div>
        <p class="field-help knowledge-disclosure">
          点击后，问题与命中的少量笔记片段会发送给已配置的 DeepSeek
          生成答案。检索在本机完成，原笔记只读。
        </p>
        <div class="knowledge-submit">
          <span class="caption">最多 2 次检索 · 每次最多 4 个片段</span
          ><ElButton
            type="primary"
            size="large"
            :loading="busy"
            :disabled="!question.trim() || !status?.available"
            @click="ask"
            ><Search v-if="!busy" :size="17" />{{
              busy ? "Agent 正在查找" : "检索并回答"
            }}</ElButton
          >
        </div>
      </section>
      <ElAlert
        v-if="error"
        :title="error"
        type="error"
        :closable="false"
        show-icon
      />
      <section v-if="result" class="panel knowledge-answer" aria-live="polite">
        <span class="eyebrow">{{
          result.refused ? "需要更多资料" : "基于你的笔记"
        }}</span>
        <h2>{{ submittedQuestion }}</h2>
        <MarkdownText :content="result.answer" />
        <p class="caption">
          {{ result.search_count }} 次实际检索 ·
          引用编号对应下方片段；可打开完整原文核对。
        </p>
      </section>
      <section v-if="sources.length" class="knowledge-sources">
        <div class="section-heading">
          <h2>找到的原文片段</h2>
          <span>{{ sources.length }} 个片段</span>
        </div>
        <article
          v-for="source in sources"
          :key="source.citation_id"
          class="panel knowledge-source"
        >
          <div class="knowledge-source-heading">
            <span class="citation-pill">{{ source.citation_id }}</span>
            <h3>{{ source.title }}</h3>
            <button
              @click="openSource(source)"
              :aria-label="`查看原文：${source.title}`"
            >
              <FileText :size="15" /> 查看原文
            </button>
          </div>
          <p class="knowledge-path">{{ source.relative_path }}</p>
          <details>
            <summary>展开命中的内容</summary>
            <pre>{{ source.excerpt }}</pre>
          </details>
        </article>
      </section>
      <section
        v-if="!busy && !result && !sources.length"
        class="panel empty-state knowledge-empty"
      >
        <BookOpen :size="36" />
        <h3>你写过的笔记，现在可以为你回答。</h3>
        <p>试试上方的示例。这里会显示真实答案和资料出处。</p>
      </section>
    </div>
    <aside class="panel knowledge-process">
      <div class="panel-heading">
        <h2><Workflow :size="18" /> 看见检索过程</h2>
      </div>
      <p class="field-help">这里显示 Agent 实际选择的搜索词和找到的内容。</p>
      <ol v-if="steps.length">
        <li v-for="(step, index) in steps" :key="index">
          <span>{{ index + 1 }}</span>
          <div>
            <strong>{{ step.label }}</strong>
            <p v-if="step.query">{{ step.query }}</p>
          </div>
        </li>
      </ol>
      <div v-else class="knowledge-process-empty">
        <Search :size="26" />
        <p>提交问题后<br />在这里跟随每一步。</p>
      </div>
      <p v-if="busy" class="waiting-message">等待下一条真实执行结果…</p>
    </aside>
  </div>
  <dialog
    ref="sourceDialog"
    class="knowledge-dialog"
    @click="
      (event) => {
        if (event.target === sourceDialog) sourceDialog?.close();
      }
    "
  >
    <header>
      <div>
        <span class="eyebrow">READ ORIGINAL</span>
        <h2>{{ sourceDetail?.title ?? "查看原文" }}</h2>
      </div>
      <button @click="sourceDialog?.close()" aria-label="关闭原文">
        <X :size="21" />
      </button>
    </header>
    <p class="knowledge-path">{{ sourceDetail?.relative_path }}</p>
    <ElAlert
      v-if="sourceError"
      :title="sourceError"
      type="error"
      :closable="false"
    />
    <MarkdownText :content="sourceDetail?.content ?? (sourceError ? '' : '正在读取原文…')" />
  </dialog>
</template>

<style scoped>
.subtle-pill {
  display: inline-flex;
  gap: 8px;
  align-items: center;
}
.knowledge-status {
  padding: 18px 24px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
.knowledge-status > div {
  display: flex;
  gap: 12px;
  align-items: center;
  flex: 1;
  flex-wrap: wrap;
}
.knowledge-status > div > span:last-child {
  font-size: 12px;
  opacity: 0.65;
}
.knowledge-status > p {
  flex-basis: 100%;
  margin: 0;
  font-size: 12px;
  opacity: 0.7;
  line-height: 1.7;
}
.knowledge-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 285px;
  gap: 24px;
  align-items: start;
}
.knowledge-main {
  min-width: 0;
  display: grid;
  gap: 22px;
}
.knowledge-query textarea {
  width: 100%;
  border: 1px solid var(--el-border-color, #dce6e2);
  background: var(--el-fill-color-blank, #fff);
  color: var(--el-text-color-primary, #263c3a);
  border-radius: 12px;
  padding: 17px;
  resize: vertical;
  min-height: 110px;
  font: inherit;
  line-height: 1.7;
  outline: none;
}
.knowledge-query textarea:focus {
  border-color: var(--el-color-primary);
  box-shadow: 0 0 0 3px var(--el-color-primary-light-9);
}
.knowledge-examples {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0 17px;
}
.knowledge-examples button {
  background: transparent;
  color: inherit;
  border: 1px solid var(--el-border-color, #dce6e2);
  border-radius: 20px;
  padding: 7px 10px;
  cursor: pointer;
  font: inherit;
  font-size: 11px;
  display: flex;
  align-items: center;
  gap: 5px;
}
.knowledge-examples button:hover {
  border-color: var(--el-color-primary);
}
.knowledge-disclosure {
  line-height: 1.8;
}
.knowledge-submit {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
}
.knowledge-answer h2 {
  font-size: 20px;
  line-height: 1.5;
  margin: 13px 0 20px;
}
.knowledge-answer-text {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  font-size: 14px;
  line-height: 1.95;
}
.knowledge-answer .caption {
  margin-top: 22px;
  margin-bottom: 0;
}
.knowledge-source {
  padding: 20px;
  margin-bottom: 12px;
}
.knowledge-source-heading {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.knowledge-source-heading h3 {
  font-size: 14px;
  flex: 1;
  margin: 0;
  min-width: 100px;
}
.knowledge-source-heading button {
  border: 0;
  background: transparent;
  color: var(--el-color-primary);
  font: inherit;
  font-size: 12px;
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px;
}
.citation-pill {
  padding: 5px 8px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  font-size: 11px;
  border-radius: 6px;
  font-weight: 700;
}
.knowledge-path {
  font-size: 11px;
  opacity: 0.65;
  margin: 12px 0;
  word-break: break-all;
  line-height: 1.8;
}
.knowledge-source summary {
  font-size: 12px;
  cursor: pointer;
  opacity: 0.8;
}
.knowledge-source pre {
  margin-bottom: 0;
  max-height: 350px;
  overflow: auto;
}
.knowledge-process {
  padding: 23px;
  position: sticky;
  top: 24px;
}
.knowledge-process ol {
  list-style: none;
  padding: 0;
  margin: 25px 0 0;
}
.knowledge-process li {
  display: flex;
  gap: 12px;
  padding-bottom: 22px;
  font-size: 12px;
  line-height: 1.65;
}
.knowledge-process li > span {
  width: 23px;
  height: 23px;
  border: 1px solid var(--el-border-color, #dce6e2);
  border-radius: 50%;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  font-size: 10px;
}
.knowledge-process li p {
  margin: 5px 0 0;
  opacity: 0.65;
  overflow-wrap: anywhere;
}
.knowledge-process-empty {
  display: grid;
  justify-items: center;
  opacity: 0.55;
  padding: 42px 0;
  text-align: center;
  line-height: 1.8;
  font-size: 12px;
}
.knowledge-process-empty p {
  margin-top: 15px;
}
.knowledge-empty {
  padding: 48px 20px;
}
.knowledge-dialog {
  width: min(850px, 92vw);
  max-height: 85vh;
  border: 1px solid var(--el-border-color, #dce6e2);
  border-radius: 18px;
  padding: 26px;
  color: var(--el-text-color-primary, #263c3a);
  background: var(--el-bg-color, #fff);
  box-shadow: 0 25px 100px #0005;
}
.knowledge-dialog::backdrop {
  background: #080e22aa;
  backdrop-filter: blur(8px);
}
.knowledge-dialog header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}
.knowledge-dialog h2 {
  font-size: 21px;
  margin: 10px 0;
}
.knowledge-dialog header button {
  background: transparent;
  border: 0;
  color: inherit;
  padding: 8px;
  cursor: pointer;
}
.knowledge-dialog pre {
  font-size: 13px;
  line-height: 1.9;
}
@media (max-width: 1200px) {
  .knowledge-layout {
    grid-template-columns: minmax(0, 1fr);
  }
  .knowledge-process {
    position: static;
  }
}
@media (max-width: 600px) {
  .knowledge-status {
    padding: 16px;
  }
  .knowledge-submit > .caption {
    font-size: 10px;
  }
  .knowledge-dialog {
    padding: 18px;
  }
}
</style>
