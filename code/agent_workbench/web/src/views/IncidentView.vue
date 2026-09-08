<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import {
  Play,
  Activity,
  CircleCheck,
  FileText,
  ChevronDown,
  Workflow,
} from "@lucide/vue";
import { consumeEvents, getJson, type Preset } from "../lib/api";
// 切换模块时保留正在接收的运行和结果；刷新整个页面才重新开始。
defineOptions({ name: "IncidentView" });
type Update = { node: string; data: unknown; received: string };
type FinalResult = {
  conclusion?: string | null;
  stop_reason?: string | null;
  evidence?: string[];
  step_count?: number;
};
const presets = ref<Preset[]>([]);
const selected = ref("normal");
const current = computed(() =>
  presets.value.find((p) => p.id === selected.value),
);
const updates = ref<Update[]>([]);
const result = ref<FinalResult | null>(null);
const busy = ref(false);
const error = ref("");
const nodeNames: Record<string, string> = {
  organize_facts: "整理告警与日志",
  review_evidence: "核对现有证据",
  run_readonly_diagnostic: "执行只读诊断工具",
  build_conclusion: "生成诊断结论",
  evidence_insufficient_stop: "资料不足，停止判断",
  max_steps_stop: "达到步骤上限，停止执行",
  tool_failure_stop: "工具失败，停止执行",
};
const stopNames: Record<string, string> = {
  evidence_insufficient: "现有证据不足，工作流已停止",
  max_steps_reached: "达到步骤上限，工作流已停止",
  tool_failure: "诊断工具失败，工作流已停止",
};
onMounted(async () => {
  try {
    presets.value = (
      await getJson<{ presets: Preset[] }>("/api/incidents/presets")
    ).presets;
  } catch (e) {
    error.value = (e as Error).message;
  }
});
async function run() {
  if (busy.value) return;
  busy.value = true;
  updates.value = [];
  result.value = null;
  error.value = "";
  let terminalEvent = false;
  try {
    const response = await fetch("/api/incidents/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ preset_id: selected.value }),
    });
    await consumeEvents(response, (event, data) => {
      if (event === "graph_update") {
        const part = data as { data?: Record<string, unknown> };
        for (const [node, update] of Object.entries(part.data ?? {}))
          updates.value.push({
            node,
            data: update,
            received: new Date().toLocaleTimeString("zh-CN", { hour12: false }),
          });
      }
      if (event === "final") {
        result.value = data as FinalResult;
        terminalEvent = true;
      }
      if (event === "error") {
        const failure = data as { message?: string };
        error.value = failure.message ?? "后端执行失败";
        terminalEvent = true;
      }
    });
    if (!terminalEvent)
      throw new Error("连接已结束，但没有收到最终结果。请检查后端再重试。");
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
</script>
<template>
  <div class="page-intro">
    <div>
      <span class="eyebrow">INCIDENT REVIEW</span>
      <h1>看见一次诊断的全过程。</h1>
      <p>真实调用已有工作流；只有后端返回一步，时间线才会增加一步。</p>
    </div>
    <span class="subtle-pill">已完成的 G8-00 核心</span>
  </div>
  <div class="execution-grid">
    <section class="panel input-panel">
      <div class="panel-heading">
        <h2><FileText :size="18" /> 输入场景</h2>
        <ElTag size="small" type="info">虚构教学数据</ElTag>
      </div>
      <label class="field-label" for="preset-choice">选择要观察的行为</label
      ><ElSelect
        id="preset-choice"
        v-model="selected"
        :disabled="busy"
        class="full-width"
        aria-label="选择诊断场景"
        ><ElOption
          v-for="p in presets"
          :key="p.id"
          :label="p.title"
          :value="p.id"
      /></ElSelect>
      <p class="field-help">{{ current?.description }}</p>
      <div class="model-hint">
        <span class="tiny-dot"></span
        >{{
          current?.uses_model
            ? "此场景会真实调用 DeepSeek 生成结论"
            : "此场景观察规则分支，不调用模型"
        }}
      </div>
      <details class="input-details" open>
        <summary>查看发给工作流的输入 <ChevronDown :size="15" /></summary>
        <pre>{{ JSON.stringify(current?.input ?? {}, null, 2) }}</pre>
      </details>
      <ElButton
        type="primary"
        size="large"
        class="full-width run-button"
        :loading="busy"
        :disabled="!current"
        @click="run"
        ><Play v-if="!busy" :size="16" />{{
          busy ? "工作流正在运行" : "运行诊断"
        }}</ElButton
      >
      <p class="caption">当前执行只读诊断，不修改服务配置。</p>
    </section>
    <section class="panel timeline-panel">
      <div class="panel-heading">
        <h2><Activity :size="19" /> 运行过程</h2>
        <span class="counter">{{ updates.length }} 个已收到的步骤</span>
      </div>
      <div v-if="!updates.length && !busy" class="empty-state">
        <Workflow :size="38" />
        <h3>从左侧启动一次诊断</h3>
        <p>这里将显示真实节点更新和最后的结果。</p>
      </div>
      <div v-if="busy && !updates.length" class="waiting-message">
        请求已发出，等待后端返回第一步…
      </div>
      <ol v-if="updates.length" class="timeline">
        <li v-for="(item, index) in updates" :key="index">
          <span class="timeline-mark"><CircleCheck :size="17" /></span>
          <div class="timeline-content">
            <div class="timeline-title">
              <strong>{{ nodeNames[item.node] ?? item.node }}</strong
              ><time>{{ item.received }}</time>
            </div>
            <details>
              <summary>{{ item.node }} <ChevronDown :size="13" /></summary>
              <pre>{{ JSON.stringify(item.data, null, 2) }}</pre>
            </details>
          </div>
        </li>
      </ol>
      <div v-if="busy && updates.length" class="waiting-message">
        继续等待后端结果；模型生成时可能需要稍候…
      </div>
      <ElAlert
        v-if="error"
        :title="error"
        type="error"
        :closable="false"
        show-icon
      />
      <div v-if="result" class="result-card">
        <span class="eyebrow">工作流最终返回</span>
        <h3>
          {{
            result.stop_reason
              ? (stopNames[result.stop_reason] ?? result.stop_reason)
              : "诊断结论已生成"
          }}
        </h3>
        <p v-if="result.conclusion" class="conclusion">
          {{ result.conclusion }}
        </p>
        <p v-else class="field-help">
          本次没有生成模型结论，请结合上方停止原因查看过程。
        </p>
        <div v-if="result.evidence?.length" class="evidence">
          <strong>本次收集的依据</strong>
          <ul>
            <li v-for="(item, i) in result.evidence" :key="i">{{ item }}</li>
          </ul>
        </div>
      </div>
    </section>
  </div>
</template>
