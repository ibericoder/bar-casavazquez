import {ref} from 'vue';

interface Notification {
    id: number;
    title: string;
    message: string;
    type: string;
    active: boolean;
    priority: number;
    target_page?: string;
    created_at: string;
    updated_at?: string;
    expires_at?: string;
}

// Support both local development and production
const getApiUrl = () => {
    if (import.meta.env.DEV || window.location.hostname === 'localhost') {
        return 'http://localhost:8080/api/notifications';
    }
    return 'https://casavazquez-website-594856899017.europe-central2.run.app/api/notifications';
};

const API_URL = getApiUrl();

export function useNotifications() {
    const notifications = ref<Notification[]>([]);
    const loading = ref(true);
    const error = ref<string | null>(null);

    async function loadNotifications(filters?: {
        target_page?: string;
        active_only?: boolean;
    }) {
        loading.value = true;
        error.value = null;

        try {
            let url = API_URL;
            if (filters) {
                const params = new URLSearchParams();
                if (filters.target_page) params.append('target_page', filters.target_page);
                if (filters.active_only !== undefined) params.append('active_only', String(filters.active_only));
                
                if (params.toString()) {
                    url += `?${params.toString()}`;
                }
            }

            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            notifications.value = await res.json();
        } catch (err: any) {
            error.value = err.message || 'Unbekannter Fehler beim Laden der Benachrichtigungen';
            console.error('Error loading notifications:', err);
        } finally {
            loading.value = false;
        }
    }

    async function getNotificationsForPage(page: string): Promise<Notification[]> {
        try {
            const res = await fetch(`${API_URL}?target_page=${page}&active_only=true`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return await res.json();
        } catch (err) {
            console.error('Error loading page notifications:', err);
            return [];
        }
    }

    return {
        notifications,
        loading,
        error,
        loadNotifications,
        getNotificationsForPage
    };
}