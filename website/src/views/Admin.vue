<template>
  <div class="admin-panel">
    <div class="header">
      <h1>Admin Panel</h1>
      <button v-if="hasUnsavedChanges" @click="saveAllChanges" class="save-all-btn">
        💾 Speichern ({{ Object.keys(unsavedChanges).length }})
      </button>
    </div>

    <div class="tabs">
      <button v-for="tab in tabs" :key="tab" :class="{ active: activeTab === tab }" @click="activeTab = tab">
        {{ tab }}
      </button>
      <button :class="{ active: activeTab === 'Log' }" @click="activeTab = 'Log'">
        Log ({{ changeLog.length }})
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
          <tr v-for="wine in wines" :key="wine.id" :class="{ 'has-changes': isWineModified(wine.id) }">
            <td>
              <input type="text" v-model="wine.name" @input="markWineAsModified(wine)">
            </td>
            <td>
              <input type="text" v-model="wine.short_description" @input="markWineAsModified(wine)">
            </td>
            <td>
              <input type="number" step="0.01" v-model.number="wine.price_bottle" @input="markWineAsModified(wine)">€
            </td>
            <td>
              <input type="number" step="0.01" v-model.number="wine.price_glass_01" @input="markWineAsModified(wine)">€
            </td>
            <td>
              <input type="number" step="0.01" v-model.number="wine.price_glass_02" @input="markWineAsModified(wine)">€
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
          <tr v-for="drink in drinks" :key="drink.id" :class="{ 'has-changes': isDrinkModified(drink.id) }">
            <td>{{ drink.name }}</td>
            <td>{{ drink.description }}</td>
            <td>
              <input type="number" step="0.01" v-model.number="drink.price" @input="markDrinkAsModified(drink)">€
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
          <tr v-for="snack in snacks" :key="snack.id" :class="{ 'has-changes': isSnackModified(snack.id) }">
            <td>{{ snack.name }}</td>
            <td>{{ snack.description }}</td>
            <td>
              <input type="number" step="0.01" v-model.number="snack.price" @input="markSnackAsModified(snack)">€
            </td>
            <td>
              <input type="checkbox" v-model="snack.available" @change="toggleSnackAvailable(snack)">
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="activeTab === 'Log' && !loading">
      <div class="log-header">
        <h2>Änderungen</h2>
        <button @click="clearLog" class="clear-btn">zurücksetzen</button>
      </div>
      <div v-if="changeLog.length === 0" class="empty-log">
        --
      </div>
      <table v-else class="log-table">
        <thead>
          <tr>
            <th>Zeit</th>
            <th>Typ</th>
            <th>Item</th>
            <th>Änderung</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(entry, index) in changeLog.slice().reverse()" :key="index">
            <td>{{ entry.timestamp }}</td>
            <td>{{ entry.type }}</td>
            <td>{{ entry.itemName }}</td>
            <td class="change-details">{{ entry.details }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import type { Wine as WineItem } from '../interfaces/vino';

type TabKey = 'Wines' | 'Drinks' | 'Snacks' | 'Log';

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

type LogEntry = {
  timestamp: string;
  type: string;
  itemName: string;
  details: string;
};

const tabs: TabKey[] = ['Wines', 'Drinks', 'Snacks'];
const activeTab = ref<TabKey>('Wines');

const wines = ref<WineItem[]>([]);
const drinks = ref<DrinkItem[]>([]);
const snacks = ref<SnackItem[]>([]);

const originalWines = ref<Record<string | number, WineItem>>({});
const originalDrinks = ref<Record<number, DrinkItem>>({});
const originalSnacks = ref<Record<number, SnackItem>>({});

const loading = ref(false);
const error = ref<string | null>(null);
const changeLog = ref<LogEntry[]>([]);

const unsavedChanges = ref<Record<string, any>>({});
const hasUnsavedChanges = computed(() => Object.keys(unsavedChanges.value).length > 0);

const cacheTimestamps = ref<Record<string, number>>({});
const CACHE_DURATION = 2 * 60 * 60 * 1000;

const isLocal = import.meta.env.DEV
  || window.location.hostname === 'localhost'
  || window.location.hostname === '127.0.0.1';

const API_BASE = isLocal
  ? 'http://localhost:8080'
  : window.location.origin; // Use the same origin as the current page

async function loadWines(forceReload = false) {
  const now = Date.now();
  const lastLoad = cacheTimestamps.value['wines'] || 0;
  
  if (!forceReload && wines.value.length > 0 && (now - lastLoad) < CACHE_DURATION) {
    console.log('Using cached wines data');
    return;
  }
  
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch(`${API_BASE}/api/wines?available_only=false`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    wines.value = data as WineItem[];
    originalWines.value = {};
    wines.value.forEach(wine => {
      originalWines.value[wine.id] = JSON.parse(JSON.stringify(wine));
    });
    cacheTimestamps.value['wines'] = Date.now();
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load wines';
  } finally {
    loading.value = false;
  }
}

async function loadDrinks(forceReload = false) {
  const now = Date.now();
  const lastLoad = cacheTimestamps.value['drinks'] || 0;
  
  if (!forceReload && drinks.value.length > 0 && (now - lastLoad) < CACHE_DURATION) {
    console.log('Using cached drinks data');
    return;
  }
  
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch(`${API_BASE}/api/drinks?available_only=false`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    drinks.value = data as DrinkItem[];
    originalDrinks.value = {};
    drinks.value.forEach(drink => {
      originalDrinks.value[drink.id] = JSON.parse(JSON.stringify(drink));
    });
    cacheTimestamps.value['drinks'] = Date.now();
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load drinks';
  } finally {
    loading.value = false;
  }
}

async function loadSnacks(forceReload = false) {
  const now = Date.now();
  const lastLoad = cacheTimestamps.value['snacks'] || 0;
  
  if (!forceReload && snacks.value.length > 0 && (now - lastLoad) < CACHE_DURATION) {
    console.log('Using cached snacks data');
    return;
  }
  
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch(`${API_BASE}/api/snacks?available_only=false`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    snacks.value = data as SnackItem[];
    originalSnacks.value = {};
    snacks.value.forEach(snack => {
      originalSnacks.value[snack.id] = JSON.parse(JSON.stringify(snack));
    });
    cacheTimestamps.value['snacks'] = Date.now();
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load snacks';
  } finally {
    loading.value = false;
  }
}

function invalidateCache() {
  cacheTimestamps.value = {};
  console.log('Cache invalidated - fresh data will be loaded on next request');
}

function addLogEntry(type: string, itemName: string, details: string) {
  const now = new Date();
  const timestamp = now.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  changeLog.value.push({ timestamp, type, itemName, details });
}

function clearLog() {
  if (confirm('Wirklich das gesamte Änderungsprotokoll löschen?')) {
    changeLog.value = [];
  }
}

function markWineAsModified(wine: WineItem) {
  const key = `wine-${wine.id}`;
  unsavedChanges.value[key] = { type: 'wine', data: wine };
}

function markDrinkAsModified(drink: DrinkItem) {
  const key = `drink-${drink.id}`;
  unsavedChanges.value[key] = { type: 'drink', data: drink };
}

function markSnackAsModified(snack: SnackItem) {
  const key = `snack-${snack.id}`;
  unsavedChanges.value[key] = { type: 'snack', data: snack };
}

function isWineModified(id: string | number) {
  return `wine-${id}` in unsavedChanges.value;
}

function isDrinkModified(id: number) {
  return `drink-${id}` in unsavedChanges.value;
}

function isSnackModified(id: number) {
  return `snack-${id}` in unsavedChanges.value;
}

async function saveAllChanges() {
  const changes = Object.entries(unsavedChanges.value);
  if (changes.length === 0) return;
  
  let hasErrors = false;
  for (const [key, change] of changes) {
    try {
      if (change.type === 'wine') {
        await saveWineChanges(change.data);
        originalWines.value[change.data.id] = JSON.parse(JSON.stringify(change.data));
      } else if (change.type === 'drink') {
        await saveDrinkChanges(change.data);
        originalDrinks.value[change.data.id] = JSON.parse(JSON.stringify(change.data));
      } else if (change.type === 'snack') {
        await saveSnackChanges(change.data);
        originalSnacks.value[change.data.id] = JSON.parse(JSON.stringify(change.data));
      }
      delete unsavedChanges.value[key];
    } catch (err) {
      console.error(`Failed to save ${key}:`, err);
      hasErrors = true;
    }
  }
  
  unsavedChanges.value = {};
  invalidateCache();
  
  if (!hasErrors) {
    window.alert('Alle Änderungen gespeichert! Cache wurde aktualisiert.');
  } else {
    window.alert('Einige Änderungen konnten nicht gespeichert werden. Siehe Console für Details.');
  }
}

async function saveWineChanges(wine: WineItem) {
  const originalWine = wines.value.find(w => w.id === wine.id);
  if (!originalWine) return;
  
  const previousPrices = {
    bottle: originalWine.price_bottle,
    glass01: originalWine.price_glass_01,
    glass02: originalWine.price_glass_02
  };
  const previousName = originalWine.name;
  const previousDesc = originalWine.short_description;
  
  const priceChanged = wine.price_bottle !== previousPrices.bottle ||
                       wine.price_glass_01 !== previousPrices.glass01 ||
                       wine.price_glass_02 !== previousPrices.glass02;
  
  const detailsChanged = wine.name !== previousName ||
                         wine.short_description !== previousDesc;
  
  if (priceChanged) {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}/price`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        price_bottle: wine.price_bottle,
        price_glass_01: wine.price_glass_01,
        price_glass_02: wine.price_glass_02
      })
    });
    if (!response.ok) throw new Error('Failed to update wine price');
    
    const details = `Flasche: ${previousPrices.bottle}€→${wine.price_bottle}€, 0.1l: ${previousPrices.glass01}€→${wine.price_glass_01}€, 0.2l: ${previousPrices.glass02}€→${wine.price_glass_02}€`;
    addLogEntry('Wein Preis', wine.name, details);
  }
  
  if (detailsChanged) {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}/details`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: wine.name, short_description: wine.short_description })
    });
    if (!response.ok) throw new Error('Failed to update wine details');
    
    const changes = [];
    if (previousName !== wine.name) changes.push(`Name: ${previousName}→${wine.name}`);
    if (previousDesc !== wine.short_description) changes.push(`Beschreibung geändert`);
    addLogEntry('Wein Details', previousName, changes.join(', '));
  }
}

