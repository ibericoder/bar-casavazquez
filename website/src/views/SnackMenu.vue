<template>
  <div v-show="false" class="hint" style="display: block">
    Heute <b> Buffet</b> mit Selbstbedienung <br />
    <p>Beim Buffet findest du Bambus-Schälchen, die du mit deinen Lieblings Snacks <b>voll</b>machen kannst.</p>
    <p>Am Ende zählen wir einfach die Schälchen und berechnen jeweils 2,50€ (mit Brot-Flatrate - solange der Vorrat
      reicht)</p>
    <br />
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
  </div>

  <div class="filter-buttons">
    <span>Filter:</span>
    <button class="filter-button" :class="{ active: veggie }" @click="toggleVeggie">
      <i class="pi pi-times" v-if="veggie" style="font-size: 8px"></i>
      Nur Veggie
    </button>
    <button class="filter-button" :class="{ active: keto }" @click="toggleKeto">
      <i class="pi pi-times" v-if="keto" style="font-size: 8px"></i>
      Keto-freundlich
    </button>
  </div>

  <section class="snacks-menu">
    <header class="snacks-header">
      <h1 class="snacks-title">SNACKS</h1>
    </header>
    <div v-if="showTopToast" class="top-toast" role="status" aria-live="polite">
      <span>Saludos desde Madrid – Diesen Samstag bekommt ihr zu jedem Getränk eine kleine Tapita, ganz wie ihr es aus
        der Hauptstadt Spaniens kennt.</span>
      <button class="toast-close" @click="showTopToast = false" aria-label="Schließen">×</button>
    </div>

    <p class="snacks-note" style="margin-top: 1rem; font-style: italic;">
      <strong>Hinweis:</strong> Damit euch alle Snacks warm erreichen, servieren wir diese ggf. nacheinander (nicht
      immer alles gleichzeitig).
    </p>

    <div class="scrollContainer">
      <div class="snack-section">
        <TransitionGroup name="snack" tag="ul" class="basic-snacks-list">
          <li v-for="snack in filteredSnacks" :key="snack.name" class="basic-snacks-item">
            <div class="snack-text">
              <span class="snacks-name">
                {{ snack.name }}
                <span v-if="snack.veggie" class="veggie-icon" title="Vegetarisch">&#127811;</span>
              </span>
              <!-- <img v-if="snack.onm" class="onmLogo" :src="onmLogo" alt="Olive und Meer" @click="showOnmInfo = true" /> -->
              <BaseModal v-model="showOnmInfo">
                <div style="display: flex;margin-bottom: 1rem; gap: 1rem">
                  <h2>Von <i>Olive & Meer</i></h2>
                  <img class="onmLogo" :src="onmLogo" />
                </div>
                <p>Unser Lieblings-Laden für Spanische Weine und Feinkost. Dir schmecken die Oliven? Dann statte doch
                  <i>Raquel</i>
                  mal
                  einen Besuch ab.
                </p>
                <p style="text-align: right">Warendorfer Str. 61, 48145 Münster</p>
              </BaseModal>
              <span class="snacks-description">{{ snack.description }}</span>
            </div>
            <span class="snacks-price">{{ snack.price }}</span>
          </li>
        </TransitionGroup>
        <br />
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

      <Transition name="section">
        <div class="snack-section" v-if="!veggie">
          <hr />
          <br />
          <h3 class="snacks-subtitle">Albondigas</h3>
          <p class="snacks-note">
            Albondigas (Fleischbällchen) mit Käse und Chili gefüllt in aromatischer Tomaten-Salsa – dazu reichen wir Brot. Perfekt für den kleinen
            Hunger auf etwas Deftiges.
          </p>
          <ul class="snacks-extras">
            <li class="snacks-item extra">
              <span class="snacks-name">Albondigas – Portion</span>
              <span class="snacks-price">9,50</span>
            </li>
          </ul>
        </div>
      </Transition>

      <div class="snack-section" v-if="!veggie">
        <hr />
        <br />
        <h3 class="snacks-subtitle">Plato de Jamón</h3>
        <p class="snacks-note">
          Serrano Schinken – luftgetrocknet und von höchster Qualität. Dazu servieren wir Brot.
        </p>
        <ul class="snacks-extras">
          <li class="snacks-item extra">
            <span class="snacks-name">Plato de Jamón</span>
            <span class="snacks-price">9,50</span>
          </li>
        </ul>
      </div>

      <Transition name="section">
        <div class="snack-section" >
          <hr />
          <br />
          <h3 class="snacks-subtitle">Plato de Quesos</h3>
          <p class="snacks-note">
            Manchego Käse – der klassische spanische Schafskäse. Dazu servieren wir Brot.
          </p>
          <ul class="snacks-extras">
            <li class="snacks-item extra veggie">
              <span class="snacks-name">Plato de Quesos</span>
              <span class="snacks-price">9,50</span>
            </li>
          </ul>
        </div>
      </Transition>

      <div class="snack-section">
        <hr />
        <br />
        <h3 class="snacks-subtitle">Plato Mixto</h3>
        <p class="snacks-note">
          Gemischte Platte mit Jamón Serrano und Manchego Käse. Dazu servieren wir Brot.
        </p>
        <ul class="snacks-extras">
          <li class="snacks-item extra">
            <span class="snacks-name">Plato Mixto</span>
            <span class="snacks-price">16,50</span>
          </li>
        </ul>
      </div>

      <Transition name="section">
        <div class="snack-section" v-if="!keto">
          <hr />
          <br />
          <h3 class="snacks-subtitle">
            Coca
            <span class="coca-clickable" @click="showCocaInfo = true">
              <img class="coca-image" :src="cocaImage" alt="Coca" />
              <span class="enlarge-hint">🔍</span>
            </span>
          </h3>
          <p class="snacks-note">
            Coca ist ein traditionelles spanisches Flachbrot, das mit mediterranen Zutaten belegt wird. Die Portion ist
            vergleichbar mit einer Pizza.
          </p>

          <BaseModal v-model="showCocaInfo">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem; margin-bottom: 1rem;">
              <h2>Coca – "Spanische Pizza"</h2>
              <img :src="cocaImage" alt="Coca" style="max-width: 300px; border-radius: 8px;" />
            </div>
            <p>Die Coca ist ein traditionelles spanisches Flachbrot, das mit mediterranen Zutaten belegt wird. Sie ist
              besonders beliebt in Katalonien und auf den Balearen. Die Portion ist vergleichbar mit einer Pizza und
              eignet sich perfekt zum Teilen oder allein genießen.</p>
          </BaseModal>
          <ul class="snacks-extras">
            <li class="snacks-item extra veggie">
              <span class="snacks-name"><b>Vegetarisch</b><br />mit Tomatensauce und Mozarella und mit guten Dingen aus
                dem meditarrenen Garten belegt (auf Wunsch Vegan)</span>
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
              <span class="snacks-name">+ Albondigas</span>
              <span class="snacks-price">+ 3,90</span>
            </li>
            <li class="snacks-item extra veggie">
              <span class="snacks-name">Doppelt Mozarella</span>
              <span class="snacks-price">+ 2,50</span>
            </li>
          </ul>
        </div>
      </Transition>

      <div class="snack-section bundle">
        <hr />
        <br />
        <h3 class="snacks-subtitle">Bundle</h3>
        <ul class="snacks-extras">
          <li class="snacks-item extra veggie">
            <span class="snacks-name"><b>1 Flasche Hauswein + Plato Queso ODER Serrano</b><br /></span>
            <span class="snacks-price">26,50</span>
          </li>
        </ul>
      </div>
      <div v-show=false class="snack-section bundle">
        <hr />
        <br />
        <h3 class="snacks-subtitle">Dessert</h3>
        <ul class="snacks-extras">
          <li class="snacks-item extra veggie">
            <span class="snacks-name"><b>Tartufo mit Schoko-Kern und Haselnussmantel</b><br /></span>
            <span class="snacks-price">8,50</span>
          </li>
          <li class="snacks-item extra veggie">
            <span class="snacks-name"><b>Antojos de Dulcinea - Biskuitkuchen mit fruchtiger Sauce</b><br /></span>
            <span class="snacks-price">6,50</span>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import onmLogo from "../assets/images/Logo-Olive-Meer_klein.png"
