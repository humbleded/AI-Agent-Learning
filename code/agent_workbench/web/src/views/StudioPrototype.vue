<script setup lang="ts">
import { computed, defineComponent, h, nextTick, onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Check,
  ChevronDown,
  FileText,
  GitBranch,
  LayoutPanelLeft,
  LoaderCircle,
  Maximize2,
  MessageSquare,
  Minus,
  PanelRightClose,
  PanelRightOpen,
  Plus,
  RefreshCw,
  Search,
  Send,
  Sparkles,
  X,
  ZoomIn
} from '@lucide/vue'
import { useKnowledgeSession, type Source } from '../lib/knowledgeSession'
import MarkdownText from '../components/MarkdownText.vue'
import { parseWorkspaceMode, preferredMode } from '../lib/workspaceMode'
import '../prototypes.css'

const route = useRoute()
const layouts = [
  { id: 'cockpit', title: '任务指挥台', icon: LayoutPanelLeft },
  { id: 'research', title: '知识研究工作室', icon: BookOpen },
  { id: 'canvas', title: '可视流程画布', icon: GitBranch }
] as const
const layout = computed(() => parseWorkspaceMode(route.query.layout) ?? preferredMode.value)
const layoutTitle = computed(() => layouts.find(item => item.id === layout.value)?.title)
const {
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
  newSession
} = useKnowledgeSession()
const candidateCount = computed(() => status.value?.candidate_count ?? status.value?.file_count ?? 0)
const scopeLabels: Record<string, string> = { '02-Concepts': '概念笔记', '03-Courses': '课程资料', '05-Papers': '论文资料' }
const scopeDescription = computed(
  () => status.value?.scopes?.map(scope => scopeLabels[scope] ?? scope).join('、') || '等待后端返回读取范围'
)
const resultTitle = computed(() => {
  if (!result.value) return '最终答案'
  if (!result.value.refused) return '基于你的笔记'
  switch (result.value.reason_code) {
    case 'NO_READABLE_DOCUMENTS':
      return '本次没有可用于检索的资料'
    case 'INSUFFICIENT_EVIDENCE':
      return '本次资料不足以回答'
    case 'INVALID_CITATIONS':
      return '回答引用未通过检查'
    default:
      return '本次未能作答'
  }
})
const exampleQuestions = [
  { title: '工具有结果，流程没继续', question: '工具已经返回了结果，Agent 为什么没有继续回答？我该检查工具结果怎样回填给模型？' },
  { title: '工具失败，该重试还是停止', question: 'Agent 调用工具失败时，哪些情况适合重试，哪些情况应该停止？怎样避免一直重试？' },
  { title: '进程重启，如何恢复任务', question: 'LangGraph 任务运行到一半进程重启了，怎样恢复之前的执行？需要保存什么？' }
]
const ExampleQuestions = defineComponent({
  name: 'StudioExampleQuestions',
  setup: () => () =>
    h(
      'div',
      { class: 'studio-example-questions', 'aria-label': '按任务选择示例问题' },
      exampleQuestions.map(example =>
        h(
          'button',
          {
            type: 'button',
            disabled: running.value,
            title: example.question,
            onClick: () => {
              question.value = example.question
            }
          },
          [example.title, h(ArrowRight, { size: 12 })]
        )
      )
    )
})
const drawerOpen = ref(true)
const readerTab = ref<'excerpt' | 'full'>('excerpt')
const drawerTab = ref<'sources' | 'reader'>('sources')
const sourceFilter = ref('')
const filteredSources = computed(() => {
  const filter = sourceFilter.value.trim().toLocaleLowerCase()
  return sources.value.filter(item => `${item.title} ${item.relative_path} ${item.excerpt}`.toLocaleLowerCase().includes(filter))
})
onMounted(() => {
  refreshStatus()
  if (layout.value === 'canvas') nextTick(fitCanvas)
})
watch(layout, next => {
  sourceFilter.value = ''
  if (next === 'canvas') nextTick(fitCanvas)
})

function openSource(source: Source) {
  selectSource(source)
  drawerTab.value = 'reader'
  readerTab.value = 'excerpt'
  drawerOpen.value = true
}
function startFresh() {
  if (running.value) return
  newSession()
  sourceFilter.value = ''
  drawerTab.value = 'sources'
}
function submitQuestion() {
  if (status.value?.available && !running.value) ask()
}