async function saveDrinkChanges(drink: DrinkItem) {
  const originalDrink = drinks.value.find(d => d.id === drink.id);
  if (!originalDrink) return;
  
  const previousPrice = originalDrink.price;
  if (drink.price !== previousPrice) {
    const response = await fetch(`${API_BASE}/api/drinks/${drink.id}/price`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ price: drink.price })
    });
    if (!response.ok) throw new Error('Failed to update drink price');
    addLogEntry('Getränk Preis', drink.name, `${previousPrice}€ → ${drink.price}€`);
  }
}

async function saveSnackChanges(snack: SnackItem) {
  const originalSnack = snacks.value.find(s => s.id === snack.id);
  if (!originalSnack) return;
  
  const previousPrice = originalSnack.price;
  if (snack.price !== previousPrice) {
    const response = await fetch(`${API_BASE}/api/snacks/${snack.id}/price`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ price: snack.price })
    });
    if (!response.ok) throw new Error('Failed to update snack price');
    addLogEntry('Snack Preis', snack.name, `${previousPrice}€ → ${snack.price}€`);
  }
}

async function toggleWineAvailable(wine: WineItem) {
  const previousAvailable = wine.available;
  const nextStatus = !previousAvailable;
  wine.available = nextStatus;
  
  try {
    const response = await fetch(`${API_BASE}/api/wines/${wine.id}/availability?available=${nextStatus}`, {
      method: 'PATCH'
    });
    if (!response.ok) throw new Error('Failed to update wine');
    addLogEntry('Wein Verfügbarkeit', wine.name, `${previousAvailable ? 'verfügbar' : 'nicht verfügbar'} → ${nextStatus ? 'verfügbar' : 'nicht verfügbar'}`);
    originalWines.value[wine.id] = JSON.parse(JSON.stringify(wine));
    invalidateCache();
  } catch (err) {
    window.alert('Error updating wine');
    wine.available = previousAvailable;
  }
}

