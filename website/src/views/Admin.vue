<template>
  <div class="admin-panel">
    <h1>Admin Panel</h1>

    <div v-if="lastChange" class="undo-banner">
      <span>letzte Änderung: {{ lastChange.type }} von {{ lastChange.itemName }}</span>
      <button @click="undoLastChange" class="undo-btn">Undo</button>
    </div>

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
              <input type="number" step="0.01" v-model.number="wine.price_bottle" @change="updateWinePrice(wine)">€
            </td>
            <td>
              <input type="number" step="0.01" v-model.number="wine.price_glass_01" @change="updateWinePrice(wine)">€
            </td>
            <td>
              <input type="number" step="0.01" v-model.number="wine.price_glass_02" @change="updateWinePrice(wine)">€
            </td>
            <td>
              <input type="checkbox" v-model="wine.available" @change="toggleWineAvailable(wine)">
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="drink in drinks" :key="drink.id">
            <td>{{ drink.name }}</td>
            <td>{{ drink.description }}</td>
            <td>
              <input type="number" step="0.01" v-model.number="drink.price" @change="updateDrinkPrice(drink)">€
            </td>
            <td>
              <input type="checkbox" v-model="drink.available" @change="toggleDrinkAvailable(drink)">
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="snack in snacks" :key="snack.id">
            <td>{{ snack.name }}</td>
            <td>{{ snack.description }}</td>
            <td>
              <input type="number" step="0.01" v-model.number="snack.price" @change="updateSnackPrice(snack)">€
            </td>
            <td>
              <input type="checkbox" v-model="snack.available" @change="toggleSnackAvailable(snack)">
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

type ChangeHistory = {
  type: 'wine-price' | 'wine-details' | 'wine-availability' | 'drink-price' | 'drink-availability' | 'snack-price' | 'snack-availability';
  itemId: string | number;
  itemName: string;
  previousData: any;
  endpoint: string;
};

const tabs: TabKey[] = ['Wines', 'Drinks', 'Snacks'];
const activeTab = ref<TabKey>('Wines');

const wines = ref<WineItem[]>([]);
const drinks = ref<DrinkItem[]>([]);
const snacks = ref<SnackItem[]>([]);

const loading = ref(false);
const error = ref<string | null>(null);
const lastChange = ref<ChangeHistory | null>(null);

const isLocal = import.meta.env.DEV
  || window.location.hostname === 'localhost'
  || window.location.hostname === '127.0.0.1';

const API_BASE = isLocal
  ? 'http://localhost:8080'
  : window.location.origin; // Use the same origin as the current page

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

async function undoLastChange() {
  if (!lastChange.value) return;
  
  try {
    const response = await fetch(`${API_BASE}${lastChange.value.endpoint}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(lastChange.value.previousData)
    });
    
    if (!response.ok) throw new Error('Failed to undo change');
    
    if (lastChange.value.type.startsWith('wine')) await loadWines();
    else if (lastChange.value.type.startsWith('drink')) await loadDrinks();
    else if (lastChange.value.type.startsWith('snack')) await loadSnacks();
    
    lastChange.value = null;
  } catch (err) {
    window.alert('Error undoing change: ' + (err instanceof Error ? err.message : 'Unknown error'));
  }
}

async function toggleWineAvailable(wine: WineItem) {
  const previousAvailable = wine.available;
  const nextStatus = !previousAvailable;
  wine.available = nextStatus;
  
  lastChange.value = {
    type: 'wine-availability',
    itemId: wine.id,
    itemName: wine.name,
    previousData: { available: previousAvailable },
    endpoint: `/api/wines/${wine.id}/availability?available=${previousAvailable}`
  };
  
  try {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}/availability?available=${nextStatus}`, {
      method: 'PATCH'
    });
    if (!response.ok) throw new Error('Failed to update wine');
    await loadWines();
  } catch (err) {
    window.alert('Error updating wine');
    wine.available = previousAvailable;
    lastChange.value = null;
  }
}

async function toggleDrinkAvailable(drink: DrinkItem) {
  const previousAvailable = drink.available;
  const nextStatus = !previousAvailable;
  drink.available = nextStatus;
  
  lastChange.value = {
    type: 'drink-availability',
    itemId: drink.id,
    itemName: drink.name,
    previousData: { available: previousAvailable },
    endpoint: `/api/drinks/${drink.id}/availability?available=${previousAvailable}`
  };
  
  try {
    const response = await fetch(`${API_BASE}/api/drinks/${drink.id}/availability?available=${nextStatus}`, {
      method: 'PATCH'
    });
    if (!response.ok) throw new Error('Failed to update drink');
    await loadDrinks();
  } catch (err) {
    window.alert('Error updating drink');
    drink.available = previousAvailable;
    lastChange.value = null;
  }
}

