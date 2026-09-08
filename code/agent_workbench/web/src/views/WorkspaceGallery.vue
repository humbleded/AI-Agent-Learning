<script setup lang="ts">
import { ArrowRight, ArrowUpRight, BookOpen, GitBranch, Layers3, LayoutPanelLeft, Search, Sparkles } from "@lucide/vue";
import "../prototypes.css";
import { computed } from "vue";
import { preferredMode, WORKSPACE_MODES } from "../lib/workspaceMode";
const lastModeName = computed(() => WORKSPACE_MODES.find((mode) => mode.id === preferredMode.value)?.title);
const layouts = [
  { id: "cockpit", number: "01", name: "任务指挥台", en: "TASK COCKPIT", icon: LayoutPanelLeft, description: "围绕一件事展开：提出任务、跟随执行、查看答案。资料需要时再展开。", tags: ["任务为中心", "侧边资料抽屉", "执行过程可见"], fit: "我想快速完成一次查询。" },
  { id: "research", number: "02", name: "知识研究工作室", en: "RESEARCH STUDIO", icon: BookOpen, description: "资料、回答、原文同时打开。边提问边核对出处，不在多个弹窗之间来回。", tags: ["三栏对照", "资料筛选", "原文 / 片段切换"], fit: "我想深入阅读并核对结论。" },
  { id: "canvas", number: "03", name: "可视流程画布", en: "WORKFLOW CANVAS", icon: GitBranch, description: "把本次查询铺成可探索的流程。拖动节点、缩放画布，点开每一步的真实结果。", tags: ["拖拽 / 缩放", "节点检查器", "事件与结果联动"], fit: "我想看懂 Agent 是怎样运行的。" },
] as const;
</script>

<template>
  <div class="workspace-gallery">
    <div class="wg-heading"><span class="wg-eyebrow"><Layers3 :size="14" /> WORKSPACE MODES</span><h1>一个工作空间，<br /><em>三种随时切换的模式。</em></h1><p>三种模式全部保留。专注任务、对照原文或查看执行流程，按你眼前的需要自由切换。</p><div class="wg-disclosure"><span></span>全部已启用 · 三种模式共享当前问题、答案和资料</div></div>
    <div class="wg-layouts">
      <article v-for="layout in layouts" :key="layout.id" class="wg-card">
        <RouterLink :to="`/studio?layout=${layout.id}`" class="wg-preview" :class="`wg-${layout.id}`" :aria-label="`进入${layout.name}`">
          <div class="wg-mini-top"><span><component :is="layout.icon" :size="11" /> SANJIU STUDIO</span><i></i></div>
          <div v-if="layout.id === 'cockpit'" class="wg-cockpit-body"><div class="wg-mini-tasks"><span class="wg-mini-add">＋ 新建任务</span><b>当前任务</b><i></i><i></i></div><div class="wg-mini-chat"><Sparkles :size="21" /><strong>今天，想解决什么？</strong><div class="wg-mini-message"><i></i><i></i><i></i></div><div class="wg-mini-input">描述一个问题 <ArrowUpRight :size="9" /></div></div><div class="wg-mini-drawer"><Search :size="12" /><b>资料</b><i></i><i></i></div></div>
          <div v-else-if="layout.id === 'research'" class="wg-research-body"><div class="wg-mini-sources"><span>找到的资料</span><div v-for="n in 3" :key="n"><BookOpen :size="10" /><i></i><i></i></div></div><div class="wg-mini-reading"><span>基于资料的回答</span><i v-for="n in 7" :key="n"></i><b>引用来源 ↗</b><div class="wg-mini-input">继续提问…</div></div><div class="wg-mini-original"><span>原文阅读</span><b>你的知识笔记</b><i v-for="n in 9" :key="n"></i></div></div>
          <div v-else class="wg-canvas-body"><div class="wg-mini-prompt"><GitBranch :size="14" /><span>提出问题</span><div></div><b>运行流程 →</b></div><div class="wg-mini-graph"><svg viewBox="0 0 220 180" aria-hidden="true"><path d="M35 47C74 47 55 97 98 97S130 44 170 44M98 97C147 97 132 145 180 145" /></svg><span class="mini-node mn-input">输入</span><span class="mini-node mn-agent">Agent</span><span class="mini-node mn-search">检索</span><span class="mini-node mn-answer">回答</span></div><div class="wg-mini-inspector"><span>节点详情</span><i></i><i></i><i></i></div></div>
          <span class="wg-preview-label">布局示意 · 点击进入工作模式</span>
        </RouterLink>
        <div class="wg-card-copy"><span class="wg-card-number">{{ layout.number }} / {{ layout.en }}</span><h2>{{ layout.name }}</h2><p>{{ layout.description }}</p><div class="wg-tags"><span v-for="tag in layout.tags" :key="tag">{{ tag }}</span></div><div class="wg-fit">{{ layout.fit }}</div><RouterLink :to="`/studio?layout=${layout.id}`" class="wg-enter">进入此模式 <ArrowRight :size="16" /></RouterLink></div>
      </article>
    </div>
    <div class="wg-bottom-note"><BookOpen :size="19" /><p><strong>切换视角，接着当前问题。</strong>顶部随时切换模式，共用同一次查询。再次从工作台进入时，会优先打开上次使用的模式；问题和资料仅保留在当前页面会话。</p><RouterLink to="/studio">继续使用{{ lastModeName }} <ArrowUpRight :size="14" /></RouterLink></div>
  </div>
</template>
