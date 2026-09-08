import { ref } from "vue";

export const WORKSPACE_MODES = [
  { id: "cockpit", title: "任务指挥台" },
  { id: "research", title: "知识研究工作室" },
  { id: "canvas", title: "可视流程画布" },
] as const;
export type WorkspaceMode = (typeof WORKSPACE_MODES)[number]["id"];
const STORAGE_KEY = "sanjiu-workbench-mode";

export function parseWorkspaceMode(value: unknown): WorkspaceMode | undefined {
  return WORKSPACE_MODES.find((mode) => mode.id === value)?.id;
}

function initialMode(): WorkspaceMode {
  try {
    return parseWorkspaceMode(window.localStorage.getItem(STORAGE_KEY)) ?? "research";
  } catch {
    return "research";
  }
}

export const preferredMode = ref<WorkspaceMode>(initialMode());

export function rememberWorkspaceMode(mode: WorkspaceMode) {
  preferredMode.value = mode;
  try {
    // Persist only the layout choice, never questions, answers or note content.
    window.localStorage.setItem(STORAGE_KEY, mode);
  } catch {
    // Layout switching still works if browser storage is unavailable.
  }
}
