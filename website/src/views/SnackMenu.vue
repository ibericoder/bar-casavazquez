<template>
  <!-- <div class="hint" style="display: block">
    Heute <b> Buffet</b> mit Selbstbedienung <br/>
    <p>Beim Buffet findest du Bambus-Schälchen, die du mit deinen Lieblings Snacks <b>voll</b>machen kannst.</p>
    <p>Am Ende zählen wir einfach die Schälchen und berechnen jeweils 2,50€ (mit Brot-Flatrate - solange der Vorrat reicht)</p>
    <br/>
    <p>🍽️ Guten Appetit! 😊</p>
    <p>(Was du am Buffet nicht findest, kannst du à la carte bestellen. Bitte auf längere Wartezeiten einstellen)</p>

    <details style="margin-top: 1rem">
      <summary style="cursor: pointer">Portionenzähler (optional)</summary>
      <div style="margin-top: 0.5rem; display: flex; align-items: center; gap: 1rem; justify-content: center">
        <button @click="decrementCounter" style="font-size: 1.5rem">−</button>
        <span style="font-size: 1.5rem">{{ portionCount }}</span>
        <button @click="incrementCounter" style="font-size: 1.5rem">+</button>
      </div>
    </details>
  </div> -->

  <div class="filter-buttons" style="display: none">
    <button class="filter-button" :class="{ active: veggie }" @click="toggleVeggie">
      <i class="pi pi-times" v-if="veggie" style="font-size: 8px"></i>
      Nur Veggie
    </button>
  </div>

  <section class="snacks-menu">
    <header class="snacks-header">
      <h1 class="snacks-title">SNACKS</h1>
      <!--      <p class="snacks-subtitle">FÜR DEN KLEINEN HUNGER</p>-->
    </header>



    <div class="scrollContainer">
      <div class="snack-section">
        <li
            v-for="snack in filteredSnacks"
            :key="snack.name"
            class="basic-snacks-item"
        >
          <div class="snack-text">
            <span class="snacks-name">{{ snack.name }}</span>
            <img v-if="snack.onm" class="onmLogo" :src="onmLogo" alt="Olive und Meer" @click="showOnmInfo = true"/>
            <BaseModal v-model="showOnmInfo">
              <div style="display: flex;margin-bottom: 1rem; gap: 1rem">
                <h2>Von <i>Olive & Meer</i></h2>
                <img class="onmLogo" :src="onmLogo"/>
              </div>
              <p>Unser Lieblings-Laden für Spanische Weine und Feinkost. Dir schmecken die Oliven? Dann statte doch <i>Raquel</i>
                mal
                einen Besuch ab. </p>
              <p style="text-align: right">Warendorfer Str. 61, 48145 Münster</p>
            </BaseModal>
            <span class="snacks-description">{{ snack.description }}</span>
          </div>
          <span class="snacks-price">{{ snack.price }}</span>
        </li>

        <ul class="snacks-extras">
          <li class="snacks-item extra veggie">
            <span class="snacks-name">Extra Aioli Dip</span>
            <span class="snacks-price">1,5</span>
          </li>
          <li class="snacks-item extra veggie">
            <span class="snacks-name">Extra Baguette</span>
            <span class="snacks-price">2,50</span>
          </li>

          <p class="snacks-note">
            Unsere Snacks & Platten sind ideal zum Teilen und bieten eine köstliche Begleitung zu unseren Drinks.
          </p>
        </ul>
      </div>

      <div class="snack-section">
        <hr/>
        <br/>
  <h3 class="snacks-subtitle">Coca <img class="coca-image" :src="cocaImage" alt="Coca" @click="showCocaInfo = true" style="cursor:pointer;vertical-align:middle;height:28px;margin-left:8px;"/></h3>
        <p class="snacks-note">
          Coca ist ein traditionelles spanisches Flachbrot, das mit mediterranen Zutaten belegt wird. Die Portion ist
          vergleichbar mit einer Pizza.
        </p>
        
              <BaseModal v-model="showCocaInfo">
                <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                  <h2>Coca – Spanisches Flachbrot</h2>
                  <img :src="cocaImage" alt="Coca" style="max-width: 300px; border-radius: 8px;"/>
                </div>
                <p>Die Coca ist ein traditionelles spanisches Flachbrot, das mit mediterranen Zutaten belegt wird. Sie ist besonders beliebt in Katalonien und auf den Balearen. Die Portion ist vergleichbar mit einer Pizza und eignet sich perfekt zum Teilen.</p>
              </BaseModal>
        <ul class="snacks-extras">
          <li class="snacks-item extra veggie">
            <span class="snacks-name"><b>Vegetarisch</b><br/>mit Tomatensauce und Mozarella und mit guten Dingen aus dem meditarrenen Garten belegt (auf Wunsch Vegan)</span>
            <span class="snacks-price">12,90</span>
          </li>
          <li class="snacks-item extra veggie">
            <span class="snacks-name"><b>Wahlweise zusätzlich:</b></span>
          </li>
          <li class="snacks-item extra" v-if="!veggie">
            <span class="snacks-name">+ Chorizo</span>
            <span class="snacks-price">+ 3,90</span>
          </li>
          <li class="snacks-item extra" v-if="!veggie">
            <span class="snacks-name">+ Serrano</span>
            <span class="snacks-price">+ 3,90</span>
          </li>
          <li class="snacks-item extra" v-if="!veggie">
            <span class="snacks-name">Doppelt Mozarella</span>
            <span class="snacks-price">+ 2,50</span>
          </li>
        </ul>
      </div>

      <div class="snack-section bundle">
        <hr/>
        <br/>
        <h3 class="snacks-subtitle">Bundle</h3>
        <ul class="snacks-extras">
          <li class="snacks-item extra veggie">
            <span class="snacks-name"><b>1 Flasche Hauswein + Plato Queso ODER Serrano</b><br/></span>
            <span class="snacks-price">26,50</span>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import {ref, computed, onMounted} from "vue";
