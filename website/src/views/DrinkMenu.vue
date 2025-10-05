<template>

  <!--  <div class="hint">-->
  <!--    Bundle des Tages 12,-  <br> 1 Glas Hauswein weiß <br>+ 1 x Käseplatte-->
  <!--  </div>-->

  <!-- Filter-Button -->
  <div class="filter-buttons">
    <button class="filter-button" :class="{ active: nonAlcoholic }" @click="toggleNonAlcoholic">
      <i class="pi pi-times" v-if="nonAlcoholic" style="font-size: 8px"></i>
      Nur alkoholfrei
    </button>
  </div>

  <!-- Top announcement toast -->
  <div v-if="showTopToast" class="top-toast" role="status" aria-live="polite">
    <span>Saludos desde Madrid – Diesen Samstag bekommt ihr zu jedem Getränk eine kleine Tapita, ganz wie ihr es aus der Hauptstadt Spaniens kennt.</span>
    <button class="toast-close" @click="showTopToast = false" aria-label="Schließen">×</button>
  </div>
  <!--    Softdrinks-->
  <section class="drinks-menu-section">
    <header class="drinks-header">
      <h1 class="drinks-title">Bebidas</h1>
    </header>

    <div class="drinks-content" :class="nonAlcoholic && 'non-alcoholic'">
      <transition-group name="drink" tag="ul" class="drinks-list">
        <li v-for="drink in nonAlcoholic ? softdrinks.filter(d => !d.alcoholic) : softdrinks" :key="drink.name"
            class="drinks-item">
          <div class="drink-text">
            <span class="drinks-name">{{ drink.name }} &nbsp;{{ drink.volume }}
              <sup v-if="drink.allergens" class="allergen-indices">{{ drink.allergens.join(',') }}</sup>
            </span>
            <div class="new-label" v-if="drink.neu">
              NEU
            </div>
          </div>
          <span class="drinks-price">{{ drink.price }}</span>
        </li>
      </transition-group>
    </div>
  </section>

  <!--    Bier-->
  <section class="drinks-menu-section">
    <header class="drinks-header">
      <h1 class="drinks-title">Cerveza</h1>
    </header>

    <div class="drinks-content" :class="nonAlcoholic && 'non-alcoholic'">
      <transition-group name="drink" tag="ul" class="drinks-list">
        <li v-for="drink in nonAlcoholic ? beers.filter(d => !d.alcoholic) : beers" :key="drink.name"
            class="drinks-item">
          <div v-if="drink.available !== false" class="drink-text">
            <span class="drinks-name">{{ drink.name }}
            <sup v-if="drink.allergens" class="allergen-indices">{{ drink.allergens.join(',') }}</sup>
            </span>
          </div>
          <span v-if="drink.available !== false" class="drinks-price">{{ drink.price }}</span>
        </li>
      </transition-group>
    </div>
  </section>

  <!--    Spritz-->
  <section class="drinks-menu-section" v-if="!nonAlcoholic">
    <header class="drinks-header">
      <h1 class="drinks-title">Spritz</h1>
      <p class="drinks-subtitle">lecker</p>
    </header>

    <div class="drinks-content" :class="nonAlcoholic && 'non-alcoholic'">
      <transition-group name="drink" tag="ul" class="drinks-list">
        <li v-for="drink in nonAlcoholic ? spritz.filter(d => !d.alcoholic) : spritz" :key="drink.name"
            class="drinks-item">
          <div class="drink-text">
            <span class="drinks-name">{{ drink.name }}
            <sup v-if="drink.allergens" class="allergen-indices">{{ drink.allergens.join(',') }}</sup>
            </span>
          </div>
          <span class="drinks-price">{{ drink.price }}</span>
        </li>
      </transition-group>
    </div>
    <p class="note">
      (*alkoholfrei für 7,50)<br><br>
      Achtet auch auf unsere Aktionen!
    </p>
  </section>

  <!--    Gin Cocktails-->
  <section class="drinks-menu-section" v-if="!nonAlcoholic">
    <header class="drinks-header">
      <h1 class="drinks-title">Gin</h1>
      <p class="drinks-subtitle">N°3 Drinks</p>
    </header>
    <br>
    <p class="note">
      Unsere Gin-Cocktails und Longdrinks bereiten wir mit dem hochwertigen N°3 Gin zu.
    </p>
    <br>
    <img src="../assets/images/no32.png" class="no3bottle" alt="no3 Gin"/>
    <div class="drinks-content" :class="nonAlcoholic && 'non-alcoholic'">
      <transition-group name="drink" tag="ul" class="drinks-list">
        <li v-for="drink in nonAlcoholic ? no3.filter(d => !d.alcoholic) : no3" :key="drink.name" class="drinks-item">
          <div class="drink-text">
            <span class="drinks-name">{{ drink.name }}
            <sup v-if="drink.allergens" class="allergen-indices">{{ drink.allergens.join(',') }}</sup>
            </span>
          </div>
          <span class="drinks-price">{{ drink.price }}</span>
        </li>
      </transition-group>
    </div>

    <div class="no3-desc">
      <img src="../assets/images/no3.png" alt="no3 Gin"/>
      <p class="note">
        “No. 3 ist ein unvergleichlicher Ultra-Premium London Dry Gin, entstanden aus dem Streben nach Perfektion, um
        den besten Gin der Welt zu kreieren. Er bietet die perfekte Balance aus drei entscheidenden Aromen: Wacholder,
        Zitrus und Gewürzen. Dadurch ist er erfrischend im Geschmack und klassisch im Stil.”
      </p>
    </div>
  </section>

  <!--   Cocktails-->
  <section class="drinks-menu-section" v-if="!nonAlcoholic">
    <header class="drinks-header">
      <h1 class="drinks-title">Cócteles</h1>
      <p class="drinks-subtitle">Cocktails</p>
    </header>
    <div class="drinks-content" :class="nonAlcoholic && 'non-alcoholic'">
      <transition-group name="drink" tag="ul" class="drinks-list">
        <li v-for="drink in nonAlcoholic ? cocktails.filter(d => !d.alcoholic) : cocktails" :key="drink.name"
            class="drinks-item">
          <div class="drink-text">
            <span class="drinks-name">{{ drink.name }}
              <sup v-if="drink.allergens" class="allergen-indices">{{ drink.allergens.join(',') }}
              </sup>
            </span>
          </div>
          <span class="drinks-price">{{ drink.price }}</span>
        </li>
      </transition-group>
    </div>

    <p class="note">
      Dein Lieblings-Cocktail ist nicht dabei? <br>Frag uns gerne! :)
    </p>
  </section>

  <!--   0 Alk-->
  <section class="drinks-menu-section">
    <header class="drinks-header">
      <h1 class="drinks-title">0%</h1>
      <p class="drinks-subtitle">Alkoholfreie Optionen</p>
    </header>
    <div class="drinks-content" :class="nonAlcoholic && 'non-alcoholic'">
      <transition-group name="drink" tag="ul" class="drinks-list">
        <li v-for="drink in nonAlcoholic ? zeroAlc.filter(d => !d.alcoholic) : zeroAlc" :key="drink.name"
            class="drinks-item">
          <div class="drink-text">
            <span class="drinks-name">{{ drink.name }}
            <sup v-if="drink.allergens" class="allergen-indices">{{ drink.allergens.join(',') }}</sup>
            </span>
          </div>
          <span class="drinks-price">{{ drink.price }}</span>
        </li>
      </transition-group>
    </div>
  </section>
  <br>
  <br>
  <div class="allergen-section">
    <h3>Allergene und Zusatzstoffe</h3>
    <p>
      In unseren Gerichten sind teilweise Zusatzstoffe und allergene Stoffe (wie z.b. Milch,
      Senf, Gluten etc.) enthalten. Bei weiteren Fragen zu den Produkten wenden Sie sich
      bitte an unser Personal.
    </p>
    <table class="allergen-table">
      <thead>
      <tr>
        <th>Index</th>
        <th>Hinweis</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td>1</td>
        <td>mit Farbstoff</td>
      </tr>
      <tr>
        <td>2</td>
        <td>mit Konservierungsstoff</td>
      </tr>
      <tr>
        <td>3</td>
        <td>mit Geschmacksverstärker</td>
      </tr>
      <tr>
        <td>4</td>
        <td>geschwefelt / enthält Sulfit</td>
      </tr>
      <tr>
        <td>5</td>
        <td>geschwärzt</td>
      </tr>
      <tr>
        <td>6</td>
        <td>mit Phosphat</td>
      </tr>
      <tr>
        <td>7</td>
        <td>mit Süßungsmitteln</td>
      </tr>
      <tr>
        <td>8</td>
        <td>koffeinhaltig</td>
      </tr>
      <tr>
        <td>9</td>
        <td>enthält Gluten (Weizen)</td>
      </tr>
      <tr>
        <td>10</td>
        <td>enthält Gluten (Gerste)</td>
      </tr>
      <tr>
        <td>11</td>
        <td>enthält Ei</td>
      </tr>
      <tr>
        <td>12</td>
        <td>enthält Nüsse / Erdnüsse</td>
      </tr>
      <tr>
        <td>13</td>
        <td>enthält Laktose / Milch</td>
      </tr>
      <tr>
        <td>14</td>
        <td>enthält Sellerie</td>
      </tr>
      <tr>
        <td>15</td>
        <td>enthält Senf</td>
      </tr>
      <tr>
        <td>24</td>
        <td>chininhaltig</td>
      </tr>
      <tr>
        <td>25</td>
        <td>enthält Gluten (Roggen)</td>
      </tr>
      </tbody>
    </table>
  </div>

