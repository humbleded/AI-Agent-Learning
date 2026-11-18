import { ref } from "vue";
import { consumeEvents, getJson } from "./api";

export interface Source {
  citation_id: string;
  source_id: string;
  title: string;
  relative_path: string;
  excerpt: string;
}

export interface KnowledgeStep {
  node: string;
  label: string;
  query?: string;
}

export interface KnowledgeStatus {
  available: boolean;
  candidate_count?: number;
  file_count: number;
  scopes?: string[];
  skipped_count?: number;
  limits?: {
    max_searches?: number;
    results_per_search?: number;
    max_question_chars?: number;
    max_file_bytes?: number;
  };
}

export interface KnowledgeIndexStats {
  candidate_count: number;
  read_count: number;
  read_failed_count: number;
  empty_count: number;
  indexed_file_count: number;
  chunk_count: number;
  skipped_count: number;
}

export interface KnowledgeResult {
  answer: string;
  sources: Source[];
  refused: boolean;
  search_count: number;
  reason_code?: "NO_READABLE_DOCUMENTS" | "INSUFFICIENT_EVIDENCE" | "INVALID_CITATIONS" | null;
  next_step?: string;
}

export interface SourceDetail {
  source_id?: string;
  title: string;
  relative_path: string;
  content: string;
}

// Layout changes share this single browser session; nothing is persisted to storage.
const question = ref("");
const submittedQuestion = ref("");
const running = ref(false);
const error = ref("");
const errorNextStep = ref("");
const status = ref<KnowledgeStatus | null>(null);
const statusError = ref("");
const result = ref<KnowledgeResult | null>(null);
const indexStats = ref<KnowledgeIndexStats | null>(null);
const sources = ref<Source[]>([]);
const steps = ref<KnowledgeStep[]>([]);
const selectedSource = ref<Source | null>(null);
const sourceDetail = ref<SourceDetail | null>(null);
const sourceLoading = ref(false);
const sourceError = ref("");
let sourceRequestId = 0;
let statusRequestId = 0;

function messageFor(cause: unknown, fallback: string): string {
  return cause instanceof Error && cause.message ? cause.message : fallback;
}

function clearSource() {
  // Invalidate in-flight reads when a question or session replaces their source list.
  sourceRequestId += 1;
  selectedSource.value = null;
  sourceDetail.value = null;
  sourceLoading.value = false;
  sourceError.value = "";
}

function clearAnswer() {
  submittedQuestion.value = "";
  error.value = "";
  errorNextStep.value = "";
  result.value = null;
  indexStats.value = null;
  sources.value = [];
  steps.value = [];
  clearSource();
}

async function refreshStatus() {
  const requestId = ++statusRequestId;
  statusError.value = "";
  try {
    const nextStatus = await getJson<KnowledgeStatus>("/api/knowledge/status");
    if (requestId === statusRequestId) status.value = nextStatus;
  } catch (cause) {
    if (requestId !== statusRequestId) return;
    status.value = null;
    statusError.value = messageFor(cause, "暂时无法读取知识库状态，请重试。");
  }
}

async function ask() {
  const input = question.value.trim();
  if (running.value || !input) return;

  running.value = true;
  clearAnswer();
  question.value = input;
  submittedQuestion.value = input;
  let terminal = false;
  try {
    const response = await fetch("/api/knowledge/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: input }),
    });
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      errorNextStep.value = data.error?.next_step || "检查页面提示和后端连接后，再提交问题。";
      throw new Error(data.error?.message || "无法启动本次知识库查询。");
    }
    await consumeEvents(response, (event, data) => {
      if (terminal) return;
      if (event === "step") {
        const update = data as KnowledgeStep;
        steps.value.push({ node: update.node, label: update.label });
      } else if (event === "index") {
        indexStats.value = data as KnowledgeIndexStats;
        const stats = indexStats.value;
        steps.value.push({
          node: "index",
          label: `读取成功 ${stats.read_count} 份，读取失败 ${stats.read_failed_count} 份；本次 ${stats.indexed_file_count} 份资料、${stats.chunk_count} 个片段进入检索。`,
        });
      } else if (event === "retrieval") {
        const update = data as {
          query: string;
          search_count: number;
          sources: Source[];
        };
        steps.value.push({
          node: "search",
          label: `第 ${update.search_count} 次检索 · 找到 ${update.sources.length} 个片段`,
          query: update.query,
        });
        for (const source of update.sources) {
          const index = sources.value.findIndex(
            (existing) => existing.citation_id === source.citation_id,
          );
          if (index < 0) sources.value.push(source);
          else sources.value[index] = source;
        }
      } else if (event === "final") {
        result.value = data as KnowledgeResult;
        sources.value = result.value.sources;
        terminal = true;
        // Keep an open original only if it still belongs to the final citations.
        if (selectedSource.value) {
          const selectedId = selectedSource.value.source_id;
          const selectedCitation = selectedSource.value.citation_id;
          const finalSource = sources.value.find(
            (source) => source.source_id === selectedId && source.citation_id === selectedCitation,
          );
          if (finalSource) selectedSource.value = finalSource;
          else clearSource();
        }
      } else if (event === "error") {
        const failure = data as { message?: string; next_step?: string };
        error.value =
          failure.message || "本次查询未能完成，请重试。";
        errorNextStep.value = failure.next_step || "检查页面提示和后端连接后，再提交问题。";
        terminal = true;
      }
    });
    if (!terminal)
      throw new Error(
        "连接已结束，但没有收到最终答案。已找到的片段仍可查看，请稍后重试。",
      );
  } catch (cause) {
    // A complete final/error event remains authoritative if closing the stream fails.
    if (!terminal) {
      error.value = messageFor(cause, "知识库查询连接失败，请稍后重试。");
      if (!errorNextStep.value)
        errorNextStep.value = "先查看已收到的片段，确认后端连接恢复后重新提交；本次查询不会自动重试。";
    }
  } finally {
    running.value = false;
  }
}

async function selectSource(source: Source) {
  if (
    selectedSource.value?.source_id === source.source_id &&
    (sourceLoading.value || sourceDetail.value)
  ) {
    selectedSource.value = source;
    return;
  }

  const requestId = ++sourceRequestId;
  selectedSource.value = source;
  sourceDetail.value = null;
  sourceError.value = "";
  sourceLoading.value = true;
  try {
    const detail = await getJson<SourceDetail>(
      `/api/knowledge/source/${encodeURIComponent(source.source_id)}`,
    );
    if (requestId === sourceRequestId) sourceDetail.value = detail;
  } catch (cause) {
    if (requestId === sourceRequestId)
      sourceError.value = messageFor(cause, "暂时无法读取这份原文，请重试。");
  } finally {
    if (requestId === sourceRequestId) sourceLoading.value = false;
  }
}

function newSession() {
  if (running.value) return;
  question.value = "";
  clearAnswer();
}

export function useKnowledgeSession() {
  return {
    question,
    submittedQuestion,
    running,
    error,
    errorNextStep,
    status,
    statusError,
    result,
    indexStats,
    sources,
    steps,
    selectedSource,
    sourceDetail,
    sourceLoading,
    sourceError,
    refreshStatus,
    ask,
    selectSource,
    newSession,
  };
}