const SourceCards = defineComponent({
  name: 'StudioSources',
  setup: () => () =>
    h(
      'div',
      { class: 'studio-source-cards' },
      sources.value.length
        ? filteredSources.value.length
          ? filteredSources.value.map(source =>
              h(
                'button',
                {
                  type: 'button',
                  class: ['studio-source-card', { selected: selectedSource.value?.citation_id === source.citation_id }],
                  onClick: () => openSource(source),
                  'aria-pressed': selectedSource.value?.citation_id === source.citation_id
                },
                [
                  h('span', { class: 'studio-citation' }, source.citation_id),
                  h('strong', source.title),
                  h('small', source.relative_path),
                  h('p', source.excerpt)
                ]
              )
            )
          : h('p', { class: 'studio-small-empty' }, '没有匹配的片段，试试别的筛选词。')
        : h('div', { class: 'studio-small-empty' }, [
            h(BookOpen, { size: 27 }),
            h('strong', '资料将从这里出现'),
            h('p', '提交问题后，显示这次真实检索命中的笔记。')
          ])
    )
})

const QueryComposer = defineComponent({
  name: 'StudioQueryComposer',
  setup: () => () =>
    h(
      'form',
      {
        class: 'studio-composer',
        onSubmit: (event: Event) => {
          event.preventDefault()
          submitQuestion()
        }
      },
      [
        h('label', { for: 'studio-question' }, layout.value === 'canvas' ? '给流程一个问题' : '你想从笔记中找到什么？'),
        h('textarea', {
          id: 'studio-question',
          value: question.value,
          disabled: running.value,
          maxlength: status.value?.limits?.max_question_chars ?? 1000,
          rows: layout.value === 'canvas' ? 6 : 3,
          placeholder: '例如：Tool Calling 与多步 Agent 有什么区别？',
          onInput: (event: Event) => {
            question.value = (event.target as HTMLTextAreaElement).value
          },
          onKeydown: (event: KeyboardEvent) => {
            if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
              event.preventDefault()
              submitQuestion()
            }
          }
        }),
        h('div', { class: 'studio-composer-actions' }, [
          h('span', 'Ctrl / ⌘ + Enter'),
          h(
            'button',
            { class: 'studio-run', type: 'submit', disabled: running.value || !question.value.trim() || !status.value?.available },
            [
              h(running.value ? LoaderCircle : Send, { size: 15, class: running.value ? 'studio-spin' : '' }),
              running.value ? '正在查询' : '检索并回答'
            ]
          )
        ]),
        h('p', { class: 'studio-data-note' }, '问题与命中的少量片段发送给 DeepSeek；检索在本机完成，原笔记只读。')
      ]
    )
})

const Reader = defineComponent({
  name: 'StudioSourceReader',
  setup: () => () =>
    h(
      'div',
      { class: 'studio-reader-content' },
      selectedSource.value
        ? [
            h('div', { class: 'studio-reader-meta' }, [
              h('span', { class: 'studio-citation' }, selectedSource.value.citation_id),
              h('h3', selectedSource.value.title),
              h('p', selectedSource.value.relative_path)
            ]),
            h('div', { class: 'studio-tabs', role: 'group', 'aria-label': '原文显示范围' }, [
              h(
                'button',
                {
                  class: { selected: readerTab.value === 'excerpt' },
                  'aria-pressed': readerTab.value === 'excerpt',
                  onClick: () => {
                    readerTab.value = 'excerpt'
                  }
                },
                '命中片段'
              ),
              h(
                'button',
                {
                  class: { selected: readerTab.value === 'full' },
                  'aria-pressed': readerTab.value === 'full',
                  onClick: () => {
                    readerTab.value = 'full'
                  }
                },
                '完整原文'
              )
            ]),
            readerTab.value === 'excerpt'
              ? h('pre', { class: 'studio-source-text' }, selectedSource.value.excerpt)
              : sourceLoading.value
                ? h('p', { class: 'studio-reader-loading' }, '正在读取完整原文…')
                : sourceError.value
                  ? h('div', { class: 'studio-error', role: 'alert' }, [
                      h('p', sourceError.value),
                      h('button', { onClick: () => selectedSource.value && selectSource(selectedSource.value) }, '重新读取')
                    ])
                  : h(MarkdownText, { class: 'studio-original-markdown', content: sourceDetail.value?.content ?? '尚未收到原文。' })
          ]
        : h('div', { class: 'studio-small-empty' }, [
            h(FileText, { size: 29 }),
            h('strong', '给每个结论，留一个出处'),
            h('p', '选择一个检索片段，在这里查看命中内容或完整原文。')
          ])
    )
})

