<template>
  <div  v-if="wine.available"  class="wine-item card" @click="toggle">
    <!-- Zusammengeklappte Ansicht -->
    <div class="collapsed-view">
      <img :src="wine.image ? wine.image : defaultImage" alt="Weinbild" class="wine-image"/>
      <div class="wine-summary">
  <h2>{{ wine.name }}</h2>
  <p v-if="Object.keys(wine.prices).length === 1 && wine.prices.flasche" class="bottle-only-hint">Nur als Flasche</p>
        <p class="characteristics" v-if="wine.characteristics">
          {{ wine.characteristics }}
        </p>
        <p class="grape"> {{ wine.grape }}</p>
        <div class="prices">
          <p class="price" v-if="wine.prices['0.1l']">
            <strong>0,1l:</strong> {{ wine.prices['0.1l'] }}
          </p>
          <p class="price" v-if="wine.prices['0.2l']">
            <strong>0,2l:</strong> {{ wine.prices['0.2l'] }}
          </p>
          <p class="price">
            <strong>Flasche:</strong> {{ wine.prices.flasche }}
          </p>
        </div>
      </div>
    </div>
    <div class="accordion-toggle">
      <i :class="{'pi': true, 'pi-chevron-down': !isOpen, 'pi-chevron-up': isOpen}"/>
    </div>

    <!-- Ausgeklappte Ansicht -->
    <transition name="accordion">
      <div class="expanded-view" v-if="isOpen">
        <p v-if="wine.origin"><strong>Herkunft:</strong> {{ wine.origin }}</p>
        <p v-if="wine.short_description"><strong>Beschreibung:</strong> {{ wine.short_description }}</p>
        <p v-if="wine.long_description">{{ wine.long_description }}</p>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import type {Wine} from '../interfaces/vino';
import 'primeicons/primeicons.css';

const {wine} = defineProps<{ wine: Wine }>();

const isOpen = ref(false);
const defaultImage =
    wine.color === 'white'
        ? new URL('../assets/images/default_vino_white.png', import.meta.url).href
        : wine.color === 'red'
            ? new URL('../assets/images/default_vino_red.png', import.meta.url).href
            : new URL('../assets/images/default_vino_rose.png', import.meta.url).href

function toggle() {
  isOpen.value = !isOpen.value;
}
</script>

<style scoped lang="scss">
@import "../assets/styles/main.scss";

.bottle-only-hint {
  color: $accent-color;
  font-size: 0.85em;
  margin-bottom: 0.2em;
}

strong {
  color: $accent-color;
}

.wine-item {
  position: relative;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
  padding-bottom: 2.5rem;
  color: white;
  border: 1px solid $accent-color;

  .card {
    background-color: transparent;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
  }

  .collapsed-view {
    display: flex;
    align-items: center;
    padding: 1rem;

    .wine-image {
      height: 80px;
      object-fit: cover;
      border-radius: 8px;
      margin-right: 1rem;
    }

    .wine-summary {
      flex: 1;
      display: flex;
      flex-direction: column;

      h2 {
        font-size: 1rem;
        margin-bottom: 0.3rem;
      }

      .prices {
        align-self: end;
        display: flex;
        justify-content: space-between;
        width: 100%;
      }

      .grape,
      .characteristics,
      .price {
        font-size: 12px;
        margin-bottom: 0.3rem;
      }
    }
  }

  .accordion-toggle {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0.5rem 0;
    background-color: transparent;
    font-size: 1.5rem;
    color: $primary-color;
    user-select: none;

    i {
      transition: transform 0.3s ease;
      margin-right: 0.5rem;
      color: $accent-color;
    }

    .toggle-label {
      font-size: 12px;
      color: $primary-color;
    }
  }

  .expanded-view {
    padding: 0 1rem 1rem;

    p {
      margin: 0.5rem 0;
      font-size: 0.75rem;
    }

    transform: translateZ(0);
  }
}

/* Accordion Transition */
.accordion-enter-active,
.accordion-leave-active {
  transition: max-height 0.3s ease;
}

.accordion-enter-from,
.accordion-leave-to {
  max-height: 0;
}

.accordion-enter-to,
.accordion-leave-from {
  max-height: 500px;
}
</style>
