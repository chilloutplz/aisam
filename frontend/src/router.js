import { createRouter, createWebHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";
import TocView from "./views/TocView.vue";
import UnitView from "./views/UnitView.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/toc", name: "toc", component: TocView },
  { path: "/unit/:id", name: "unit", component: UnitView, props: true },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