import BaseModal from "../components/BaseModal.vue";
import cocaImage from "../assets/images/coca.png";

const veggie = ref(false)
const keto = ref(false)
const showOnmInfo = ref(false)
const showCocaInfo = ref(false)
const showTopToast = ref(false)

const snacks = [
  { name: 'Nachos mit Aioli Dip', description: '', price: '5', veggie: true, keto: false },
  { name: 'Brot Aioli Dip', description: '', price: '5', veggie: true, keto: false },
  { name: 'Oliven Mix', description: '', price: '5', veggie: true, onm: true, keto: true },
  { name: 'Dátiles con Bacon', description: 'Datteln im Speckmantel', price: '7,5', veggie: false, keto: false },
  { name: 'Kroketten + Dip', description: 'gefüllt mit Käse & Jalapeños', price: '6,5', veggie: false, available: true, keto: false },
  { name: 'Aros de Cebolla', description: 'Zwiebelringe', price: '5', veggie: true, keto: false },
  { name: 'Croquetas con Chorizo', description: 'kleine Kroketten mit Chorizo-Füllung', price: '6,5', veggie: false, keto: false },
  { name: 'Palitos Vegetales', description: 'Gemüse-Sticks mit Erbsen-Minze', price: '7,5', veggie: true, keto: true },
  { name: 'Frango Piri Piri', description: 'würzige kleine Hähnchen Flügel mit Piri Piri Paprika Gewürz (pikant)', price: '8,5', veggie: false, keto: true },
  { name: 'Tortilla Española', description: 'Mini Kartoffel-Omelett', price: '8,5', veggie: true, keto: true },
];
// { name: 'Palta Rebozada', description: 'Avocadospalten paniert', price: '8,5', veggie: true, keto: false },
// { name: 'Tapas Mix (2p)', description: 'Mix aus verschiedenen Tapas', price: '24,5', veggie: false, keto: false },
// { name: 'Vegane Nuggets', description: 'mit Tomaten-Salsa oder Aioli', price: '6,5', veggie: true, keto: false },
// { name: 'Veggi Mix (2p)', description: 'Mix aus verschiedenen Veggie Tapas.', price: '24,5', veggie: true, keto: false },
// { name: 'Champiñones Rebozados', description: 'Panierte Champignons', price: '5', veggie: true, keto: false },

