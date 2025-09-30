<template>
  <div class="admin-panel">
    <header class="admin-header">
      <h1>Casa Vazquez Admin</h1>
      <p>Menu Management Interface</p>
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
        <h2>Wines Management</h2>
        <div class="data-grid">
          <div v-if="winesLoading" class="loading">Loading wines...</div>
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useWineMenu } from './useWineMenu';
import { useDrinksMenu } from '../composables/useDrinksMenu';
import { useSnacksMenu } from '../composables/useSnacksMenu';
import { useNotifications } from '../composables/useNotifications';

const activeTab = ref('wines');

const tabs = [
  { id: 'wines', label: 'Wines' },
  { id: 'drinks', label: 'Drinks' },
  { id: 'snacks', label: 'Snacks' },
  { id: 'notifications', label: 'Notifications' }
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
  await loadVinos();
  await loadDrinks({ available_only: false });
  await loadSnacks({ available_only: false });
  await loadNotifications({ active_only: false });
});

// Wine actions
async function toggleWineAvailability(wine: any) {
  try {
    const apiUrl = import.meta.env.DEV ? 'http://localhost:8080' : 'https://casavazquez-website-594856899017.europe-central2.run.app';
    const response = await fetch(`${apiUrl}/api/wines/${wine.id}/availability?available=${!wine.available}`, {
      method: 'PATCH'
    });
    if (response.ok) {
      wine.available = !wine.available;
    }
  } catch (error) {
    console.error('Error toggling wine availability:', error);
  }
}

function editWine(wine: any) {
  alert(`Edit wine: ${wine.name} (Feature coming soon)`);
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

.admin-header {
  background-color: $accent-color;
  color: white;
  padding: 2rem;
  text-align: center;
  
  h1 {
    margin: 0 0 0.5rem 0;
    font-size: 2.5rem;
    font-family: 'King Red', serif;
  }
  
  p {
    margin: 0;
    opacity: 0.9;
  }
}

.admin-nav {
  background-color: white;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  justify-content: center;
  gap: 1rem;
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
}

.admin-content {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.admin-section {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  
  h2 {
    margin: 0 0 1.5rem 0;
    color: $accent-color;
    font-size: 1.8rem;
  }
}

.data-grid {
  .loading, .error {
    text-align: center;
    padding: 2rem;
    font-size: 1.1rem;
  }
  
  .error {
    color: #e74c3c;
  }
}

.grid-header, .grid-row {
  display: grid;
  grid-template-columns: 80px 200px 120px 120px 120px 120px 200px;
  gap: 1rem;
  padding: 1rem;
  align-items: center;
  border-bottom: 1px solid #eee;
  
  span {
    font-size: 0.9rem;
  }
}

.grid-header {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #495057;
  border-radius: 6px 6px 0 0;
}

.grid-row {
  &:hover {
    background-color: #f8f9fa;
  }
  
  &.inactive {
    opacity: 0.6;
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