import onmLogo from "../assets/images/Logo-Olive-Meer_klein.png"
import BaseModal from "../components/BaseModal.vue";
import cocaImage from "../assets/images/coca.png";

const veggie = ref(false)
const showOnmInfo = ref(false)
const showCocaInfo = ref(false)


const snacks = [
  {name: 'Nachos mit Aioli Dip', description: '', price: '5', veggie: true},
  {name: 'Brot Aioli Dip', description: '', price: '5', veggie: true},
  {name: 'Oliven Mix', description: '', price: '5', veggie: true, onm: true},
  {name: 'Plato de Jamón', description: '(80g) + Brot', price: '9,5', veggie: false},
  {name: 'Plato de Quesos', description: '(80g) + Brot', price: '9,5', veggie: true},
  {name: 'Plato Mixto', description: 'Gemischte Platte mit Jamón & Quesos + Brot', price: '16,5', veggie: false},
];

const filteredSnacks = computed(() =>
    veggie.value ? snacks.filter(s => s.veggie) : snacks
);

function toggleVeggie() {
  veggie.value = !veggie.value;
}

const portionCount = ref(0)
const storageKey = 'buffetCounter'
const ttlKey = 'buffetCounterTTL'

function loadCounter() {
  const stored = localStorage.getItem(storageKey)
  const ttl = localStorage.getItem(ttlKey)
  const now = Date.now()
  if (stored && ttl && parseInt(ttl) > now) {
    portionCount.value = parseInt(stored)
  } else {
    localStorage.removeItem(storageKey)
    localStorage.removeItem(ttlKey)
  }
}

/** function saveCounter() {
 const now = Date.now()
 localStorage.setItem(storageKey, portionCount.value.toString())
 localStorage.setItem(ttlKey, (now + 12 * 60 * 60 * 1000).toString())
 } */

/** function incrementCounter() {
 portionCount.value++
 saveCounter()
 }

 function decrementCounter() {
 if (portionCount.value > 0) {
 portionCount.value--
 saveCounter()
 }
 } */

onMounted(() => {
  loadCounter()
})
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";

.coca-image {
  height: 28px;
  vertical-align: middle;
  margin-left: 8px;
  cursor: pointer;
}

ul {
  list-style: none;
}

.hint {
  text-shadow: 1px 1px 2px #ceaa72;
  border: 2px solid #ceaa72;
  background-color: transparent;
}

hr {
  width: 33%;
  margin: 0 auto;
  border-color: #ceaa72;
}

.snacks-menu {
  background-color: $background-color;
  color: $text-color;
  font-family: $font-family;
  max-width: 90%;
  border: 2px solid $accent-color;
  border-radius: 8px;
  padding: 0 0.5rem;
  margin: 10% auto;
  position: relative;
  padding-top: 3rem;

  .scrollContainer {
    overflow: scroll;
    padding: 1rem;
    border-radius: 5px;

    &.veggie {
      .snacks-item {
        &:not(.veggie) {
          display: none;
        }
      }

      .snack-section {
        &:not(.veggie) {
          display: none;
        }
      }
    }
  }
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

.inactive {
  opacity: .5;
}

.snacks-header {
  text-align: center;
  position: absolute;
  width: 100%;
  top: -34px;
}

.snacks-title {
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

.snack-text {
  position: relative;

  img {
    position: absolute;
    right: -50px;
    height: 30px;
    transform: rotate(-15deg);
  }
}

.onmLogo {
  height: 35px;
  transform: rotate(-15deg);
}

.snacks-subtitle {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  text-align: center;
}

.bundle {
  li {
    margin-bottom: 1rem !important;
  }
}

.snack-enter-active, .snack-leave-active {
  transition: max-height 0.41s ease-in-out;
  overflow: hidden;
}

.snack-enter-from, .snack-leave-to {
  max-height: 0;
}

.snack-enter-to, .snack-leave-from {
  max-height: 100px;
}



.basic-snacks-list {
  list-style: none;
  margin: 0;
  padding: 0;
  margin-bottom: 1.5rem;
}

.basic-snacks-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;

  .snack-text {
    display: flex;
    flex-direction: column;

    .snacks-description {
      font-size: 0.7rem;
      font-style: italic;
      padding-right: 4px;
    }
  }

  .snacks-name {
    font-size: 1rem;
    padding-right: 1rem;
  }

  .snacks-price {
    font-size: 1rem;
    color: $accent-color;
  }

  &.extra {
    span {
      font-size: 0.7rem;
    }
  }
}

.snacks-extras {
  margin-bottom: 2rem;

  li {
    display: flex;
    justify-content: space-between;
    margin: 0.2rem 0;
    font-size: 0.9rem;
    font-style: italic;
    color: $text-color;
  }
}

.snacks-note {
  font-size: 0.7rem;
  line-height: 1.4;
  margin: 2rem auto;
  text-align: center;
  color: $accent-color;
  max-width: 90%;
}

.today-hint {
  color: white;
  margin: 1rem auto;
}
</style>
