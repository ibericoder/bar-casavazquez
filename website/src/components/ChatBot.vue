<template>
  <div v-if="features.chatbot.enabled && isOpen" class="chat-bot">
    <div class="chat-header">
      <div class="chat-title">
        <span class="wine-icon">🍷</span>
        <span>Wine Sommelier</span>
      </div>
      <div class="chat-actions">
        <button @click="clearChat" class="clear-button" title="Chat löschen">🗑️</button>
        <button @click="toggleChat" class="close-button" title="Schließen">✕</button>
      </div>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="message in messages"
        :key="message.id"
        class="message"
        :class="{ 'user-message': message.isUser, 'bot-message': !message.isUser }"
      >
        <div class="message-content">
          <div class="message-text" v-html="formatMessage(message.content)"></div>
          
          <!-- Wine Recommendations -->
          <div v-if="message.recommendations && message.recommendations.length > 0" class="recommendations">
            <h4>🍷 Meine Empfehlungen:</h4>
            <div
              v-for="rec in message.recommendations"
              :key="rec.wine.id"
              class="recommendation-card"
            >
              <div class="wine-info">
                <h5>{{ rec.wine.name }}</h5>
                <p class="wine-description">{{ rec.wine.description }}</p>
                <div class="wine-details">
                  <span class="price">{{ rec.wine.price }}€</span>
                  <span class="color-badge" :class="rec.wine.color">{{ getColorLabel(rec.wine.color) }}</span>
                </div>
                <div v-if="rec.reasons && rec.reasons.length > 0" class="reasons">
                  <p><strong>Warum dieser Wein:</strong></p>
                  <ul>
                    <li v-for="reason in rec.reasons.slice(0, 2)" :key="reason">{{ reason }}</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="message-timestamp">
          {{ formatTime(message.timestamp) }}
        </div>
      </div>
      
      <div v-if="isLoading" class="message bot-message">
        <div class="message-content">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="chat-input">
      <form @submit.prevent="handleSendMessage">
        <input
          v-model="currentMessage"
          type="text"
          placeholder="Beschreiben Sie Ihren Geschmack..."
          :disabled="isLoading"
          class="message-input"
        />
        <button
          type="submit"
          :disabled="!currentMessage.trim() || isLoading"
          class="send-button"
        >
          <span v-if="!isLoading">📤</span>
          <span v-else>⏳</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue';
import { features } from '../config/features';
import { useChat } from '../composables/useChat';

const { messages, isLoading, isOpen, toggleChat, sendMessage, clearChat } = useChat();

const currentMessage = ref('');
const messagesContainer = ref<HTMLElement>();

const handleSendMessage = async () => {
  if (!currentMessage.value.trim()) return;
  
  const message = currentMessage.value;
  currentMessage.value = '';
  
  await sendMessage(message);
  scrollToBottom();
};

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const formatMessage = (content: string): string => {
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
    .replace(/🍷/g, '<span class="wine-emoji">🍷</span>');
};

const formatTime = (timestamp: Date): string => {
  return timestamp.toLocaleTimeString('de-DE', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

const getColorLabel = (color: string): string => {
  const labels = {
    'red': 'Rotwein',
    'white': 'Weißwein',
    'rose': 'Rosé'
  };
  return labels[color as keyof typeof labels] || color;
};

// Auto-scroll when new messages arrive
watch(() => messages.length, () => {
  scrollToBottom();
});
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";

.chat-bot {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  z-index: 1001;
  overflow: hidden;
  border: 1px solid #e0e0e0;
}

.chat-header {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  font-size: 16px;
}

.wine-icon {
  font-size: 20px;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.clear-button, .close-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
}

.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 85%;
  
  &.user-message {
    align-self: flex-end;
    
    .message-content {
      background: #8b4513;
      color: white;
      border-radius: 18px 18px 4px 18px;
    }
  }
  
  &.bot-message {
    align-self: flex-start;
    
    .message-content {
      background: #f5f5f5;
      color: #333;
      border-radius: 18px 18px 18px 4px;
    }
  }
}

.message-content {
  padding: 12px 16px;
  word-wrap: break-word;
}

.message-text {
  line-height: 1.4;
}

.message-timestamp {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
  text-align: right;
  
  .user-message & {
    text-align: left;
  }
}

.recommendations {
  margin-top: 16px;
  
  h4 {
    margin: 0 0 12px 0;
    color: #8b4513;
    font-size: 14px;
  }
}

.recommendation-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
  
  h5 {
    margin: 0 0 8px 0;
    color: #8b4513;
    font-size: 14px;
    font-weight: bold;
  }
  
  .wine-description {
    font-size: 12px;
    color: #666;
    margin: 0 0 8px 0;
    line-height: 1.3;
  }
  
  .wine-details {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  
  .price {
    font-weight: bold;
    color: #8b4513;
    font-size: 14px;
  }
  
  .color-badge {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 12px;
    color: white;
    
    &.red {
      background: #722f37;
    }
    
    &.white {
      background: #daa520;
      color: #333;
    }
    
    &.rose {
      background: #d4526e;
    }
  }
  
  .reasons {
    font-size: 11px;
    
    p {
      margin: 0 0 4px 0;
      font-weight: bold;
    }
    
    ul {
      margin: 0;
      padding-left: 16px;
      
      li {
        margin-bottom: 2px;
      }
    }
  }
}

.typing-indicator {
  display: flex;
  gap: 4px;
  
  span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #8b4513;
    animation: typing 1.4s infinite ease-in-out;
    
    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
  }
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  
  form {
    display: flex;
    gap: 8px;
  }
  
  .message-input {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 20px;
    outline: none;
    font-size: 14px;
    
    &:focus {
      border-color: #8b4513;
    }
    
    &:disabled {
      background: #f5f5f5;
      cursor: not-allowed;
    }
  }
  
  .send-button {
    background: #8b4513;
    color: white;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
    
    &:hover:not(:disabled) {
      background: #a0522d;
    }
    
    &:disabled {
      background: #ccc;
      cursor: not-allowed;
    }
  }
}

.wine-emoji {
  color: #8b4513;
}

@media (max-width: 768px) {
  .chat-bot {
    bottom: 70px;
    right: 15px;
    left: 15px;
    width: auto;
    height: 450px;
  }
  
  .recommendation-card {
    .wine-details {
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;
    }
  }
}
</style>