<template>
  <section class="wine-menu-section">
    <header class="wine-header">
      <h1 class="wine-title">Vino</h1>
    </header>
    <p class="note">Unsere Hausweine gibt es für<br> 7€ (0.2l) bzw. 19€ (0.75l).</p>
    <div class="wine-tasting-link">
      <router-link to="/wine-tasting" class="tasting-link">🍷Die Weine aus unserer letzten Weinverkostung findest du hier >></router-link>
    </div>
    <div v-if="selectedColor === 'rosé' && false" class="happy-hour-hint">🎉 Happy Hour 🎉! Mo-Fr bis 19 Uhr zu
      jeder Flasche Rosé eine Plato Mixto aufs Haus.
    </div>
    <div class="filter-buttons">
      <button :class="{ active: selectedColor === '' }" @click="selectedColor = ''">Alle</button>
      <button :class="{ active: selectedColor === 'red' }" @click="selectedColor = 'red'">Rot</button>
      <button :class="{ active: selectedColor === 'white' }" @click="selectedColor = 'white'">Weiß</button>
      <button :class="{ active: selectedColor === 'rosé' }" @click="selectedColor = 'rosé'">Rosé</button>
    </div>
    <div class="happy-hour-container">
      <span></span>
      <span></span>
      <span></span>
      <span>{{ roseLabel }}</span>
    </div>
    <br />
    <div v-if="shouldUseApi && loading" class="spinner">
      <h3>Bin kurz im Weinkeller..</h3>
      <div class="spinner-icon"></div>
    </div>
    <div v-else class="scrollContainer">
      <transition-group name="wine" tag="ul" class="wine-list">
        <WineItem v-for="wine in filteredWines" :key="wine.id" :wine="wine"/>
      </transition-group>
    </div>
  </section>
</template>

<script setup lang="ts">
import {ref, onMounted, computed} from 'vue';
import {type Wine} from "../interfaces/vino.ts";
import WineItem from '../components/WineItem.vue';
import {useNow} from '@vueuse/core';
import {useWineMenu} from "./useWineMenu.ts";
import {vinos as staticVinos}  from '../data/vinos.ts'

const  {loadVinos, loading, vinos} = useWineMenu();
const shouldUseApi = true;

const now = useNow();
const isHappyHour = computed(() => {
  const date = now.value;
  const day = date.getDay();
  const hour = date.getHours();
  return day >= 1 && day <= 5 && hour < 19;
});

const wines = ref<Wine[]>([]);
const selectedColor = ref<string>('');

onMounted(async () => {
  if (!shouldUseApi) {
    wines.value = staticVinos;
    return;
  }
  await loadVinos();
  wines.value = vinos.value;
});

const roseLabel = computed(() => {
  return ''
  return isHappyHour.value ? 'Happy Hour 🎉' : '';
});

const filteredWines = computed(() => {
  if (!selectedColor.value) return wines.value;
  return wines.value.filter(wine => wine.color === selectedColor.value);
});
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";

.note {
  font-size:  1rem;
}

.wine-tasting-link {
  text-align: center;
  margin-bottom: 20px;
}

.tasting-link {
  color: #8b4513;
  text-decoration: none;
  font-weight: bold;
  font-size: 16px;
  padding: 8px 16px;
  border: 2px solid #8b4513;
  border-radius: 6px;
  display: inline-block;
  transition: all 0.3s ease;
}

.tasting-link:hover {
  background-color: #8b4513;
  color: white;
}

.wine-menu-section {
  background-color: $background-color;
  color: $text-color;
  font-family: $font-family;
  padding: 2rem 1rem;
  max-width: 90%;
  margin: 10% auto 20%;
  border: 2px solid $accent-color;
  border-radius: 8px;
  position: relative;
}

.top-toast {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: .5rem;
  justify-content: space-between;
  background: $background-color;
  color: $accent-color;
  border: 1px solid $accent-color;
  border-radius: 6px;
  padding: .5rem .75rem;
  margin: .5rem 0 0;
}

.toast-close {
  background: transparent;
  border: none;
  color: $accent-color;
  font-size: 1.2rem;
  line-height: 1;
  cursor: pointer;
}

.wine-header {
  text-align: center;
  position: absolute;
  width: 100%;
  top: -34px;
}

.wine-title {
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  background: $background-color;
  width: min-content;
  margin: 0 auto;
  padding: 0 1rem;
  color: $accent-color;
  font-size: 2rem;
  font-family: 'King Red';
  font-weight: normal;
}

.happy-hour-hint {
  text-align: center;
}

.happy-hour-container {
  width: 100%;
  display: flex;
  justify-content: space-evenly;

  span {
    flex: 1;
    font-size: 11px;
    text-align: center;
  }
}

.wine-subtitle {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  color: $accent-color;
  text-align: center;
}

.filter-buttons {
  text-align: center;
  margin: 3rem 0 0 0;

  button {
    padding: 0.5rem 1rem;
    border: 1px solid $primary-color;
    background-color: #fff;
    color: $dark-color;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
    margin-right: 0.5rem;
    flex: auto;

    &:hover {
      background-color: $accent-color;
      color: #fff;
      border-color: $accent-color;
    }

    &.active {
      background-color: $accent-color;
      color: #fff;
      border-color: $accent-color;
    }
  }
}

.scrollContainer {
  overflow-y: auto;
  padding: 1rem 0;
  border-radius: 5px;
}

.wine-list {
  list-style: none;
  margin: 0;
  padding: 0;
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rose-image {
  opacity: 0.5;
  display: block;
  margin: 1rem auto;
}

.coming-soon {
  display: block;
  width: 100%;
  text-align: right;
  padding: 8px;
  color: grey;
}

.wine-enter-active, .wine-leave-active {
  transition: max-height 0.41s ease-in-out, opacity 0.41s ease-in-out;
  overflow: hidden;
}

.wine-enter-from, .wine-leave-to {
  max-height: 0;
  opacity: 0;
}

.wine-enter-to, .wine-leave-from {
  max-height: 500px;
  opacity: 1;
}
</style>
