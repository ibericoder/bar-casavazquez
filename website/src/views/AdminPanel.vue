<template>
  <div class="admin-panel">
    <!-- Login Modal -->
    <LoginModal 
      :show="showLogin" 
      @close="showLogin = false"
      @login-success="handleLoginSuccess"
    />

    <!-- Not Authenticated View -->
    <div v-if="!isAuthenticated" class="auth-required">
      <div class="auth-message">
        <h1>Admin-Zugang erforderlich</h1>
        <p>Bitte melden Sie sich an, um das Admin-Panel zu verwenden.</p>
        <button @click="showLogin = true" class="login-trigger-btn">
          Anmelden
        </button>
      </div>
    </div>

    <!-- Authenticated Admin Panel -->
    <div v-else>
      <header class="admin-header">
        <div class="header-content">
          <div>
            <h1>Casa Vazquez Admin</h1>
            <p>Menü-Verwaltung</p>
          </div>
          <div class="user-info">
            <span>Willkommen, {{ user?.full_name || user?.username }}</span>
            <button @click="handleLogout" class="logout-btn">Abmelden</button>
          </div>
        </div>
      </header>

    <nav class="admin-nav">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['nav-btn', { active: activeTab === tab.id }]"
      >
        {{ tab.label }}
      </button>
    </nav>

    <main class="admin-content">
      <!-- Wines Management -->
      <section v-if="activeTab === 'wines'" class="admin-section">
        <h2>Weine Verwaltung</h2>
        <div class="data-grid">
          <div v-if="winesLoading" class="loading">Lade Weine...</div>
          <div v-else-if="winesError" class="error">{{ winesError }}</div>
          <div v-else>
            <div class="grid-header">
              <span>ID</span>
              <span>Name</span>
              <span>Color</span>
              <span>Price (Bottle)</span>
              <span>Available</span>
              <span>Actions</span>
            </div>
            <div 
              v-for="wine in wines" 
              :key="wine.id" 
              class="grid-row"
              :class="{ inactive: !wine.available }"
            >
              <span>{{ wine.id }}</span>
              <span>{{ wine.name }}</span>
              <span>{{ wine.color }}</span>
              <span>{{ wine.prices?.flasche || 'N/A' }}</span>
              <span>
                <button 
                  @click="toggleWineAvailability(wine)"
                  :class="['toggle-btn', wine.available ? 'active' : 'inactive']"
                >
                  {{ wine.available ? 'Available' : 'Unavailable' }}
                </button>
              </span>
              <span>
                <button @click="editWine(wine)" class="action-btn edit">Edit</button>
                <button @click="deleteWine(wine)" class="action-btn delete">Delete</button>
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Edit Wine Modal -->
      <div v-if="isEditingWine" class="modal-backdrop">
        <div class="modal">
          <h3>Wein bearbeiten</h3>
          <div class="form-grid">
            <label>
              Name
              <input v-model="editForm.name" type="text" />
            </label>
            <label>
              Farbe
              <select v-model="editForm.color">
                <option value="red">Rot</option>
                <option value="white">Weiß</option>
                <option value="rosé">Rosé</option>
              </select>
            </label>
            <label>
              Traube
              <input v-model="editForm.grape" type="text" />
            </label>
            <label>
              Herkunft
              <input v-model="editForm.origin" type="text" />
            </label>
          </div>

          <h4>Preise</h4>
          <div class="prices-grid">
            <label>
              0.1l
              <input v-model="editForm.prices['0.1l']" type="text" placeholder="z.B. 4,00€" />
            </label>
            <label>
              0.2l
              <input v-model="editForm.prices['0.2l']" type="text" placeholder="z.B. 7,50€" />
            </label>
            <label>
              0.25l
              <input v-model="editForm.prices['0.25l']" type="text" />
            </label>
            <label>
              Glas
              <input v-model="editForm.prices['glas']" type="text" />
            </label>
            <label>
              Flasche
              <input v-model="editForm.prices['flasche']" type="text" placeholder="z.B. 25,00€" />
            </label>
          </div>

          <div v-if="otherPriceKeys.length" class="other-prices">
            <h5>Weitere Preisfelder</h5>
            <div class="prices-grid">
              <label v-for="k in otherPriceKeys" :key="k">
                {{ k }}
                <input v-model="editForm.prices[k]" type="text" />
              </label>
            </div>
          </div>

          <div class="modal-actions">
            <button class="action-btn save" @click="saveWine">Speichern</button>
            <button class="action-btn cancel" @click="closeEdit">Abbrechen</button>
          </div>
        </div>
      </div>

      <!-- Drinks Management -->
      <section v-if="activeTab === 'drinks'" class="admin-section">
        <h2>Drinks Management</h2>
        <div class="data-grid">
          <div v-if="drinksLoading" class="loading">Loading drinks...</div>
          <div v-else-if="drinksError" class="error">{{ drinksError }}</div>
          <div v-else>
            <div class="grid-header">
              <span>ID</span>
              <span>Name</span>
              <span>Category</span>
              <span>Price</span>
              <span>Alcoholic</span>
              <span>Available</span>
              <span>Actions</span>
            </div>
            <div 
              v-for="drink in drinks" 
              :key="drink.id" 
              class="grid-row"
              :class="{ inactive: !drink.available }"
            >
              <span>{{ drink.id }}</span>
              <span>{{ drink.name }}</span>
              <span>{{ drink.category }}</span>
              <span>{{ drink.price }}</span>
              <span>{{ drink.alcoholic ? 'Yes' : 'No' }}</span>
              <span>
                <button 
                  @click="toggleDrinkAvailability(drink)"
                  :class="['toggle-btn', drink.available ? 'active' : 'inactive']"
                >
                  {{ drink.available ? 'Available' : 'Unavailable' }}
                </button>
              </span>
              <span>
                <button @click="editDrink(drink)" class="action-btn edit">Edit</button>
                <button @click="deleteDrink(drink)" class="action-btn delete">Delete</button>
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Snacks Management -->
      <section v-if="activeTab === 'snacks'" class="admin-section">
        <h2>Snacks Management</h2>
        <div class="data-grid">
          <div v-if="snacksLoading" class="loading">Loading snacks...</div>
          <div v-else-if="snacksError" class="error">{{ snacksError }}</div>
          <div v-else>
            <div class="grid-header">
              <span>ID</span>
              <span>Name</span>
              <span>Category</span>
              <span>Price</span>
              <span>Diet</span>
              <span>Available</span>
              <span>Actions</span>
            </div>
            <div 
              v-for="snack in snacks" 
              :key="snack.id" 
              class="grid-row"
              :class="{ inactive: !snack.available }"
            >
              <span>{{ snack.id }}</span>
              <span>{{ snack.name }}</span>
              <span>{{ snack.category }}</span>
              <span>{{ snack.price }}</span>
              <span>
                <span v-if="snack.vegan" class="diet-tag vegan">Vegan</span>
                <span v-else-if="snack.vegetarian" class="diet-tag vegetarian">Vegetarian</span>
                <span v-else class="diet-tag">Regular</span>
              </span>
              <span>
                <button 
                  @click="toggleSnackAvailability(snack)"
                  :class="['toggle-btn', snack.available ? 'active' : 'inactive']"
                >
                  {{ snack.available ? 'Available' : 'Unavailable' }}
                </button>
              </span>
              <span>
                <button @click="editSnack(snack)" class="action-btn edit">Edit</button>
                <button @click="deleteSnack(snack)" class="action-btn delete">Delete</button>
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Notifications Management -->
      <section v-if="activeTab === 'notifications'" class="admin-section">
        <h2>Notifications Management</h2>
        <div class="data-grid">
          <div v-if="notificationsLoading" class="loading">Loading notifications...</div>
          <div v-else-if="notificationsError" class="error">{{ notificationsError }}</div>
          <div v-else>
            <div class="grid-header">
              <span>ID</span>
              <span>Title</span>
              <span>Type</span>
              <span>Target Page</span>
              <span>Priority</span>
              <span>Active</span>
              <span>Actions</span>
            </div>
            <div 
              v-for="notification in notifications" 
              :key="notification.id" 
              class="grid-row"
              :class="{ inactive: !notification.active }"
            >
              <span>{{ notification.id }}</span>
              <span>{{ notification.title }}</span>
              <span>{{ notification.type }}</span>
              <span>{{ notification.target_page || 'All' }}</span>
              <span>{{ notification.priority }}</span>
              <span>
                <button 
                  @click="toggleNotificationStatus(notification)"
                  :class="['toggle-btn', notification.active ? 'active' : 'inactive']"
                >
                  {{ notification.active ? 'Active' : 'Inactive' }}
                </button>
              </span>
              <span>
                <button @click="editNotification(notification)" class="action-btn edit">Edit</button>
                <button @click="deleteNotification(notification)" class="action-btn delete">Delete</button>
              </span>
            </div>
          </div>
        </div>
      </section>
    </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useWineMenu } from './useWineMenu';