async function toggleSnackAvailable(snack: SnackItem) {
  const previousAvailable = snack.available;
  const nextStatus = !previousAvailable;
  snack.available = nextStatus;
  
  lastChange.value = {
    type: 'snack-availability',
    itemId: snack.id,
    itemName: snack.name,
    previousData: { available: previousAvailable },
    endpoint: `/api/snacks/${snack.id}/availability?available=${previousAvailable}`
  };
  
  try {
    const response = await fetch(`${API_BASE}/api/snacks/${snack.id}/availability?available=${nextStatus}`, {
      method: 'PATCH'
    });
    if (!response.ok) throw new Error('Failed to update snack');
    await loadSnacks();
  } catch (err) {
    window.alert('Error updating snack');
    snack.available = previousAvailable;
    lastChange.value = null;
  }
}

async function updateWinePrice(wine: WineItem) {
  const originalWine = wines.value.find(w => w.id === wine.id);
  if (!originalWine) return;
  
  const previousPrices = {
    price_bottle: originalWine.price_bottle,
    price_glass_01: originalWine.price_glass_01,
    price_glass_02: originalWine.price_glass_02
  };
  
  lastChange.value = {
    type: 'wine-price',
    itemId: wine.id,
    itemName: wine.name,
    previousData: previousPrices,
    endpoint: `/api/wines/${wine.id}/price`
  };
  
  try {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}/price`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        price_bottle: wine.price_bottle,
        price_glass_01: wine.price_glass_01,
        price_glass_02: wine.price_glass_02
      })
    });
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to update wine price: ${errorText}`);
    }
    console.log('Wine price updated successfully');
  } catch (err) {
    console.error('Error updating wine price:', err);
    window.alert('Error updating wine price: ' + (err instanceof Error ? err.message : 'Unknown error'));
    lastChange.value = null;
  }
}

async function updateWineDetails(wine: WineItem) {
  const originalWine = wines.value.find(w => w.id === wine.id);
  if (!originalWine) return;
  
  const previousDetails = {
    name: originalWine.name,
    short_description: originalWine.short_description
  };
  
  lastChange.value = {
    type: 'wine-details',
    itemId: wine.id,
    itemName: originalWine.name,
    previousData: previousDetails,
    endpoint: `/api/wines/${wine.id}/details`
  };
  
  try {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}/details`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: wine.name, short_description: wine.short_description })
    });
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to update wine details: ${errorText}`);
    }
    console.log('Wine details updated successfully');
  } catch (err) {
    console.error('Error updating wine details:', err);
    window.alert('Error updating wine details: ' + (err instanceof Error ? err.message : 'Unknown error'));
    lastChange.value = null;
  }
}

async function updateDrinkPrice(drink: DrinkItem) {
  const originalDrink = drinks.value.find(d => d.id === drink.id);
  if (!originalDrink) return;
  
  const previousPrice = originalDrink.price;
  
  lastChange.value = {
    type: 'drink-price',
    itemId: drink.id,
    itemName: drink.name,
    previousData: { price: previousPrice },
    endpoint: `/api/drinks/${drink.id}/price`
  };
  
  try {
    const response = await fetch(`${API_BASE}/api/drinks/${drink.id}/price`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ price: drink.price })
    });
    if (!response.ok) throw new Error('Failed to update drink price');
  } catch (err) {
    window.alert('Error updating drink price');
    lastChange.value = null;
  }
}

async function updateSnackPrice(snack: SnackItem) {
  const originalSnack = snacks.value.find(s => s.id === snack.id);
  if (!originalSnack) return;
  
  const previousPrice = originalSnack.price;
  
  lastChange.value = {
    type: 'snack-price',
    itemId: snack.id,
    itemName: snack.name,
    previousData: { price: previousPrice },
    endpoint: `/api/snacks/${snack.id}/price`
  };
  
  try {
    const response = await fetch(`${API_BASE}/api/snacks/${snack.id}/price`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ price: snack.price })
    });
    if (!response.ok) throw new Error('Failed to update snack price');
  } catch (err) {
    window.alert('Error updating snack price');
    lastChange.value = null;
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

input[type="text"] {
  width: 100%;
  min-width: 150px;
  padding: 0.25rem;
  box-sizing: border-box;
}

input[type="checkbox"] {
  cursor: pointer;
}

button {
  margin-right: 0.5rem;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}

.undo-banner {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.undo-banner span {
  font-weight: 500;
}

.undo-btn {
  background-color: #ffc107;
  color: #000;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.undo-btn:hover {
  background-color: #ffca2c;
}
</style>