type NodeId = 'input' | 'agent' | 'search' | 'answer' | 'citation'
const initialNodes: { id: NodeId; name: string; subtitle: string; x: number; y: number }[] = [
  { id: 'input', name: '输入', subtitle: '你的问题', x: 45, y: 215 },
  { id: 'agent', name: 'Agent', subtitle: '决定搜索词', x: 250, y: 105 },
  { id: 'search', name: '检索', subtitle: '本地知识库', x: 458, y: 230 },
  { id: 'answer', name: '回答', subtitle: '基于资料生成', x: 670, y: 105 },
  { id: 'citation', name: '引用', subtitle: '返回资料出处', x: 690, y: 380 }
]
const nodes = reactive(initialNodes.map(node => ({ ...node })))
const nodeIcons = { input: MessageSquare, agent: Sparkles, search: Search, answer: FileText, citation: BookOpen }
const selectedNodeId = ref<NodeId>('input')
const selectedNode = computed(() => nodes.find(node => node.id === selectedNodeId.value)!)
const nodeEvents = computed(() =>
  steps.value.filter(step => (selectedNodeId.value === 'input' ? step.node === 'index' : step.node === selectedNodeId.value))
)
const zoom = ref(0.85)
const viewport = ref<HTMLDivElement | null>(null)
const edges = computed(() =>
  (
    [
      ['input', 'agent'],
      ['agent', 'search'],
      ['search', 'answer'],
      ['answer', 'citation']
    ] as [NodeId, NodeId][]
  ).map(([from, to]) => {
    const a = nodes.find(node => node.id === from)!
    const b = nodes.find(node => node.id === to)!
    const x1 = a.x + 170,
      y1 = a.y + 52,
      x2 = b.x,
      y2 = b.y + 52
    return { id: `${from}-${to}`, path: `M${x1} ${y1} C${x1 + 65} ${y1} ${x2 - 65} ${y2} ${x2} ${y2}` }
  })
)
function nodeState(id: NodeId): string {
  if (id === 'input') return submittedQuestion.value ? '已提交问题' : '等待输入'
  if (id === 'agent') {
    const count = steps.value.filter(step => step.node === 'agent').length
    return count ? `收到 ${count} 次更新` : '等待 Agent 更新'
  }
  if (id === 'search') {
    const count = steps.value.filter(step => step.node === 'search').length
    return count ? `${count} 次检索已返回` : '等待检索结果'
  }
  if (id === 'answer') return result.value ? (result.value.refused ? '返回无法作答原因' : '答案已返回') : '等待最终答案'
  return result.value ? (result.value.sources.length ? `${result.value.sources.length} 个出处` : '本次无可用引用') : '等待回答出处'
}
function nodeHasEvidence(id: NodeId) {
  return id === 'input'
    ? !!submittedQuestion.value
    : id === 'answer' || id === 'citation'
      ? !!result.value
      : steps.value.some(step => step.node === id)
}
let drag: { id: NodeId; pointer: number; startX: number; startY: number; x: number; y: number } | null = null
function dragStart(event: PointerEvent, id: NodeId) {
  if (event.button !== 0) return
  selectedNodeId.value = id
  const node = nodes.find(item => item.id === id)!
  drag = { id, pointer: event.pointerId, startX: event.clientX, startY: event.clientY, x: node.x, y: node.y }
  ;(event.currentTarget as HTMLElement).setPointerCapture(event.pointerId)
}
function dragMove(event: PointerEvent) {
  if (!drag || drag.pointer !== event.pointerId) return
  const node = nodes.find(item => item.id === drag!.id)!
  node.x = Math.min(800, Math.max(12, drag.x + (event.clientX - drag.startX) / zoom.value))
  node.y = Math.min(490, Math.max(15, drag.y + (event.clientY - drag.startY) / zoom.value))
}
function keyMove(event: KeyboardEvent, id: NodeId) {
  const amount = event.shiftKey ? 30 : 10
  const moves: Record<string, [number, number]> = {
    ArrowLeft: [-amount, 0],
    ArrowRight: [amount, 0],
    ArrowUp: [0, -amount],
    ArrowDown: [0, amount]
  }
  const delta = moves[event.key]
  if (!delta) return
  event.preventDefault()
  const node = nodes.find(item => item.id === id)!
  node.x = Math.max(12, Math.min(800, node.x + delta[0]))
  node.y = Math.max(15, Math.min(490, node.y + delta[1]))
}
function changeZoom(delta: number) {
  zoom.value = Math.min(1.4, Math.max(0.4, Math.round((zoom.value + delta) * 100) / 100))
}
function fitCanvas() {
  zoom.value = Math.max(0.4, Math.min(1, ((viewport.value?.clientWidth ?? 900) - 30) / 1000))
}
function resetCanvas() {
  initialNodes.forEach((node, index) => Object.assign(nodes[index]!, node))
  fitCanvas()
  viewport.value?.scrollTo(0, 0)
}
</script>

