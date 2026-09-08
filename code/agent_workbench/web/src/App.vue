<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import {
  Boxes,
  LayoutDashboard,
  LibraryBig,
  Activity,
  Route,
  ArrowUpRight,
  Palette,
  Search,
  PanelsTopLeft,
} from "@lucide/vue";
import { getJson, type Health } from "./lib/api";
const route = useRoute();
const health = ref<Health | null>(null);
const failure = ref("");
const refreshing = ref(false);
const sections = [
  { path: "/", title: "工作台概览", icon: LayoutDashboard },
  { path: "/studio", title: "我的知识库", icon: Search },
  { path: "/documents", title: "工程文档", icon: LibraryBig },
  { path: "/incidents", title: "故障诊断", icon: Activity },
  { path: "/roadmap", title: "接下来的能力", icon: Route },
  { path: "/gallery", title: "工作模式", icon: PanelsTopLeft },
  { path: "/themes", title: "配色设置", icon: Palette },
];
const title = computed(
  () => sections.find((s) => s.path === route.path)?.title ?? "工作台",
);
async function refresh() {
  refreshing.value = true;
  try {
    health.value = await getJson<Health>("/api/health");
    failure.value = "";
  } catch {
    health.value = null;
    failure.value = "后端未连接，请先启动本地 API。";
  } finally {
    refreshing.value = false;
  }
}
onMounted(refresh);
</script>
<template>
  <RouterView v-if="route.path === '/studio'" />
  <div v-else class="workbench">
    <aside class="sidebar">
      <RouterLink to="/" class="brand"
        ><span class="brand-icon"><Boxes :size="23" /></span
        ><span
          >三玖 · Agent<span class="brand-sub">LEARNING WORKBENCH</span></span
        ></RouterLink
      >
      <div class="workspace-label">我的项目空间 <span>LOCAL</span></div>
      <nav aria-label="工作台导航">
        <RouterLink
          v-for="item in sections"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: route.path === item.path }"
          ><component :is="item.icon" :size="19" /><span>{{ item.title }}</span
          ><span v-if="route.path === item.path" class="nav-dot"></span
        ></RouterLink>
      </nav>
      <div class="sidebar-note">
        <span class="eyebrow">一条持续生长的路线</span>
        <p>学一个能力，<br />让它在这里运行。</p>
        <span>LangChain + LangGraph</span>
      </div>
      <div class="profile">
        <div class="avatar">玖</div>
        <div><strong>三玖</strong><span>构建自己的 Agent 应用</span></div>
      </div>
    </aside>
    <div class="main-shell">
      <header class="topbar">
        <div class="breadcrumb">
          项目空间 <span>/</span> <strong>{{ title }}</strong>
        </div>
        <div class="topbar-actions">
          <span class="connection" :class="{ online: health?.status === 'ok' }"
            ><i></i
            >{{ health?.status === "ok" ? "后端已连接" : "等待后端连接" }}</span
          ><ElButton text :loading="refreshing" @click="refresh"
            >刷新连接</ElButton
          ><a
            href="http://127.0.0.1:8765/docs"
            target="_blank"
            rel="noopener noreferrer"
            class="api-link"
            >API 文档 <ArrowUpRight :size="14"
          /></a>
        </div>
      </header>
      <main>
        <ElAlert
          v-if="failure"
          :title="failure"
          type="warning"
          :closable="false"
          class="connection-alert"
        /><RouterView v-slot="{ Component }"
          ><KeepAlive include="IncidentView,KnowledgeView"
            ><component :is="Component" /></KeepAlive
        ></RouterView>
      </main>
      <footer>
        同一个界面，连接每一次真实进步。<span
          >Vue · FastAPI · LangChain · LangGraph</span
        >
      </footer>
    </div>
  </div>
</template>
