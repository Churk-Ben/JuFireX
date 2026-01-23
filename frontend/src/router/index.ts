import { createRouter, createWebHistory } from "vue-router";

const ApiTest = () => import("@/pages/ApiTest.vue");
const AppHome = () => import("@/pages/AppHome.vue");
const Navigations = () => import("@/pages/Navigations.vue");
const Projects = () => import("@/pages/Projects.vue");

const AdminUsers = () => import("@/pages/admin/Users.vue");
const AdminNavigations = () => import("@/pages/admin/Navigations.vue");
const AdminProjects = () => import("@/pages/admin/Projects.vue");

const UserProfile = () => import("@/pages/user/Profile.vue");
const UserSettings = () => import("@/pages/user/Settings.vue");
const UserLogout = () => import("@/pages/user/Logout.vue");
const Login = () => import("@/pages/Login.vue");

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: "/test", component: ApiTest },
		{ path: "/", component: AppHome },
		{ path: "/navigations", component: Navigations },
		{ path: "/projects", component: Projects },
		{ path: "/admin", redirect: "/admin/users" },
		{ path: "/admin/users", component: AdminUsers },
		{ path: "/admin/navigations", component: AdminNavigations },
		{ path: "/admin/projects", component: AdminProjects },
		{ path: "/login", component: Login },
		{ path: "/user", redirect: "/user/profile" },
		{ path: "/user/profile", component: UserProfile },
		{ path: "/user/settings", component: UserSettings },
		{ path: "/user/logout", component: UserLogout },
	],
});

export default router;
