import { createRouter, createWebHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";
import TocView from "./views/TocView.vue";
import UnitView from "./views/UnitView.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/toc", name: "toc", component: TocView },
  { path: "/unit/:id", name: "unit", component: UnitView, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 앱이 처음 켜졌을 때 딱 한 번만 작동하도록 플래그 설정
let isFirstLoad = true;

router.beforeEach((to, from, next) => {
  if (isFirstLoad) {
    isFirstLoad = false;
    
    // 로컬 스토리지에서 마지막으로 방문한 '전체 URL 경로'를 가져옵니다.
    const lastVisitedPath = localStorage.getItem("last_visited_path");
    
    // 사용자가 첫 메인 페이지("/")로 진입할 때만 마지막 방문 페이지로 강제 리다이렉트합니다.
    // 만약 사용자가 공유된 링크나 특정 URL을 직접 치고 들어왔다면 그 경로를 존중해 줍니다.
    if (lastVisitedPath && to.path === "/") {
      return next(lastVisitedPath);
    }
  }
  next();
});

router.afterEach((to) => {
  // 사용자가 페이지 이동에 성공하면 현재의 fullPath(예: /unit/5)를 로컬 스토리지에 기록합니다.
  if (to.path) {
    localStorage.setItem("last_visited_path", to.fullPath);
  }
});

export default router;