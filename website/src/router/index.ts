import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import sitemapRoutesJson from './sitemap-routes.json';

export interface RouteMetaInfo {
    path: string;
    name?: string | null;
    changefreq: 'weekly' | 'monthly' | 'yearly';
    priority: number;
}

export const sitemapRoutes: RouteMetaInfo[] = sitemapRoutesJson as RouteMetaInfo[];

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        redirect: '/home',
    },
    {
        path: '/wine-tasting',
        name: 'WineTasting',
        component: () => import('../views/WineTasting.vue'),
    },
    {
        path: '/home',
        name: 'LandingPage',
        component: () => import('../views/LandingPage.vue'),
    },
    {
        path: '/vino',
        name: 'WineMenu',
        component: () => import('../views/WineMenu.vue'),
    },
    {
        path: '/drinks',
        name: 'DrinkMenu',
        component: () => import('../views/DrinkMenu.vue'),
    },
    {
        path: '/snacks',
        name: 'SnackMenu',
        component: () => import('../views/SnackMenu.vue'),
    },
    {
        path: '/showroom',
        name: 'Showroom',
        component: () => import('../views/Showroom.vue'),
    },
    {
        path: '/legals',
        name: 'Legals',
        component: () => import('../views/Legals.vue'),
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/home',
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
    scrollBehavior(_to, _from, savedPosition) {
        if (savedPosition) {
            return savedPosition;
        }
        return { left: 0, top: 0 };
    },
});

export default router;