<template>
  <div class="studio-shell" :class="`studio-${layout}`">
    <header class="studio-topbar">
      <RouterLink to="/gallery" class="studio-back"><ArrowLeft :size="16" /><span>工作模式</span></RouterLink>
      <div class="studio-wordmark">
        <span><Sparkles :size="17" /></span><strong>三玖 <i>/</i> Studio</strong>
      </div>
      <nav class="studio-layout-switch" aria-label="切换工作模式">
        <RouterLink v-for="item in layouts" :key="item.id" :to="`/studio?layout=${item.id}`" :class="{ selected: layout === item.id }"
          ><component :is="item.icon" :size="14" /><span>{{ item.title }}</span></RouterLink
        >
      </nav>
      <span class="studio-prototype-label">三种模式已启用</span><RouterLink to="/" class="studio-home">返回工作台</RouterLink>
    </header>
    <div class="studio-context">
      <div>
        <span :class="['studio-connection-dot', { connected: status?.available }]"></span
        ><strong>{{
          status?.available ? '已扫描到候选笔记' : status ? '未扫描到候选笔记' : statusError ? '知识库状态读取失败' : '正在读取知识库状态'
        }}</strong
        ><span v-if="status">{{ candidateCount }} 份候选笔记 · 查询时验证读取</span
        ><button @click="refreshStatus" :disabled="running" aria-label="刷新知识库状态"><RefreshCw :size="12" /></button>
      </div>
      <span>同一次查询 · 切换模式保留结果</span>
    </div>
    <p v-if="statusError" class="studio-status-error" role="alert">{{ statusError }}</p>
    <div class="studio-scope-note">
      <span :title="status?.scopes?.join('、')">只读范围：{{ scopeDescription }}</span
      ><span>个人记忆不在范围内</span>
    </div>
    <details v-if="indexStats" class="studio-index-status" :open="indexStats.read_failed_count > 0">
      <summary>
        本次资料准备：{{ indexStats.indexed_file_count }} 份资料、{{ indexStats.chunk_count }} 个片段进入检索<span
          v-if="indexStats.read_failed_count"
        >
          · {{ indexStats.read_failed_count }} 份读取失败</span
        >
      </summary>
      <p>
        候选 {{ indexStats.candidate_count }} 份 · 读取成功 {{ indexStats.read_count }} 份 · 读取失败 {{ indexStats.read_failed_count }} 份
        · 空内容 {{ indexStats.empty_count }} 份 · 按读取规则排除 {{ indexStats.skipped_count }} 项
      </p>
      <p v-if="indexStats.read_failed_count">读取失败的文件没有参与本次检索。可以检查文件是否可读，再重新查询。</p>
    </details>

    <div class="studio-layout" :class="{ 'drawer-closed': layout === 'cockpit' && !drawerOpen }">
      <aside v-if="layout === 'cockpit'" class="studio-task-rail">
        <div class="studio-rail-label">工作空间 <span>01</span></div>
        <button class="studio-new" :disabled="running" @click="startFresh"><Plus :size="17" />新建任务</button>
        <div class="studio-task-section">本次任务</div>
        <button v-if="submittedQuestion" class="studio-current-task">
          <MessageSquare :size="15" /><span>{{ submittedQuestion }}</span
          ><i :class="{ running }"></i>
        </button>
        <div v-else class="studio-task-empty">还没有任务。<br />从右侧提出第一个问题。</div>
        <div class="studio-rail-bottom">
          <BookOpen :size="20" /><strong>用已有知识，解决眼前的问题。</strong>
          <p>当前任务在三种模式间共享，刷新页面后清空。</p>
        </div>
      </aside>

      <aside v-if="layout === 'research'" class="studio-research-sources">
        <div class="studio-pane-title">
          <h2><Search :size="16" />检索资料</h2>
          <span>{{ sources.length }}</span>
        </div>
        <label class="studio-source-filter"
          ><Search :size="13" /><input v-model="sourceFilter" placeholder="筛选本次片段" aria-label="筛选本次检索片段" /></label
        ><SourceCards />
        <div class="studio-pane-footnote">仅显示本次真实检索命中的内容。</div>
      </aside>

      <aside v-if="layout === 'canvas'" class="studio-canvas-query">
        <div class="studio-pane-title">
          <h2><MessageSquare :size="16" />流程输入</h2>
        </div>
        <p class="studio-canvas-intro">一个问题，<br /><strong>看见背后的每一步。</strong></p>
        <QueryComposer /><ExampleQuestions /><button class="studio-new canvas-new" :disabled="running" @click="startFresh">
          <Plus :size="14" />清空并开始新查询
        </button>
        <div class="studio-canvas-key">
          <span><i></i>等待事件</span><span><i class="has-evidence"></i>已收到真实结果</span>
        </div>
        <p class="studio-canvas-disclaimer">画布按输入、Agent、检索、回答、引用展示信息。拖动只调整位置，不会修改后端流程或执行顺序。</p>
      </aside>

      <section v-if="layout !== 'canvas'" class="studio-conversation">
        <div class="studio-pane-title">
          <h2>
            <component :is="layout === 'research' ? BookOpen : Sparkles" :size="17" />{{
              layout === 'research' ? '边问，边核对' : '当前任务'
            }}
          </h2>
          <div>
            <button v-if="layout === 'research'" class="studio-text-button" :disabled="running" @click="startFresh">
              <Plus :size="13" />新查询</button
            ><button
              v-if="layout === 'cockpit'"
              class="studio-icon-button"
              @click="drawerOpen = !drawerOpen"
              :aria-label="drawerOpen ? '折叠资料抽屉' : '展开资料抽屉'"
            >
              <PanelRightClose v-if="drawerOpen" :size="17" /><PanelRightOpen v-else :size="17" />
            </button>
          </div>
        </div>
        <div class="studio-conversation-scroll">
          <div v-if="!submittedQuestion" class="studio-welcome">
            <span class="studio-welcome-icon"><Sparkles :size="29" /></span
            ><span class="studio-overline">{{ layout === 'research' ? 'READ. ASK. VERIFY.' : 'YOUR NEXT GOOD QUESTION' }}</span>
            <h1>{{ layout === 'research' ? '我的 AI 工作台已更新！' : '今天，想解决什么？' }}</h1>
            <p>
              {{
                layout === 'research'
                  ? '左边找到资料，中间组织答案，右边核对原文。三个视角，围绕同一个问题。'
                  : '给知识库一个具体问题。这里会显示真实执行过程、回答和可以追溯的出处。'
              }}
            </p>
            <ExampleQuestions />
          </div>
          <template v-else
            ><div class="studio-user-message">
              <span>你</span>
              <h2>{{ submittedQuestion }}</h2>
            </div>
            <div v-if="steps.length" class="studio-run-trace">
              <details :open="running || layout === 'cockpit'">
                <summary>
                  <GitBranch :size="14" />{{ running ? '正在执行' : '执行记录' }}<span>{{ steps.length }} 条真实事件</span
                  ><ChevronDown :size="13" />
                </summary>
                <ol>
                  <li v-for="(step, index) in steps" :key="index">
                    <span>{{ index + 1 }}</span>
                    <div>
                      <strong>{{ step.label }}</strong>
                      <p v-if="step.query">{{ step.query }}</p>
                    </div>
                  </li>
                </ol>
              </details>
            </div>
            <div v-if="running" class="studio-progress-message" role="status">
              <LoaderCircle :size="15" class="studio-spin" />等待下一条真实执行结果…
            </div>
            <article v-if="result" class="studio-response">
              <div class="studio-response-label">
                <Sparkles :size="17" /><strong>{{ resultTitle }}</strong>
              </div>
              <MarkdownText class="studio-answer-text" :content="result.answer" />
              <p v-if="result.next_step" class="studio-next-step"><strong>下一步：</strong>{{ result.next_step }}</p>
              <div v-if="result.sources.length" class="studio-answer-sources">
                <span>查看出处</span
                ><button v-for="source in result.sources" :key="source.citation_id" @click="openSource(source)" :title="source.title">
                  {{ source.citation_id }} <ArrowRight :size="11" />
                </button>
              </div>
              <div class="studio-answer-note">{{ result.search_count }} 次实际检索 · 点击引用按钮核对原文</div>
            </article></template
          >
          <div v-if="error" class="studio-error" role="alert">
            <strong>这次查询没有完成</strong>
            <p>{{ error }}</p>
            <p v-if="errorNextStep"><strong>下一步：</strong>{{ errorNextStep }}</p>
            <span v-if="sources.length">已收到的检索片段仍可查看。</span>
          </div>
        </div>
        <QueryComposer />
      </section>

      <section v-else class="studio-canvas-center">
        <div class="studio-canvas-bar">
          <div>
            <GitBranch :size="17" /><strong>知识问答 · 执行视图</strong
            ><span>{{ running ? '请求进行中' : result ? '结果已返回' : '等待提问' }}</span>
          </div>
          <button class="studio-icon-button" @click="resetCanvas" aria-label="重置节点位置和缩放"><RefreshCw :size="15" /></button>
        </div>
        <div v-if="error" class="studio-error canvas-error" role="alert">
          <strong>这次查询没有完成</strong>
          <p>{{ error }}</p>
          <p v-if="errorNextStep"><strong>下一步：</strong>{{ errorNextStep }}</p>
        </div>
        <div ref="viewport" class="studio-canvas-viewport">
          <div class="studio-world-extent" :style="{ width: `${1000 * zoom}px`, height: `${640 * zoom}px` }">
            <div class="studio-world" :style="{ transform: `scale(${zoom})` }">
              <svg class="studio-edges" viewBox="0 0 1000 640" aria-hidden="true">
                <defs>
                  <marker id="studio-flow-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
                    <path d="M0 0L7 3.5L0 7" />
                  </marker>
                </defs>
                <path v-for="edge in edges" :key="edge.id" :d="edge.path" marker-end="url(#studio-flow-arrow)" /></svg
              ><button
                v-for="node in nodes"
                :key="node.id"
                class="studio-node"
                :class="{ selected: selectedNodeId === node.id, observed: nodeHasEvidence(node.id) }"
                :style="{ left: `${node.x}px`, top: `${node.y}px` }"
                :aria-pressed="selectedNodeId === node.id"
                :aria-label="`${node.name}：${nodeState(node.id)}。可拖动或用方向键移动。`"
                @click="selectedNodeId = node.id"
                @pointerdown="dragStart($event, node.id)"
                @pointermove="dragMove"
                @pointerup="drag = null"
                @pointercancel="drag = null"
                @lostpointercapture="drag = null"
                @keydown="keyMove($event, node.id)"
              >
                <div class="studio-node-heading">
                  <span><component :is="nodeIcons[node.id]" :size="19" /></span>
                  <div>
                    <strong>{{ node.name }}</strong
                    ><small>{{ node.subtitle }}</small>
                  </div>
                  <i></i>
                </div>
                <div class="studio-node-status"><Check v-if="nodeHasEvidence(node.id)" :size="11" />{{ nodeState(node.id) }}</div>
              </button>
              <div class="studio-world-label">点击节点检查结果 · 拖动调整视图</div>
            </div>
          </div>
        </div>
        <div class="studio-canvas-tools">
          <button @click="changeZoom(-0.1)" :disabled="zoom <= 0.4" aria-label="缩小画布"><Minus :size="15" /></button
          ><span>{{ Math.round(zoom * 100) }}%</span
          ><button @click="changeZoom(0.1)" :disabled="zoom >= 1.4" aria-label="放大画布"><ZoomIn :size="15" /></button><i></i
          ><button @click="fitCanvas" aria-label="让画布适合当前宽度"><Maximize2 :size="15" /></button>
        </div>
        <span class="studio-canvas-note">视图节点用于解释过程，真实流程可能重复检索。</span>
      </section>

      <aside v-if="layout === 'canvas'" class="studio-inspector">
        <div class="studio-pane-title">
          <h2><component :is="nodeIcons[selectedNodeId]" :size="16" />{{ selectedNode.name }} · 检查器</h2>
        </div>
        <div class="studio-inspector-body">
          <span class="studio-inspector-status" :class="{ observed: nodeHasEvidence(selectedNodeId) }">{{ nodeState(selectedNodeId) }}</span
          ><template v-if="selectedNodeId === 'input'"
            ><h3>提交的问题</h3>
            <p class="studio-inspector-text">
              {{ submittedQuestion || '还没有提交问题。从左侧输入并运行后，这里显示实际输入。' }}
            </p></template
          ><template v-else-if="selectedNodeId === 'answer'"
            ><h3>{{ resultTitle }}</h3>
            <template v-if="result"
              ><MarkdownText class="studio-inspector-text" :content="result.answer" />
              <p v-if="result.next_step" class="studio-next-step"><strong>下一步：</strong>{{ result.next_step }}</p></template
            >
            <p v-else class="studio-inspector-text">还没有收到最终结果。运行后，这里显示后端返回的原始答案。</p></template
          ><template v-else-if="selectedNodeId === 'citation'"
            ><h3>回答出处</h3>
            <p v-if="!result" class="studio-inspector-text">等待最终回答返回来源。没有提前填入示例引用。</p>
            <template v-else
              ><p class="studio-inspector-text">
                {{ result.sources.length ? '点击资料查看实际命中片段和完整原文。' : '本次结果没有返回可用出处。' }}
              </p>
              <SourceCards /></template></template
          ><template v-else
            ><h3>已收到的事件</h3>
            <p v-if="!nodeEvents.length" class="studio-inspector-text">这个步骤尚未返回事件。</p></template
          >
          <ol v-if="nodeEvents.length" class="studio-event-list">
            <li v-for="(event, index) in nodeEvents" :key="index">
              <strong>{{ event.label }}</strong>
              <p v-if="event.query">{{ event.query }}</p>
            </li>
          </ol>
          <template v-if="selectedNodeId === 'search' && sources.length"
            ><h3>检索片段</h3>
            <SourceCards
          /></template>
          <div v-if="selectedSource" class="studio-inspector-reader">
            <div class="studio-inspector-reader-title">
              <strong>选中的原文</strong><button @click="selectedSource = null" aria-label="关闭选中原文"><X :size="13" /></button>
            </div>
            <Reader />
          </div>
        </div>
      </aside>

      <aside v-if="layout === 'research' || (layout === 'cockpit' && drawerOpen)" class="studio-reader-pane">
        <div class="studio-pane-title">
          <h2><BookOpen :size="16" />{{ layout === 'research' ? '原文阅读' : '资料抽屉' }}</h2>
          <button v-if="layout === 'cockpit'" class="studio-icon-button" @click="drawerOpen = false" aria-label="关闭资料抽屉">
            <X :size="15" />
          </button>
        </div>
        <div v-if="layout === 'cockpit'" class="studio-drawer-tabs">
          <button :class="{ selected: drawerTab === 'sources' }" @click="drawerTab = 'sources'">
            检索资料 <span>{{ sources.length }}</span></button
          ><button :class="{ selected: drawerTab === 'reader' }" @click="drawerTab = 'reader'">查看原文</button>
        </div>
        <template v-if="layout === 'cockpit' && drawerTab === 'sources'"
          ><label class="studio-source-filter"
            ><Search :size="13" /><input v-model="sourceFilter" placeholder="筛选本次片段" aria-label="筛选本次检索片段" /></label
          ><SourceCards /></template
        ><Reader v-else />
      </aside>
    </div>
    <div class="studio-bottom-bar">
      <span>{{ layoutTitle }} · 本地工作台</span><span>原笔记只读 · 当前查询保留在本页会话，刷新后清空</span>
    </div>
  </div>
</template>