</template>

<script setup lang="ts">
import {ref} from "vue";

const nonAlcoholic = ref(false);
const showTopToast = ref(false);

function toggleNonAlcoholic() {
  nonAlcoholic.value = !nonAlcoholic.value;
}

const beers = [
  {
    name: "Krombacher Radler",
    volume: "0,33l",
    price: "3,5€",
    category: "Bier",
    alcoholic: true,
    allergens: [4, 10],
    available: false,
  },
  {
    name: "Helles vom Fass 0,2",
    volume: "0,2l",
    price: "2,9€",
    category: "Bier",
    alcoholic: true,
    allergens: [4, 10]
  },
  {
    name: "Helles vom Fass 0,4",
    volume: "0,4l",
    price: "5,5€",
    category: "Bier",
    alcoholic: true,
    allergens: [4, 10]
  },
  {
    name: "Krombacher Weizen",
    volume: "0,50l",
    price: "5,9€",
    category: "Bier",
    alcoholic: true,
    allergens: [4, 9, 10], available: false
  },
  {
    name: "Krombacher Weizen 0,0%",
    volume: "0,50l",
    price: "5,5€",
    category: "Bier",
    alcoholic: false,
    allergens: [4, 9, 10]
  },
  {
    name: "Estrella de Galicia Especial",
    volume: "0,20l",
    price: "2,5€",
    category: "Bier",
    alcoholic: true,
    allergens: [4, 10],
    available: false,
  },
  {
    name: "Krombacher Pils (0,0%)",
    volume: "0,33l",
    price: "3,5€",
    category: "Bier",
    alcoholic: false,
    allergens: [4, 10]
  },
  {
    name: "Brinkshoff's N°1",
    volume: "0,33l",
    price: "3,5€",
    category: "Bier",
    alcoholic: true,
    allergens: [4, 10],
    available: false,
  },
  {
    name: "San Miguel",
    volume: "0,33l",
    price: "3,9€",
    category: "Bier",
    alcoholic: true,
    allergens: [4, 10],
    available: false
  },
  {
    name: "Krombacher Pils",
    volume: "0,33l",
    price: "3,9",
    category: "Bier",
    alcoholic: true,
    allergens: [4, 10],
    available: false,
  },
  {
    name: "Estrella de Galicia",
    volume: "0,33l",
    price: "3,9€",
    category: "Bier",
    alcoholic: true,
    allergens: [4, 10],
    available: false
  }
];

