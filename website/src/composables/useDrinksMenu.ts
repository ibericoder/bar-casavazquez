import {ref} from 'vue';

interface Drink {
    id: number;
    name: string;
    category: string;
    price: string;
    volume?: string;
    alcoholic: boolean;
    allergens?: number[];
    neu?: boolean;
    available: boolean;
    description?: string;
    image?: string;
}

// Support both local development and production
const getApiUrl = () => {
    if (import.meta.env.DEV || window.location.hostname === 'localhost') {
        return 'http://localhost:8080/api/drinks';
    }
    return 'https://casavazquez-website-594856899017.europe-central2.run.app/api/drinks';
};

const API_URL = getApiUrl();

export function useDrinksMenu() {
    const drinks = ref<Drink[]>([]);
    const loading = ref(true);
    const error = ref<string | null>(null);

    async function loadDrinks(filters?: {
        category?: string;
        alcoholic?: boolean;
        available_only?: boolean;
    }) {
        loading.value = true;
        error.value = null;

        try {
            let url = API_URL;
            if (filters) {
                const params = new URLSearchParams();
                if (filters.category) params.append('category', filters.category);
                if (filters.alcoholic !== undefined) params.append('alcoholic', String(filters.alcoholic));
                if (filters.available_only !== undefined) params.append('available_only', String(filters.available_only));
                
                if (params.toString()) {
                    url += `?${params.toString()}`;
                }
            }

            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            drinks.value = await res.json();
        } catch (err: any) {
            error.value = err.message || 'Unbekannter Fehler beim Laden der Getränke';
            console.error('Error loading drinks:', err);
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
            console.error('Error loading drink categories:', err);
            return [];
        }
    }

    return {
        drinks,
        loading,
        error,
        loadDrinks,
        getAvailableCategories
    };
}