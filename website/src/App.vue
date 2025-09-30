<template>
  <div class="app-container">
    <router-view/>
    <NavigationBar/>
    
    <!-- Chat Components -->
    <ChatToggle />
    <ChatBot />
  </div>
</template>

<script setup lang="ts">
import NavigationBar from './components/NavigationBar.vue';
import ChatToggle from './components/ChatToggle.vue';
import ChatBot from './components/ChatBot.vue';

</script>
<style scoped>
</style>