const softdrinks = [
  {
    name: "Eistee von Rauch",
    volume: "0,33l",
    price: "3,9€",
    category: "Softdrink",
    alcoholic: false,
    allergens: [1, 2, 8]
  },
  {
    name: "Bio Saftschorle von Rauch",
    volume: "0,33l",
    price: "3,9€",
    category: "Softdrink",
    alcoholic: false,
    allergens: []
  },
  {name: "Thomas Henry", volume: "0,20l", price: "2,5€", category: "Softdrink", alcoholic: false, allergens: [24]},
  {
    name: "Coca Cola Zero",
    volume: "0,33l",
    price: "3,9€",
    category: "Softdrink",
    alcoholic: false,
    allergens: [1, 7, 8]
  },
  {
    name: "Wasser Classic/Naturell",
    volume: "0,75l",
    price: "6,9€",
    category: "Softdrink",
    alcoholic: false,
    allergens: []
  },
  {
    name: "Vital-Wasser",
    volume: "1l Karaffe",
    price: "6,9€",
    category: "Softdrink",
    alcoholic: false,
    allergens: [],
    neu: true
  }
];

const cocktails = [
  {name: "Yuzu Sour", price: "10,5€", category: "Cocktail", alcoholic: true, allergens: [11]},
  {name: "Espresso Martini", price: "10,5€", category: "Cocktail", alcoholic: true, allergens: [8, 13]},
  {name: "Whisky Sour", price: "10,5€", category: "Cocktail", alcoholic: true, allergens: [11]},
  {name: "Cosmopolitan", price: "10,5€", category: "Cocktail", alcoholic: true, allergens: []},
  {name: "Skinny Bitch", price: "7,5€", category: "Cocktail", alcoholic: true, allergens: []},
];

const spritz = [
  {name: "*Limoncello", price: "8,5€", category: "Cocktail", alcoholic: true, allergens: [1, 4]},
  {name: "*Aperol", price: "8,5€", category: "Cocktail", alcoholic: true, allergens: [1, 4]},
  {name: "Sarti", price: "8,5€", category: "Cocktail", alcoholic: true, allergens: [1, 4]},
  {name: "Yuzu", price: "8,5€", category: "Cocktail", alcoholic: true, allergens: [1, 4]},
];

