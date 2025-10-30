import { ref, computed } from 'vue';

interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  role: string;
  is_active: boolean;
}

// Global auth state
const token = ref<string | null>(localStorage.getItem('admin_token'));
const user = ref<User | null>(
  localStorage.getItem('admin_user') 
    ? JSON.parse(localStorage.getItem('admin_user')!) 
    : null
);

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value);
  const isAdmin = computed(() => user.value?.role === 'admin');
  const isManager = computed(() => user.value?.role === 'manager' || isAdmin.value);

  const login = (newToken: string, newUser: User) => {
    token.value = newToken;
    user.value = newUser;
    localStorage.setItem('admin_token', newToken);
    localStorage.setItem('admin_user', JSON.stringify(newUser));
  };

  const logout = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_user');
  };

  const getAuthHeaders = () => {
    if (!token.value) return {};
    return {
      'Authorization': `Bearer ${token.value}`
    };
  };

  const getApiUrl = () => {
    if (import.meta.env.DEV || window.location.hostname === 'localhost') {
      return 'http://localhost:8080';
    }
    return 'https://casavazquez-website-594856899017.europe-central2.run.app';
  };

  const authenticatedFetch = async (url: string, options: RequestInit = {}) => {
    const headers = Object.fromEntries(
      Object.entries({
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
        ...(options.headers || {})
      }).filter(([_, v]) => v !== undefined)
    );

    const response = await fetch(url, {
      ...options,
      headers
    });

    if (response.status === 401) {
      // Token expired or invalid
      logout();
      throw new Error('Authentication expired. Please log in again.');
    }

    return response;
  };

  const verifyToken = async () => {
    if (!token.value) return false;

    try {
      const response = await authenticatedFetch(`${getApiUrl()}/api/auth/me`);
      if (response.ok) {
        const userData = await response.json();
        user.value = userData;
        return true;
      } else {
        logout();
        return false;
      }
    } catch (error) {
      logout();
      return false;
    }
  };

  return {
    token: computed(() => token.value),
    user: computed(() => user.value),
    isAuthenticated,
    isAdmin,
    isManager,
    login,
    logout,
    getAuthHeaders,
    authenticatedFetch,
    verifyToken,
    getApiUrl
  };
}
