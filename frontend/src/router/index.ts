import { createRouter, createWebHistory } from "vue-router";

// pages/
const AppHome = () => import("@/pages/AppHome.vue");
const Navigations = () => import("@/pages/Navigations.vue");
const Projects = () => import("@/pages/Projects.vue");
const Blogs = () => import("@/pages/Blogs.vue");
const ApiTest = () => import("@/pages/ApiTest.vue");

const Login = () => import("@/pages/Login.vue");
const Register = () => import("@/pages/Register.vue");

// pages/user/
const UserProfile = () => import("@/pages/user/Profile.vue");
const UserSettings = () => import("@/pages/user/Settings.vue");
const UserLogout = () => import("@/pages/user/Logout.vue");

// pages/admin/
const AdminUsers = () => import("@/pages/admin/Users.vue");
const AdminNavigations = () => import("@/pages/admin/Navigations.vue");
const AdminProjects = () => import("@/pages/admin/Projects.vue");
const AdminBlogs = () => import("@/pages/admin/Blogs.vue");

// pages/blog/
const BlogOverview = () => import("@/pages/blog/Overview.vue");
const BlogEditor = () => import("@/pages/blog/Editor.vue");

// pages/project
const ProjectOverview = () => import("@/pages/project/Overview.vue");
const ProjectExplorer = () => import("@/pages/project/Explorer.vue");

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: AppHome },
    { path: "/navigations", component: Navigations },
    { path: "/projects", component: Projects },
    { path: "/blogs", component: Blogs },
    { path: "/test", component: ApiTest },
    { path: "/login", component: Login },
    { path: "/register", component: Register },
    { path: "/user", redirect: "/user/profile" },
    { path: "/user/profile", component: UserProfile },
    { path: "/user/settings", component: UserSettings },
    { path: "/user/logout", component: UserLogout },
    { path: "/admin", redirect: "/admin/users" },
    { path: "/admin/users", component: AdminUsers },
    { path: "/admin/navigations", component: AdminNavigations },
    { path: "/admin/projects", component: AdminProjects },
    { path: "/admin/blogs", component: AdminBlogs },
    { path: "/blog", redirect: "/blogs" },
    { path: "/blog/:uuid", component: BlogOverview },
    { path: "/blog/:uuid/editor", component: BlogEditor },
    { path: "/project", redirect: "/projects" },
    { path: "/project/:uuid", component: ProjectOverview },
    { path: "/project/:uuid/explorer", component: ProjectExplorer },
  ],
});

export default router;
