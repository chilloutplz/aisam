import { createRouter, createWebHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";
import TocView from "./views/TocView.vue";
import UnitView from "./views/UnitView.vue";
import { loadState } from "./storage.js";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/toc", name: "toc", component: TocView },
  { path: "/unit/:id", name: "unit", component: UnitView, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 홈 화면으로 오면, 저장된 마지막 위치가 있는지 확인해서
// 있으면 처음부터 다시 고르지 않고 그 지점으로 바로 이동시킨다.
router.beforeEach((to) => {
  if (to.name === "home") {
    const state = loadState();
    if (state?.level && state?.grade && state?.subject) {
      if (state.lastUnitId) {
        return { name: "unit", params: { id: state.lastUnitId } };
      }
      return { name: "toc" };
    }
  }
});

export default router;
