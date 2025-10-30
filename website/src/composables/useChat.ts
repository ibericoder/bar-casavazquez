import { reactive, toRef } from 'vue';

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
  // Prefer explicit API base from env; otherwise, use 127.0.0.1 to avoid potential localhost/IPv6 stalls in some Windows setups
  const API_BASE = import.meta.env.VITE_API_URL 
    || (typeof window !== 'undefined' ? `http://127.0.0.1:8080` : 'http://127.0.0.1:8080');

  const addMessage = (content: string, isUser: boolean, recommendations?: any[]): ChatMessage => {
    const uniqueId = `${Date.now()}-${Math.random().toString(36).slice(2,8)}`;
    const message: ChatMessage = {
      id: uniqueId,
      content,
      isUser,
      timestamp: new Date(),
      recommendations
    };

    // Use immutable assignment to ensure Vue reactivity detects the update
    chatState.messages = [...chatState.messages, message];
    // Debug log for reactivity issues
  try {
      console.debug('[useChat] addMessage', { id: message.id, isUser, total: chatState.messages.length });
    } catch (e) {
      // ignore when not in browser environment
    }
    return message;
  };

  const sendMessage = async (message: string) => {
    if (!message.trim()) return;

    // Add user message
    addMessage(message, true);
    chatState.isLoading = true;
    chatState.hasError = false;

    try {
      // Add a timeout so the UI never hangs indefinitely if the server is unreachable
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 15000);

      const response = await fetch(`${API_BASE}/api/chat/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          context: {}
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Add bot response
      addMessage(data.response, false, data.recommendations);
      try {
        console.debug('[useChat] sendMessage response', data);
      } catch (e) {}
      
    } catch (error) {
      console.error('Chat error:', error);
      
      // Fallback: try simple GET recommender endpoint to still answer the user
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        const q = encodeURIComponent(message.trim());
        const res = await fetch(`${API_BASE}/api/chat/recommend?message=${q}`, { signal: controller.signal });
        clearTimeout(timeoutId);
        if (res.ok) {
          const rdata = await res.json();
          const explanation = rdata.explanation || 'Ich habe einige Vorschläge für Sie zusammengestellt.';
          addMessage(explanation, false, rdata.recommendations);
          chatState.hasError = false;
          return; // success via fallback
        }
      } catch (e) {
        // ignore and show friendly error below
      }

      chatState.hasError = true;
      const isAbort = (error as any)?.name === 'AbortError';
      const msg = isAbort 
        ? 'Zeitüberschreitung beim Verbinden mit dem Server. Bitte prüfen Sie die Verbindung und versuchen Sie es erneut.'
        : 'Entschuldigung, es gab ein technisches Problem. Bitte versuchen Sie es später nochmal.';
      addMessage(msg, false);
    } finally {
      chatState.isLoading = false;
    }
  };

  const toggleChat = () => {
    chatState.isOpen = !chatState.isOpen;
    
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
      const response = await fetch(`${API_BASE}/health`);
      if (response.ok) {
        return true; // If health endpoint works, assume chatbot is available
      }
      return false;
    } catch (error) {
      console.error('Error checking chatbot status:', error);
      return true; // Default to enabled if we can't check
    }
  };

  return {
    messages: toRef(chatState, 'messages'),
    isLoading: toRef(chatState, 'isLoading'),
    isOpen: toRef(chatState, 'isOpen'),
    hasError: toRef(chatState, 'hasError'),
    
    sendMessage,
    toggleChat,
    clearChat,
    checkChatbotStatus
  };
}
