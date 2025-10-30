import {ref} from 'vue';

interface Snack {
    id: number;
    name: string;
    price: string;
    category: string;
    description?: string;
    allergens?: number[];
    vegetarian: boolean;
    vegan: boolean;
    available: boolean;
    image?: string;
    neu?: boolean;
}

// Support both local development and production
const getApiUrl = () => {
    if (import.meta.env.DEV || window.location.hostname === 'localhost') {
        return 'http://localhost:8080/api/snacks';
    }
    return 'https://casavazquez-website-594856899017.europe-central2.run.app/api/snacks';
};

const API_URL = getApiUrl();

export function useSnacksMenu() {
    const snacks = ref<Snack[]>([]);
    const loading = ref(true);
    const error = ref<string | null>(null);

    async function loadSnacks(filters?: {
        category?: string;
        vegetarian?: boolean;
        vegan?: boolean;
        available_only?: boolean;
    }) {
        loading.value = true;
        error.value = null;

        try {
            let url = API_URL;
            if (filters) {
                const params = new URLSearchParams();
                if (filters.category) params.append('category', filters.category);
                if (filters.vegetarian !== undefined) params.append('vegetarian', String(filters.vegetarian));
                if (filters.vegan !== undefined) params.append('vegan', String(filters.vegan));
                if (filters.available_only !== undefined) params.append('available_only', String(filters.available_only));
                
                if (params.toString()) {
                    url += `?${params.toString()}`;
                }
            }

            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            snacks.value = await res.json();
        } catch (err: any) {
            error.value = err.message || 'Unbekannter Fehler beim Laden der Snacks';
            console.error('Error loading snacks:', err);
        } finally {
            loading.value = false;
        }
    }

    async function getAvailableCategories(): Promise<string[]> {
        try {
            const res = await fetch(`${API_URL}/categories/available`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return await res.json();
        } catch (err) {
            console.error('Error loading snack categories:', err);
            return [];
        }
    }

    return {
        snacks,
        loading,
        error,
        loadSnacks,
        getAvailableCategories
    };
}