const no3 = [
  {name: "Negroni", price: "10,5€", category: "Cocktail", alcoholic: true, allergens: [4]},
  {name: "Gin Fizz", price: "10,5€", category: "Cocktail", alcoholic: true, allergens: [11]},
  {name: "Gin Tonic", price: "7,9€", category: "Cocktail", alcoholic: true, allergens: [24]},
  {name: "Tom Collins", price: "7,5€", category: "Cocktail", alcoholic: true, allergens: []}
];

const zeroAlc = [
  {name: "Gin Fizz", price: "9€", category: "Cocktail", alcoholic: false, allergens: [11]},
  {name: "Gin Tonic", price: "7,5€", category: "Cocktail", alcoholic: false, allergens: [24]},
  {name: "Aperol Spritz", price: "7,5€", category: "Cocktail", alcoholic: false, allergens: [1, 4]},
  {name: "Limoncello Spritz", price: "7,5€", category: "Cocktail", alcoholic: false, allergens: [1, 4]},
];
</script>


<style lang="scss" scoped>
@use "../assets/styles/main" as *;

.drinks-menu-section {
  background-color: $background-color;
  color: $text-color;
  font-family: $font-family;
  padding: 2rem 1rem 0 1rem;
  max-width: 90%;
  margin: 10% auto;
  border: 2px solid $accent-color;
  border-radius: 8px;
  position: relative;
  margin-bottom: 20%;
}

.drinks-header {
  text-align: center;
  position: absolute;
  width: 100%;
  top: -34px;
}

.drinks-title {
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  background: $background-color;
  width: min-content;
  margin: 0;
  padding: 0 1rem;
  color: $accent-color;
  font-size: 2rem;
  font-family: 'King Red';
  font-weight: normal;
}

.drinks-subtitle {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  color: $accent-color;
  text-align: center;
}

.drinks-content {
  overflow-y: auto;
  padding: 1rem;
  border-radius: 5px;
}

.drinks-list {
  list-style: none;
  margin: 0;
  padding: 0;
  margin-bottom: 1.5rem;
}

.drinks-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  position: relative;

  .drink-text {
    display: flex;
    flex-direction: column;
    position: relative;

    .drinks-name {
      font-size: 1rem;

      .allergen-indices {
        font-size: 10px;
      }
    }

    .new-label {
      position: absolute;
      top: 0.25rem;
      right: -50px;
      background: linear-gradient(135deg, #2ecc71, #27ae60);
      color: #fff;
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 0.2rem 0.6rem;
      border-radius: 0.25rem;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
      transform: rotate(10deg);
      transform-origin: top right;
      transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
      opacity: .5;


      .drinks-item:hover & {
        transform: rotate(0deg) scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      }
    }

    .drinks-description {
      font-size: 0.7rem;
      font-style: italic;
    }

  }

  .drinks-price {
    font-size: 1rem;
    color: $accent-color;
  }
}

.drink-enter-active, .drink-leave-active {
  transition: max-height 0.41s ease-in-out, opacity 0.41s ease-in-out;
  overflow: hidden;
}

.drink-enter-from, .drink-leave-to {
  max-height: 0;
  opacity: 0;
}

.drink-enter-to, .drink-leave-from {
  opacity: 1;
}


.no3-desc {
  display: flex;
  align-items: center;
  gap: .5rem;
  padding-bottom: .5rem;
}

.no3bottle {
  position: absolute;
  top: 33%;
  left: 50%;
  height: 120px;
}

.allergen-section {
  padding: 1rem;
}

.allergen-table {
  width: 100%;
  max-width: 600px;
  margin: 2rem auto;
  border-collapse: collapse;
  font-family: sans-serif;
  font-size: 0.95rem;
  background: rgba(255, 255, 255, 0.62);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  color: black;
}

.allergen-table thead {
  background-color: rgba(244, 244, 244, 0.79);
}

.allergen-table th,
.allergen-table td {
  padding: 10px 14px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.allergen-table th {
  color: #333;
  font-weight: 600;
}

.allergen-table tbody tr:nth-child(even) {
  background-color: rgba(250, 250, 250, 0.54);
}

.allergen-table tbody tr:hover {
  background-color: #f0f0f0;
}

@media (max-width: 600px) {
  .allergen-table {
    font-size: 0.85rem;
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
  background: #221d32;
  color: #ceaa72;
  border: 1px solid #ceaa72;
  border-radius: 6px;
  padding: .5rem .75rem;
  margin: .5rem 1rem 0;
}

.toast-close {
  background: transparent;
  border: none;
  color: #ceaa72;
  font-size: 1.2rem;
  line-height: 1;
  cursor: pointer;
}
</style>