import { useDrinksMenu } from '../composables/useDrinksMenu';
import { useSnacksMenu } from '../composables/useSnacksMenu';
import { useNotifications } from '../composables/useNotifications';
import { useAuth } from '../composables/useAuth';
import LoginModal from '../components/LoginModal.vue';

const { isAuthenticated, user, login, logout, authenticatedFetch, getApiUrl } = useAuth();

const showLogin = ref(false);
const activeTab = ref('wines');

const tabs = [
  { id: 'wines', label: 'Weine' },
  { id: 'drinks', label: 'Getränke' },
  { id: 'snacks', label: 'Snacks' },
  { id: 'notifications', label: 'Benachrichtigungen' }
];

// Wines
const { vinos: wines, loading: winesLoading, error: winesError, loadVinos } = useWineMenu();

// Drinks
const { drinks, loading: drinksLoading, error: drinksError, loadDrinks } = useDrinksMenu();

// Snacks
const { snacks, loading: snacksLoading, error: snacksError, loadSnacks } = useSnacksMenu();

// Notifications
const { notifications, loading: notificationsLoading, error: notificationsError, loadNotifications } = useNotifications();

onMounted(async () => {
  if (isAuthenticated.value) {
    await loadMenuData();
  }
});

// Authentication functions
const handleLoginSuccess = (token: string, userData: any) => {
  login(token, userData);
  loadMenuData();
};