async function toggleDrinkAvailable(drink: DrinkItem) {
  const previousAvailable = drink.available;
  const nextStatus = !previousAvailable;
  drink.available = nextStatus;
  
  try {
    const response = await fetch(`${API_BASE}/api/drinks/${drink.id}/availability?available=${nextStatus}`, {
      method: 'PATCH'
    });
    if (!response.ok) throw new Error('Failed to update drink');
    addLogEntry('Getränk Verfügbarkeit', drink.name, `${previousAvailable ? 'verfügbar' : 'nicht verfügbar'} → ${nextStatus ? 'verfügbar' : 'nicht verfügbar'}`);
    originalDrinks.value[drink.id] = JSON.parse(JSON.stringify(drink));
    invalidateCache();
  } catch (err) {
    window.alert('Error updating drink');
    drink.available = previousAvailable;
  }
}

async function toggleSnackAvailable(snack: SnackItem) {
  const previousAvailable = snack.available;
  const nextStatus = !previousAvailable;
  snack.available = nextStatus;
  
  try {
    const response = await fetch(`${API_BASE}/api/snacks/${snack.id}/availability?available=${nextStatus}`, {
      method: 'PATCH'
    });
    if (!response.ok) throw new Error('Failed to update snack');
    addLogEntry('Snack Verfügbarkeit', snack.name, `${previousAvailable ? 'verfügbar' : 'nicht verfügbar'} → ${nextStatus ? 'verfügbar' : 'nicht verfügbar'}`);
    originalSnacks.value[snack.id] = JSON.parse(JSON.stringify(snack));
    invalidateCache();
  } catch (err) {
    window.alert('Error updating snack');
    snack.available = previousAvailable;
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

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.log-header h2 {
  margin: 0;
}

.clear-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.clear-btn:hover {
  background-color: #c82333;
}

.empty-log {
  text-align: center;
  color: #666;
  padding: 2rem;
  font-style: italic;
}

.log-table {
  font-size: 0.9rem;
}

.log-table td {
  vertical-align: top;
}

.log-table td:first-child {
  white-space: nowrap;
  font-family: monospace;
  font-size: 0.85rem;
}

.change-details {
  word-break: break-word;
  max-width: 400px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header h1 {
  margin: 0;
}

.save-all-btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.save-all-btn:hover {
  background-color: #218838;
}

.has-changes {
  background-color: #fff3cd;
  border-left: 3px solid #ffc107;
}

.has-changes input {
  background-color: #fffbef;
}
</style>