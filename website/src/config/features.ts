interface FeatureFlags {
  chatbot: {
    enabled: boolean;
    position: 'bottom-right' | 'bottom-left';
    autoOpen: boolean;
  };
}

export const features: FeatureFlags = {
  chatbot: {
    enabled: true, // Can be controlled via environment variable
    position: 'bottom-right',
    autoOpen: false
  }
};

// Check if feature is enabled via environment variable
if (import.meta.env.VITE_ENABLE_CHATBOT === 'false') {
  features.chatbot.enabled = false;
}