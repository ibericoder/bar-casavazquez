<template>
  <div class="snack-item card" @click="toggle">
    <!-- Zusammengeklappte Ansicht -->
    <div class="collapsed-snack">
      <img :src="snack.image ? snack.image : defaultImage" alt="Weinbild" class="snack-image"/>
      <div class="snack-summary">
        <h2>{{ snack.name }}</h2>
        <p class="characteristics" v-if="snack.characteristics">
          {{ snack.characteristics }}
        </p>
        <p class="grape"> {{ snack.grape }}</p>
        <div class="prices">
          <p class="price" v-if="snack.prices['0.1l']">
            <strong>0,1l:</strong> {{ snack.prices['0.1l'] }}
          </p>
          <p class="price" v-if="snack.prices['0.2l']">
            <strong>0,2l:</strong> {{ snack.prices['0.2l'] }}
          </p>
          <p class="price">
            <strong>Flasche:</strong> {{ snack.prices.flasche }}
          </p>
        </div>
      </div>
    </div>
    <div class="accordion-toggle">
      <i :class="{'pi': true, 'pi-chevron-down': !isOpen, 'pi-chevron-up': isOpen}"/>
      <!--      <span class="toggle-label">{{ isOpen ? 'Weniger Infos' : 'Mehr Infos' }}</span>-->
    </div>

    <!-- Ausgeklappte Ansicht -->
    <transition name="accordion">
      <div class="expanded-view" v-if="isOpen">
        <p v-if="snack.origin"><strong>Herkunft:</strong> {{ snack.origin }}</p>
        <p v-if="snack.shortDescription"><strong>Beschreibung:</strong> {{ snack.shortDescription }}</p>
        <p v-if="snack.longDescription">{{ snack.longDescription }}</p>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import type {Wine} from '../interfaces/vino';
import 'primeicons/primeicons.css';

const {snack} = defineProps<{ snack: Wine }>();

const isOpen = ref(false);
// Verwende den relativen Pfad zum Default-Bild
const defaultImage = snack.color === 'white'
    ? new URL('../assets/images/default_vino_white.png', import.meta.url).href
    : new URL('../assets/images/default_vino_red.png', import.meta.url).href;

function toggle() {
  isOpen.value = !isOpen.value;
}
</script>

<style scoped lang="scss">
@import "../assets/styles/main.scss";

.snack-item {
  position: relative;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
  padding-bottom: 2.5rem;

  .collapsed-view {
    display: flex;
    align-items: center;
    padding: 1rem;

    .snack-image {
      height: 80px;
      object-fit: cover;
      border-radius: 8px;
      margin-right: 1rem;
    }

    .snack-summary {
      flex: 1;
      display: flex;
      flex-direction: column;

      h2 {
        font-size: 1rem;
        margin-bottom: 0.3rem;
        color: $dark-color;
      }

      .prices {
        align-self: end;
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
    background-color: $toggle-bg;
    border-top: 1px solid $primary-color;
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
    border-top: 1px solid $primary-color;

    p {
      margin: 0.5rem 0;
      font-size: 13px;
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
