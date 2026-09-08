export interface ModuleInfo {
  id: string;
  title: string;
  status: string;
  detail: string;
}
export interface Health {
  status: string;
  modules: ModuleInfo[];
}
export interface DocumentInfo {
  page_content: string;
  metadata: Record<string, unknown>;
}
export interface Preset {
  id: string;
  title: string;
  description: string;
  uses_model: boolean;
  fictional: boolean;
  input: Record<string, unknown>;
}
export async function getJson<T>(
  url: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok)
    throw new Error(
      data.error?.message ??
        data.detail?.error?.message ??
        data.detail?.message ??
        "请求失败，请查看后端状态。",
    );
  return data as T;
}

/** Read complete SSE frames even when frames are split across network chunks. */
export async function consumeEvents(
  response: Response,
  onEvent: (event: string, data: unknown) => void,
) {
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error?.message ?? "无法启动工作流。");
  }
  if (!response.body) throw new Error("浏览器没有收到可读取的响应。");
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let pending = "";
  function flush() {
    let match: RegExpExecArray | null;
    while ((match = /\r?\n\r?\n/.exec(pending))) {
      const frame = pending.slice(0, match.index);
      pending = pending.slice(match.index + match[0].length);
      let event = "message";
      const data: string[] = [];
      for (const line of frame.split(/\r?\n/)) {
        if (line.startsWith("event:")) event = line.slice(6).trim();
        if (line.startsWith("data:"))
          data.push(line.slice(5).replace(/^ /, ""));
      }
      if (data.length) onEvent(event, JSON.parse(data.join("\n")));
    }
  }
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        pending += decoder.decode();
        flush();
        break;
      }
      pending += decoder.decode(value, { stream: true });
      flush();
    }
  } finally {
    await reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}
