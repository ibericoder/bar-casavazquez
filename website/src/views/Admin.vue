<template>
  <div class="admin-panel">
    <h1>Admin Panel</h1>

    <div class="tabs">
      <button v-for="tab in tabs" :key="tab" :class="{ active: activeTab === tab }" @click="activeTab = tab">
        {{ tab }}
      </button>
    </div>

    <div v-if="loading">Loading {{ activeTab }}...</div>
    <div v-if="error">Error: {{ error }}</div>

    <div v-if="activeTab === 'Wines' && !loading && wines.length">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Bottle</th>
            <th>0.1l</th>
            <th>0.2l</th>
            <th>Available</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="wine in wines" :key="wine.id">
            <td>
              <input type="text" v-model="wine.name" @change="updateWineDetails(wine)">
            </td>
            <td>
              <input type="text" v-model="wine.short_description" @change="updateWineDetails(wine)">
            </td>
            <td>
              <input type="text" v-model="wine.prices.flasche" @change="updateWinePrice(wine)">
            </td>
            <td>
              <input type="text" v-model="wine.prices['0.1l']" @change="updateWinePrice(wine)">
            </td>
            <td>
              <input type="text" v-model="wine.prices['0.2l']" @change="updateWinePrice(wine)">
            </td>
            <td>
              <input type="checkbox" v-model="wine.available" @change="toggleWineAvailable(wine)">
            </td>
            <td>
              <button @click="deleteWine(wine)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="activeTab === 'Drinks' && !loading && drinks.length">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Available</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drink in drinks" :key="drink.id">
            <td>{{ drink.name }}</td>
            <td>{{ drink.description }}</td>
            <td>
              <input type="text" v-model="drink.price" @change="updateDrinkPrice(drink)">
            </td>
            <td>
              <input type="checkbox" v-model="drink.available" @change="toggleDrinkAvailable(drink)">
            </td>
            <td>
              <button @click="deleteDrink(drink)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="activeTab === 'Snacks' && !loading && snacks.length">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Available</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="snack in snacks" :key="snack.id">
            <td>{{ snack.name }}</td>
            <td>{{ snack.description }}</td>
            <td>
              <input type="text" v-model="snack.price" @change="updateSnackPrice(snack)">
            </td>
            <td>
              <input type="checkbox" v-model="snack.available" @change="toggleSnackAvailable(snack)">
            </td>
            <td>
              <button @click="deleteSnack(snack)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import type { Wine as WineItem } from '../interfaces/vino';

type TabKey = 'Wines' | 'Drinks' | 'Snacks';

type DrinkItem = {
  id: number;
  name: string;
  description?: string;
  available: boolean;
  category: string;
  price: string;
};

type SnackItem = {
  id: number;
  name: string;
  description?: string;
  available: boolean;
  price: string;
};

const tabs: TabKey[] = ['Wines', 'Drinks', 'Snacks'];
const activeTab = ref<TabKey>('Wines');

const wines = ref<WineItem[]>([]);
const drinks = ref<DrinkItem[]>([]);
const snacks = ref<SnackItem[]>([]);

const loading = ref(false);
const error = ref<string | null>(null);

const isLocal = import.meta.env.DEV
  || window.location.hostname === 'localhost'
  || window.location.hostname === '127.0.0.1';

const API_BASE = isLocal
  ? 'http://localhost:8080'
  : 'https://casavazquez-website-594856899017.europe-central2.run.app';

async function loadWines() {
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch(`${API_BASE}/api/wines?available_only=false`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    wines.value = data as WineItem[];
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load wines';
  } finally {
    loading.value = false;
  }
}

async function loadDrinks() {
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch(`${API_BASE}/api/drinks?available_only=false`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    drinks.value = data as DrinkItem[];
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load drinks';
  } finally {
    loading.value = false;
  }
}

async function loadSnacks() {
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch(`${API_BASE}/api/snacks?available_only=false`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    snacks.value = data as SnackItem[];
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load snacks';
  } finally {
    loading.value = false;
  }
}