const handleLogout = () => {
  logout();
  showLogin.value = false;
};

// Load all menu data
const loadMenuData = async () => {
  await loadVinos();
  await loadDrinks({ available_only: false });
  await loadSnacks({ available_only: false });
  await loadNotifications({ active_only: false });
};

// Wine actions
const isEditingWine = ref(false);
const editForm = ref<any | null>(null);

async function toggleWineAvailability(wine: any) {
  try {
    const response = await authenticatedFetch(`${getApiUrl()}/api/wines/${wine.id}/availability?available=${!wine.available}`, {
      method: 'PATCH'
    });
    if (response.ok) {
      wine.available = !wine.available;
    } else {
      throw new Error('Failed to update wine availability');
    }
  } catch (error) {
    console.error('Error toggling wine availability:', error);
    alert('Failed to update wine availability. Please try again.');
  }
}

function editWine(wine: any) {
  isEditingWine.value = true;
  editForm.value = {
    id: wine.id,
    name: wine.name,
    color: wine.color,
    grape: wine.grape,
    origin: wine.origin || '',
    short_description: wine.short_description || '',
    long_description: wine.long_description || '',
    characteristics: wine.characteristics || '',
    available: !!wine.available,
    prices: { ...(wine.prices || {}) }
  };
}

function closeEdit() {
  isEditingWine.value = false;
  editForm.value = null;
}

const commonPriceKeys = ['0.1l','0.2l','0.25l','glas','flasche'];
const otherPriceKeys = computed(() => {
  if (!editForm.value?.prices) return [] as string[];
  return Object.keys(editForm.value.prices).filter(k => !commonPriceKeys.includes(k));
});

