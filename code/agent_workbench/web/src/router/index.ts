import { createRouter, createWebHistory } from "vue-router";
import { parseWorkspaceMode, preferredMode, rememberWorkspaceMode } from "../lib/workspaceMode";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: () => import("../views/HomeView.vue") },
    { path: "/themes", component: () => import("../views/ThemeGallery.vue") },
    { path: "/gallery", component: () => import("../views/WorkspaceGallery.vue") },
    { path: "/studio", component: () => import("../views/StudioPrototype.vue") },
    {
      path: "/knowledge",
      component: () => import("../views/KnowledgeView.vue"),
    },
    {
      path: "/incidents",
      component: () => import("../views/IncidentView.vue"),
    },
    {
      path: "/documents",
      component: () => import("../views/DocumentsView.vue"),
    },
    { path: "/roadmap", component: () => import("../views/RoadmapView.vue") },
    { path: "/:pathMatch(.*)*", redirect: "/" },
  ],
});

router.beforeEach((to) => {
  if (to.path === "/studio" && !parseWorkspaceMode(to.query.layout)) {
    return { path: to.path, query: { ...to.query, layout: preferredMode.value }, hash: to.hash, replace: true };
  }
});

router.afterEach((to, _from, failure) => {
  const mode = parseWorkspaceMode(to.query.layout);
  if (!failure && to.path === "/studio" && mode) rememberWorkspaceMode(mode);
});

export default router;
