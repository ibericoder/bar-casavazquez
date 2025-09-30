import { ref, reactive, computed } from 'vue';

interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  recommendations?: any[];
}

interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  isOpen: boolean;
  hasError: boolean;
}

const chatState = reactive<ChatState>({
  messages: [],
  isLoading: false,
  isOpen: false,
  hasError: false
});

export function useChat() {
  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8080';

  const addMessage = (content: string, isUser: boolean, recommendations?: any[]): ChatMessage => {
    const message: ChatMessage = {
      id: Date.now().toString(),
      content,
      isUser,
      timestamp: new Date(),
      recommendations
    };
    
    chatState.messages.push(message);
    return message;
  };

  const sendMessage = async (message: string) => {
    if (!message.trim()) return;

    // Add user message
    addMessage(message, true);
    chatState.isLoading = true;
    chatState.hasError = false;

    try {
      const response = await fetch(`${API_BASE}/api/chat/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          context: {}
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Add bot response
      addMessage(data.response, false, data.recommendations);
      
    } catch (error) {
      console.error('Chat error:', error);
      chatState.hasError = true;
      addMessage(
        'Entschuldigung, es gab ein technisches Problem. Bitte versuchen Sie es später nochmal.',
        false
      );
    } finally {
      chatState.isLoading = false;
    }
  };

  const toggleChat = () => {
    chatState.isOpen = !chatState.isOpen;
    
    // Add welcome message if this is the first time opening
    if (chatState.isOpen && chatState.messages.length === 0) {
      addMessage(
        'Hallo! Ich bin Ihr Weinsommelier-Assistent. Beschreiben Sie mir Ihren Geschmack und ich empfehle Ihnen passende Weine aus unserem Sortiment! 🍷',
        false
      );
    }
  };

  const clearChat = () => {
    chatState.messages = [];
    chatState.hasError = false;
  };

  const checkChatbotStatus = async (): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE}/api/chat/status`);
      const data = await response.json();
      return data.enabled;
    } catch (error) {
      console.error('Error checking chatbot status:', error);
      return false;
    }
  };

  return {
    // State
    messages: chatState.messages,
    isLoading: computed(() => chatState.isLoading),
    isOpen: computed(() => chatState.isOpen),
    hasError: computed(() => chatState.hasError),
    
    // Actions
    sendMessage,
    toggleChat,
    clearChat,
    checkChatbotStatus
  };
}