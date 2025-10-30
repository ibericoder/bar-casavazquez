import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../views/LandingPage.vue';
import WineMenu from '../views/WineMenu.vue';
import SnackMenu from '../views/SnackMenu.vue';
import DrinkMenu from '../views/DrinkMenu.vue';
import Showroom from '../views/Showroom.vue';
import WineTasting from '../views/WineTasting.vue';
import Legals from '../views/Legals.vue';
import Admin from '../views/Admin.vue';

const routes = [
    {
        path: '/',
        redirect: '/home',
    },
    {
        path: '/wine-tasting',
        name: 'WineTasting',
        component: WineTasting,
    },
    {
        path: '/home',
        name: 'LandingPage',
        component: LandingPage,
    },
    {
        path: '/vino',
        name: 'WineMenu',
        component: WineMenu,
    },
    {
        path: '/drinks',
        name: 'DrinkMenu',
        component: DrinkMenu,
    },
    {
        path: '/snacks',
        name: 'SnackMenu',
        component: SnackMenu,
    },
    {
        path: '/showroom',
        name: 'Showroom',
        component: Showroom,
    },
    {
        path: '/legals',
        name: 'Legals',
        component: Legals,
    },
    {
        path: '/admin',
        name: 'Admin',
        component: Admin,
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/home',
    },
];

const router = createRouter({
    history: createWebHistory('/casavazquez/'),
    routes,
    scrollBehavior(_to, _from, savedPosition) {
        if (savedPosition) {
            return savedPosition;
        }
        return { left: 0, top: 0 };
    },
});

export default router;
