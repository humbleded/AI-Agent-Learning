import MarkdownIt from "markdown-it";

// Notes and model output are untrusted text. Keep formatting, never execute HTML
// or automatically load remote images and links from the private knowledge base.
const renderer = new MarkdownIt({ html: false, linkify: false, breaks: true });
renderer.disable(["image", "link", "autolink"]);

export function renderMarkdown(content: string): string {
  return renderer.render(content);
}
