<template>
  <div v-if="features.chatbot.enabled" class="chat-toggle">
    <button
      @click="toggleChat"
      class="chat-toggle-button"
      :class="{ 'has-notification': !isOpen && hasNewMessage }"
      aria-label="Wine Chat öffnen"
    >
      <span class="chat-icon">🍷</span>
      <span class="chat-label">Wine Chat</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { features } from '../config/features';
import { useChat } from '../composables/useChat';

const { isOpen, toggleChat, checkChatbotStatus } = useChat();
const hasNewMessage = ref(false);
const isEnabled = ref(false);

onMounted(async () => {
  // Check if chatbot is enabled on the backend
  isEnabled.value = await checkChatbotStatus();
  
  // Override frontend feature flag if backend has it disabled
  if (!isEnabled.value) {
    features.chatbot.enabled = false;
  }
});
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";

.chat-toggle {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chat-toggle-button {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 120px;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(139, 69, 19, 0.4);
    background: linear-gradient(135deg, #a0522d 0%, #8b4513 100%);
  }
  
  &:active {
    transform: translateY(0);
  }
  
  &.has-notification {
    animation: pulse 2s infinite;
    
    &::after {
      content: '';
      position: absolute;
      top: -2px;
      right: -2px;
      width: 12px;
      height: 12px;
      background: #ff4444;
      border-radius: 50%;
      border: 2px solid white;
    }
  }
}

.chat-icon {
  font-size: 18px;
}

.chat-label {
  font-family: 'Great Vibes', cursive;
  font-size: 16px;
}

@keyframes pulse {
  0% {
    box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
  }
  50% {
    box-shadow: 0 4px 12px rgba(139, 69, 19, 0.6);
  }
  100% {
    box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
  }
}

@media (max-width: 768px) {
  .chat-toggle {
    bottom: 15px;
    right: 15px;
  }
  
  .chat-toggle-button {
    padding: 10px 16px;
    min-width: 100px;
    
    .chat-label {
      font-size: 14px;
    }
  }
}
</style>