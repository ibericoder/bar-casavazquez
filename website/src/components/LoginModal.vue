<template>
  <div v-if="show" class="login-modal-overlay" @click="closeModal">
    <div class="login-modal" @click.stop>
      <div class="login-header">
        <h2>Admin Login</h2>
        <button @click="closeModal" class="close-btn">&times;</button>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="loginData.username"
            type="text"
            required
            :disabled="loading"
            placeholder="Enter username"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="loginData.password"
            type="password"
            required
            :disabled="loading"
            placeholder="Enter password"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" :disabled="loading" class="login-btn">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      
      <div class="login-info">
        <p><strong>Development Credentials:</strong></p>
        <p>Username: <code>admin</code></p>
        <p>Password: <code>admin</code></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

interface LoginData {
  username: string;
  password: string;
}

interface Props {
  show: boolean;
}

interface Emits {
  (e: 'close'): void;
  (e: 'login-success', token: string, user: any): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const loginData = ref<LoginData>({
  username: '',
  password: ''
});

const loading = ref(false);
const error = ref('');

// Reset form when modal opens/closes
watch(() => props.show, (newValue) => {
  if (newValue) {
    loginData.value = { username: '', password: '' };
    error.value = '';
  }
});

const closeModal = () => {
  emit('close');
};

const getApiUrl = () => {
  if (import.meta.env.DEV || window.location.hostname === 'localhost') {
    return 'http://localhost:8080';
  }
  return 'https://casavazquez-website-594856899017.europe-central2.run.app';
};

const handleLogin = async () => {
  if (!loginData.value.username || !loginData.value.password) {
    error.value = 'Please fill in all fields';
    return;
  }
  
  loading.value = true;
  error.value = '';
  
  try {
    const response = await fetch(`${getApiUrl()}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginData.value),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Login failed');
    }
    
    const tokenData = await response.json();
    
    // Store token in localStorage
    localStorage.setItem('admin_token', tokenData.access_token);
    localStorage.setItem('admin_user', JSON.stringify(tokenData.user));
    
    emit('login-success', tokenData.access_token, tokenData.user);
    closeModal();
    
  } catch (err: any) {
    error.value = err.message || 'Login failed';
  } finally {
    loading.value = false;
  }
};
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";

.login-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.login-modal {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  animation: modalAppear 0.3s ease-out;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.login-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  
  h2 {
    margin: 0;
    color: $accent-color;
    font-family: 'King Red', serif;
    font-size: 1.8rem;
  }
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #999;
  cursor: pointer;
  line-height: 1;
  
  &:hover {
    color: #666;
  }
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #333;
  }
  
  input {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.2s ease;
    
    &:focus {
      outline: none;
      border-color: $accent-color;
    }
    
    &:disabled {
      background-color: #f5f5f5;
      cursor: not-allowed;
    }
  }
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  border: 1px solid #fcc;
  font-size: 0.9rem;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: $accent-color;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  
  &:hover:not(:disabled) {
    background-color: darken($accent-color, 10%);
  }
  
  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
}

.login-info {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  border-left: 4px solid $accent-color;
  
  p {
    margin: 0.25rem 0;
    font-size: 0.9rem;
    
    &:first-child {
      font-weight: 500;
      margin-bottom: 0.5rem;
    }
  }
  
  code {
    background-color: #e9ecef;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
  }
}
</style>