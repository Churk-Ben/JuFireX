import { createRouter, createWebHistory } from "vue-router";

const AppHome = () => import("@/pages/AppHome.vue");

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: "/", component: AppHome },
	],
});

export default router;