async function saveWine() {
  if (!editForm.value) return;
  try {
    const payload: any = {
      name: editForm.value.name,
      color: editForm.value.color,
      grape: editForm.value.grape,
      origin: editForm.value.origin,
      short_description: editForm.value.short_description,
      long_description: editForm.value.long_description,
      characteristics: editForm.value.characteristics,
      available: editForm.value.available,
      prices: editForm.value.prices || {}
    };
    const res = await authenticatedFetch(`${getApiUrl()}/api/wines/${editForm.value.id}`, {
      method: 'PUT',
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    // Update list locally
    const updated = await res.json();
    const idx = wines.value.findIndex(w => w.id === updated.id);
    if (idx >= 0) {
      wines.value[idx] = { ...wines.value[idx], ...updated } as any;
    }
    closeEdit();
  } catch (e) {
    console.error('Failed to save wine', e);
    alert('Speichern fehlgeschlagen.');
  }
}

function deleteWine(wine: any) {
  if (confirm(`Delete wine: ${wine.name}?`)) {
    alert('Delete feature coming soon');
  }
}

// Drink actions
async function toggleDrinkAvailability(drink: any) {
  try {
    const apiUrl = import.meta.env.DEV ? 'http://localhost:8080' : 'https://casavazquez-website-594856899017.europe-central2.run.app';
    const response = await fetch(`${apiUrl}/api/drinks/${drink.id}/availability?available=${!drink.available}`, {
      method: 'PATCH'
    });
    if (response.ok) {
      drink.available = !drink.available;
    }
  } catch (error) {
    console.error('Error toggling drink availability:', error);
  }
}

function editDrink(drink: any) {
  alert(`Edit drink: ${drink.name} (Feature coming soon)`);
}

function deleteDrink(drink: any) {
  if (confirm(`Delete drink: ${drink.name}?`)) {
    alert('Delete feature coming soon');
  }
}

// Snack actions
async function toggleSnackAvailability(snack: any) {
  try {
    const apiUrl = import.meta.env.DEV ? 'http://localhost:8080' : 'https://casavazquez-website-594856899017.europe-central2.run.app';
    const response = await fetch(`${apiUrl}/api/snacks/${snack.id}/availability?available=${!snack.available}`, {
      method: 'PATCH'
    });
    if (response.ok) {
      snack.available = !snack.available;
    }
  } catch (error) {
    console.error('Error toggling snack availability:', error);
  }
}

function editSnack(snack: any) {
  alert(`Edit snack: ${snack.name} (Feature coming soon)`);
}

function deleteSnack(snack: any) {
  if (confirm(`Delete snack: ${snack.name}?`)) {
    alert('Delete feature coming soon');
  }
}

// Notification actions
async function toggleNotificationStatus(notification: any) {
  try {
    const apiUrl = import.meta.env.DEV ? 'http://localhost:8080' : 'https://casavazquez-website-594856899017.europe-central2.run.app';
    const response = await fetch(`${apiUrl}/api/notifications/${notification.id}/status?active=${!notification.active}`, {
      method: 'PATCH'
    });
    if (response.ok) {
      notification.active = !notification.active;
    }
  } catch (error) {
    console.error('Error toggling notification status:', error);
  }
}

function editNotification(notification: any) {
  alert(`Edit notification: ${notification.title} (Feature coming soon)`);
}

function deleteNotification(notification: any) {
  if (confirm(`Delete notification: ${notification.title}?`)) {
    alert('Delete feature coming soon');
  }
}
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";

.admin-panel {
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: $font-family;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.modal {
  width: 680px;
  max-width: 95vw;
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 12px 36px rgba(0,0,0,0.2);
}
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
  label { display: flex; flex-direction: column; gap: 6px; font-size: 14px; }
  input, select { padding: 8px; border: 1px solid #ddd; border-radius: 6px; }
}
.prices-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 12px;
  label { display: flex; flex-direction: column; gap: 6px; font-size: 14px; }
  input { padding: 8px; border: 1px solid #ddd; border-radius: 6px; }
}
.modal-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
.action-btn.save { background: #2e7d32; color: #fff; }
.action-btn.cancel { background: #9e9e9e; color: #fff; }

.admin-header {
  background-color: $accent-color;
  color: white;
  padding: 1rem;
  
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1400px;
    margin: 0 auto;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  h1 {
    margin: 0 0 0.5rem 0;
    font-size: 2rem;
    font-family: 'King Red', serif;
    
    @media (max-width: 768px) {
      font-size: 1.5rem;
    }
  }
  
  p {
    margin: 0;
    opacity: 0.9;
    font-size: 0.9rem;
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  
  span {
    font-size: 0.9rem;
    opacity: 0.9;
    
    @media (max-width: 480px) {
      font-size: 0.8rem;
    }
  }
}

.logout-btn {
  padding: 0.5rem 1rem;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.3);
  }
  
  @media (max-width: 480px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
}

.auth-required {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}

.auth-message {
  text-align: center;
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  max-width: 400px;
  
  h1 {
    color: $accent-color;
    font-family: 'King Red', serif;
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  
  p {
    color: #666;
    margin-bottom: 2rem;
    font-size: 1.1rem;
  }
}

.login-trigger-btn {
  padding: 1rem 2rem;
  background-color: $accent-color;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  
  &:hover {
    background-color: darken($accent-color, 10%);
  }
}

.admin-nav {
  background-color: white;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  
  @media (max-width: 768px) {
    padding: 0.5rem;
    gap: 0.25rem;
  }
}

.nav-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid $accent-color;
  background-color: white;
  color: $accent-color;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  
  &:hover, &.active {
    background-color: $accent-color;
    color: white;
  }
  
  @media (max-width: 768px) {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
}

.admin-content {
  padding: 1rem;
  max-width: 1400px;
  margin: 0 auto;
  
  @media (max-width: 768px) {
    padding: 0.5rem;
  }
}

.admin-section {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  
  h2 {
    margin: 0 0 1.5rem 0;
    color: $accent-color;
    font-size: 1.8rem;
  }
  
  @media (max-width: 768px) {
    padding: 1rem;
    
    h2 {
      font-size: 1.4rem;
      margin-bottom: 1rem;
    }
  }
}

.data-grid {
  .loading, .error {
    text-align: center;
    padding: 2rem;
    font-size: 1.1rem;
    
    @media (max-width: 768px) {
      padding: 1rem;
      font-size: 1rem;
    }
  }
  
  .error {
    color: #e74c3c;
  }
}

.grid-header, .grid-row {
  display: grid;
  grid-template-columns: 60px 1fr 100px 100px 100px 120px 140px;
  gap: 0.5rem;
  padding: 1rem;
  align-items: center;
  border-bottom: 1px solid #eee;
  
  span {
    font-size: 0.9rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  @media (max-width: 1024px) {
    grid-template-columns: 50px 1fr 80px 100px 120px;
    gap: 0.25rem;
    padding: 0.75rem 0.5rem;
    
    span:nth-child(4), span:nth-child(5) {
      display: none;
    }
  }
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr auto;
    gap: 0.5rem;
    padding: 1rem 0.5rem;
    
    span:nth-child(1), span:nth-child(3), span:nth-child(4), span:nth-child(5) {
      display: none;
    }
  }
  
  @media (max-width: 480px) {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
    padding: 1rem;
    
    span {
      white-space: normal;
      word-wrap: break-word;
    }
  }
}

.grid-header {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #495057;
  border-radius: 6px 6px 0 0;
  
  @media (max-width: 768px) {
    span:nth-child(2)::before {
      content: "Name";
      font-weight: bold;
      display: block;
    }
    span:nth-child(6)::before {
      content: "Status";
      font-weight: bold;
      display: block;
    }
    span:nth-child(7)::before {
      content: "Actions";
      font-weight: bold;
      display: block;
    }
  }
  
  @media (max-width: 480px) {
    display: none;
  }
}

.grid-row {
  &:hover {
    background-color: #f8f9fa;
  }
  
  &.inactive {
    opacity: 0.6;
  }
  
  @media (max-width: 480px) {
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 1rem;
    background: white;
    
    span {
      padding: 0.25rem 0;
    }
    
    span:nth-child(2) {
      font-weight: bold;
      font-size: 1rem;
      color: $accent-color;
    }
  }
}

.toggle-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 500;
  
  &.active {
    background-color: #28a745;
    color: white;
  }
  
  &.inactive {
    background-color: #dc3545;
    color: white;
  }
  
  @media (max-width: 768px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.75rem;
  }
  
  @media (max-width: 480px) {
    width: 100%;
    margin-bottom: 0.5rem;
  }
}

.action-btn {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  margin-right: 0.5rem;
  
  &.edit {
    background-color: #007bff;
    color: white;
  }
  
  &.delete {
    background-color: #dc3545;
    color: white;
  }
  
  &:hover {
    opacity: 0.8;
  }
  
  @media (max-width: 768px) {
    padding: 0.3rem 0.6rem;
    font-size: 0.75rem;
    margin-right: 0.25rem;
  }
  
  @media (max-width: 480px) {
    width: calc(50% - 0.25rem);
    margin: 0.25rem 0.25rem 0.25rem 0;
    
    &:nth-child(even) {
      margin-right: 0;
    }
  }
}

.diet-tag {
  padding: 0.3rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  
  &.vegan {
    background-color: #28a745;
    color: white;
  }
  
  &.vegetarian {
    background-color: #ffc107;
    color: #212529;
  }
}
</style>