import { createRouter, createWebHistory } from 'vue-router'
import Settings from "../components/Settings.vue";
import Main from "../components/Main.vue";

const routes = [
    {
        path: '/',
        redirect: '/main'
    },
    {
        path: '/main',
        name: 'Main',
        component: Main
    },
    {
        path: '/settings',
        name: 'Settings',
        component: Settings,
        meta: {
          title: 'Settings'
        }
      },

]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router