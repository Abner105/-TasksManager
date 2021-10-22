import Vue from "vue";
import VueRouter from "vue-router";
const Tasks = () => import('../components/TaskList.vue')
const Projects = () => import('../components/ProjectList.vue')
Vue.use(VueRouter)
const routes = [
    {
        path: '',
        redirect: '/tasks'
    },
    {
        path: '/tasks',
        component: Tasks,
    },
    {
        path: '/projects',
        component: Projects,
    }
]
const router = new VueRouter({
    routes,
    mode: 'history'
})
export default router