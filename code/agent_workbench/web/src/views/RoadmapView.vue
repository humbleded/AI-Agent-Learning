<script setup lang="ts">
import {
  LibraryBig,
  MessagesSquare,
  BrainCircuit,
  Plug,
  FlaskConical,
} from "@lucide/vue";
const items = [
  {
    icon: LibraryBig,
    name: "文档处理",
    where: "R6-01",
    text: "看到正文、来源和切分后的资料片段。",
    status: "当前学习",
  },
  {
    icon: MessagesSquare,
    name: "检索与有依据的回答",
    where: "R6-02 / R6-03",
    text: "知识库词面检索演示已接入；后续继续学习向量检索、质量改进与可靠引用。",
    status: "已有演示，继续学习",
  },
  {
    icon: BrainCircuit,
    name: "四类记忆与图片 / 音频",
    where: "D7-03",
    text: "管理已确认的记忆，找回图片和音频中的证据。",
    status: "随学习接入",
  },
  {
    icon: Plug,
    name: "工具与 MCP",
    where: "M9",
    text: "查看工具的参数、调用结果和授权边界。",
    status: "随学习接入",
  },
  {
    icon: FlaskConical,
    name: "评估与运行记录",
    where: "E10 / J11",
    text: "对比真实效果、成本、失败与改进。",
    status: "随学习接入",
  },
];
</script>
<template>
  <div class="page-intro">
    <div>
      <span class="eyebrow">ONE WORKBENCH, GROWING CAPABILITIES</span>
      <h1>新的能力，回到同一个工作台。</h1>
      <p>
        下面是接入安排。功能以真实实现为准，每一个模块都有自己的学习与验证证据。
      </p>
    </div>
  </div>
  <section class="roadmap-list">
    <article
      v-for="(item, index) in items"
      :key="item.name"
      class="roadmap-item"
    >
      <span class="roadmap-number">0{{ index + 1 }}</span
      ><component :is="item.icon" :size="25" />
      <div>
        <h2>{{ item.name }}</h2>
        <p>{{ item.text }}</p>
      </div>
      <span class="roadmap-task">{{ item.where }}</span
      ><ElTag :type="index === 0 ? 'warning' : 'info'" effect="plain">{{
        item.status
      }}</ElTag>
    </article>
  </section>
  <div class="quiet-note">
    统一 Vue 前端 · 统一 FastAPI 入口 · 独立业务核心和测试<br />助手完成的界面搭建，会与由你独立完成的代码和理解分别记录。
  </div>
</template>