const filteredSnacks = computed(() => {
  let filtered = snacks.filter(s => s.available !== false);
  if (veggie.value) {
    filtered = filtered.filter(s => s.veggie);
  }
  if (keto.value) {
    filtered = filtered.filter(s => s.keto);
  }
  return filtered;
});

function toggleVeggie() {
  veggie.value = !veggie.value;
}

function toggleKeto() {
  keto.value = !keto.value;
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

function saveCounter() {
  const now = Date.now()
  localStorage.setItem(storageKey, portionCount.value.toString())
  localStorage.setItem(ttlKey, (now + 12 * 60 * 60 * 1000).toString())
}

function incrementCounter() {
  portionCount.value++
  saveCounter()
}

function decrementCounter() {
  if (portionCount.value > 0) {
    portionCount.value--
    saveCounter()
  }
}

onMounted(() => {
  loadCounter()
})
</script>

<style lang="scss" scoped>
@use "../assets/styles/main" as *;

.coca-image {
  height: 28px;
  vertical-align: middle;
  margin-left: 8px;
  cursor: pointer;
}

.coca-clickable {
  display: inline-block;
  position: relative;
  cursor: pointer;
  transition: transform 0.2s ease;

  &:hover {
    transform: scale(1.1);
  }

  &:hover .enlarge-hint {
    opacity: 1;
  }
}

.enlarge-hint {
  display: inline-block;
  margin-left: 0.25rem;
  font-size: 0.9rem;
  opacity: 0.6;
  transition: opacity 0.2s ease;
  vertical-align: middle;
}

ul {
  list-style: none;
}

.filter-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;

  span {
    font-weight: bold;
    color: $text-color;
  }

  .filter-button {
    background-color: transparent;
    border: 2px solid $accent-color;
    color: $accent-color;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.25rem;

    &.active {
      background-color: $accent-color;
      color: $background-color;
    }
  }
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

.veggie-icon {
  display: inline-block;
  font-size: 0.9rem;
  vertical-align: middle;
  transform: translate(-2px, -5px) rotate(282deg);
  opacity: .75;
}

.bundle {
  li {
    margin-bottom: 1rem !important;
  }
}

.snack-enter-active,
.snack-leave-active {
  transition: all 0.4s ease;
}

.snack-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.snack-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.snack-move {
  transition: transform 0.4s ease;
}

.section-enter-active,
.section-leave-active {
  transition: all 0.4s ease;
}

.section-enter-from,
.section-leave-to {
  opacity: 0;
  transform: translateY(-20px);
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
