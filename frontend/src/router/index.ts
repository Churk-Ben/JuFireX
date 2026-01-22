import { createRouter, createWebHistory } from "vue-router";

const AppHome = () => import("@/pages/AppHome.vue");
const ApiTest = () => import("@/pages/ApiTest.vue");

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: "/", component: AppHome },
		{ path: "/test", component: ApiTest },
	],
});

export default router;
