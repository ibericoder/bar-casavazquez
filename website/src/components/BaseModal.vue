<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="modelValue" class="modal-overlay" @click.self="close">
        <div class="modal-content">
          <slot />
          <button class="modal-close" @click="close">×</button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

defineProps<{ modelValue: boolean }>()

const emit = defineEmits<{ (e: 'update:modelValue', value: boolean): void }>()

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped>
@import "../assets/styles/main.scss";

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(100, 100, 100, 0.26);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
  color: black;
}

.modal-content {
  background: #221d32;
  border-radius: 0.5rem;
  max-width: 500px;
  width: 100%;
  padding: 1rem;
  position: relative;
  font-size: 80%;
  color: wheat;
  border: 1px solid wheat;
}

.modal-close {
  position: absolute;
  top: 0.5rem;
  right: 0.75rem;
  font-size: 1.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.5s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
