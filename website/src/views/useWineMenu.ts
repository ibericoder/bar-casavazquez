import {ref} from 'vue';
import type {Wine} from '../interfaces/vino.ts';

const API_URL = 'https://casavazquez-website-594856899017.europe-central2.run.app/casavazquez/api/vinos';

export function useWineMenu() {

    const vinos = ref<Wine[]>([]);
    const loading = ref(true);
    const error = ref<string | null>(null);

    async function loadVinos() {

        try {
            const res = await fetch(API_URL);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            vinos.value = await res.json();
        } catch (err: any) {
            error.value = err.message || 'Unbekannter Fehler';
        } finally {
            loading.value = false;
        }

    }

    return {loadVinos, vinos, loading, error};
}