import { createRouter, createWebHistory } from "vue-router";

const ApiTest = () => import("@/pages/ApiTest.vue");
const AppHome = () => import("@/pages/AppHome.vue");
const Navigations = () => import("@/pages/Navigations.vue");
const Projects = () => import("@/pages/Projects.vue");

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: "/test", component: ApiTest },
		{ path: "/", component: AppHome },
		{ path: "/navigations", component: Navigations },
		{ path: "/projects", component: Projects },
	],
});

export default router;