async function toggleWineAvailable(wine: WineItem) {
  const nextStatus = wine.available;
  try {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}/availability?available=${nextStatus}`, {
      method: 'PATCH'
    });
    if (!response.ok) throw new Error('Failed to update wine');
    await loadWines();
  } catch (err) {
    window.alert('Error updating wine');
    wine.available = !nextStatus;
  }
}

async function toggleDrinkAvailable(drink: DrinkItem) {
  const nextStatus = drink.available;
  try {
    const response = await fetch(`${API_BASE}/api/drinks/${drink.id}/availability?available=${nextStatus}`, {
      method: 'PATCH'
    });
    if (!response.ok) throw new Error('Failed to update drink');
    await loadDrinks();
  } catch (err) {
    window.alert('Error updating drink');
    drink.available = !nextStatus;
  }
}

async function toggleSnackAvailable(snack: SnackItem) {
  const nextStatus = snack.available;
  try {
    const response = await fetch(`${API_BASE}/api/snacks/${snack.id}/availability?available=${nextStatus}`, {
      method: 'PATCH'
    });
    if (!response.ok) throw new Error('Failed to update snack');
    await loadSnacks();
  } catch (err) {
    window.alert('Error updating snack');
    snack.available = !nextStatus;
  }
}

async function updateWinePrice(wine: WineItem) {
  try {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}/price`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(wine.prices)
    });
    if (!response.ok) throw new Error('Failed to update wine price');
  } catch (err) {
    window.alert('Error updating wine price');
  }
}

async function updateWineDetails(wine: WineItem) {
  try {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}/details`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: wine.name, short_description: wine.short_description })
    });
    if (!response.ok) throw new Error('Failed to update wine details');
  } catch (err) {
    window.alert('Error updating wine details');
  }
}

async function updateDrinkPrice(drink: DrinkItem) {
  try {
    const response = await fetch(`${API_BASE}/api/drinks/${drink.id}/price`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ price: drink.price })
    });
    if (!response.ok) throw new Error('Failed to update drink price');
  } catch (err) {
    window.alert('Error updating drink price');
  }
}

async function updateSnackPrice(snack: SnackItem) {
  try {
    const response = await fetch(`${API_BASE}/api/snacks/${snack.id}/price`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ price: snack.price })
    });
    if (!response.ok) throw new Error('Failed to update snack price');
  } catch (err) {
    window.alert('Error updating snack price');
  }
}

async function deleteWine(wine: WineItem) {
  if (!window.confirm(`Delete ${wine.name}?`)) return;
  try {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete wine');
    wines.value = wines.value.filter(item => item.id !== wine.id);
  } catch (err) {
    window.alert('Error deleting wine');
  }
}

async function deleteDrink(drink: DrinkItem) {
  if (!window.confirm(`Delete ${drink.name}?`)) return;
  try {
    const response = await fetch(`${API_BASE}/api/drinks/${drink.id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete drink');
    drinks.value = drinks.value.filter(item => item.id !== drink.id);
  } catch (err) {
    window.alert('Error deleting drink');
  }
}

async function deleteSnack(snack: SnackItem) {
  if (!window.confirm(`Delete ${snack.name}?`)) return;
  try {
    const response = await fetch(`${API_BASE}/api/snacks/${snack.id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete snack');
    snacks.value = snacks.value.filter(item => item.id !== snack.id);
  } catch (err) {
    window.alert('Error deleting snack');
  }
}

watch(activeTab, (newTab) => {
  error.value = null;
  if (newTab === 'Wines' && wines.value.length === 0) loadWines();
  if (newTab === 'Drinks' && drinks.value.length === 0) loadDrinks();
  if (newTab === 'Snacks' && snacks.value.length === 0) loadSnacks();
});

onMounted(() => {
  loadWines();
});
</script>

<style scoped>
.admin-panel {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #ddd;
}

.tabs button {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 1rem;
}

.tabs button.active {
  border-bottom-color: #333;
  font-weight: bold;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th,
td {
  padding: 0.5rem;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background: #f4f4f4;
}

button {
  margin-right: 0.5rem;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}
</style>