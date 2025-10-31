<template>
  <main>
    <header class="hero">
      <h1>Casa Vazquez – Weinbar & Cocktails in Münster</h1>
    </header>

    <!-- Announcement Modal -->
    <!-- <BaseModal v-model="showAnnouncement">
      <div style="display:flex;flex-direction:column;gap:0.75rem">
        <h2 style="margin:0">Saludos desde Madrid</h2>
        <p style="margin:0">
          Diesen Samstag bekommt ihr zu jedem Getränk eine kleine Tapita – ganz wie ihr es aus der Hauptstadt Spaniens kennt.
        </p>
      </div>
    </BaseModal> -->

    <section class="tile-navigation" aria-label="Navigation zu Speisekarten">
      <router-link class="nav-link" to="/vino">
        <div class="navigation-tile">Weine</div>
      </router-link>
      <router-link class="nav-link" to="/drinks">
        <div class="navigation-tile">Getränke</div>
      </router-link>
      <router-link class="nav-link" to="/snacks">
        <div class="navigation-tile">Snacks</div>
      </router-link>
      <router-link class="nav-link" to="/showroom">
        <div class="navigation-tile">Galerie</div>
      </router-link>
      <router-link class="nav-link" to="/wine-tasting">
        <div class="navigation-tile">Tasting</div>
      </router-link>
    </section>
    <br >
    <br >
    <section aria-label="Aktuelle Neuigkeiten">
      <h2>Aktuelles aus der Casa Vazquez</h2>
      <div class="landing-page container">
        <NotificationCard
            v-for="note in combinedNotifications"
            :key="note.title"
            :title="note.title"
            :created-at="note.createdAt"
            :image="note.image"
            :text="note.text"
            :roundedImage="note.roundedImage"
            :linkText="note.linkText"
            :linkTo="note.linkTo"
        />
      </div>
    </section>

    <section aria-label="Über Casa Vazquez">
      <h2>Willkommen bei unserer Bar in Münster!</h2>
      <p>
        Du warst noch nie bei uns und fragst dich, was wir bieten?<br/>
        Wir laden zum gemütlichen Verweilen an der Warendorfer Straße ein. <br/>
        Leckere Drinks und Snacks und eine Auswahl an besonderen Weinen
        versüßen dir den Feierabend. <br/>
        Ganz ungezwungen – wie bei Freunden.
      </p>
    </section>

    <div class="impressum">
      <h1>Impressum</h1>
      <p>
        Angaben gemäß § 5 TMG:<br>
        Casa Vazquez Münster – José Benjamin Marco Joaquin Guerrero Vazquez<br>
        Warendorfer Str 113<br>
        48145 Münster<br>
        Deutschland
      </p>
      <p>Ust: 33750944916 NAST1</p>
      <p>
        Kontakt:<br>
        Telefon: +49 176 4278 7953<br>
        E-Mail: info@casavazquez.de
      </p>
      <p>
        Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV:<br>
        José Benjamin Marco Joaquin Guerrero Vazquez (siehe Anschrift)
      </p>
      <p>
        Haftungsausschluss (Disclaimer):
      </p>
      <p>
        Haftung für Inhalte:<br>
        Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für eigene Inhalte auf diesen Seiten nach den allgemeinen
        Gesetzen verantwortlich. Nach §§ 8 bis 10 TMG sind wir als Diensteanbieter jedoch nicht verpflichtet,
        übermittelte
        oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige
        Tätigkeit hinweisen. Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen bleiben hiervon
        unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt der Kenntnis einer konkreten
        Rechtsverletzung möglich.
      </p>
      <p>
        Haftung für Links:<br>
        Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb
        können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist
        stets
        der jeweilige Anbieter oder Betreiber der Seiten verantwortlich.
      </p>
      <p>
        Urheberrecht:<br>
        Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen
        Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen
        des
        Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.
      </p>

    </div>
      <div v-if="false" class="easter-egg" @click="handleClick" :style="{ transform: 'scale(' + scale + ')' }" :class="{ 'shake': isShaking }">
        <template v-if="clickCount < 5">
          <img :src="osterei" alt="Osertei" class="egg-icon" />
        </template>
        <template v-else>
          <div class="voucher">
            <h2>Gutschein!</h2>
            <p>Herzlichen Glückwunsch – Du hast ein Osterei gefunden! Zeig uns diesen Gutschein und du erhältst ein gratis Osterbier!</p>
            <p>(pro Person 1x einlösbar)</p>
          </div>
        </template>
      </div>

    <footer>
      <div class="sources-link">
        Icons by <a href="https://icons8.com/" target="_blank" rel="noopener">icons8.com</a>
      </div>
    </footer>
  </main>
</template>

<script setup lang="ts">
import {ref, onMounted} from "vue";
import {notifications} from "../data/notifications.ts";
import NotificationCard from "../components/NotificationCard.vue";
import osterei from "../assets/images/icons8-easter-64.png";

const extraNotes = [
  {
    title: "Live Musik im Casa Vazquez. Ohne Reservierung. Eifnach vorbeikommen und genießen",
    text: "Entspannte Live-Musik Abende mit lokalen Künstlern. Kommen Sie vorbei und genießen Sie gute Musik bei einem Glas Wein.",
    createdAt: "2025-10-26"
  },
  {
    title: "Live Musik im Casa Vazquez. Ohne Reservierung. Eifnach vorbeikommen und genießen",
    text: "Entspannte Live-Musik Abende mit lokalen Künstlern. Kommen Sie vorbei und genießen Sie gute Musik bei einem Glas Wein.",
    createdAt: "2025-11-04"
  },
  {
    title: "Live Musik im Casa Vazquez. Ohne Reservierung. Eifnach vorbeikommen und genießen",
    text: "Entspannte Live-Musik Abende mit lokalen Künstlern. Kommen Sie vorbei und genießen Sie gute Musik bei einem Glas Wein.",
    createdAt: "2025-12-02"
  }
];

const combinedNotifications = [...extraNotes, ...notifications] as typeof notifications;

const clickCount = ref(0);
const scale = ref(1);
const isShaking = ref(false);

function handleClick() {
  if (clickCount.value < 2) {
    clickCount.value++;
    scale.value *= 1.21;
  } else {
    clickCount.value++;
    scale.value = 1;
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth",
    });
  }

  isShaking.value = true;
  setTimeout(() => {
    isShaking.value = false;
  }, 500);
}

onMounted(() => {
  // Announcement currently disabled
});
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";

h1, h2, h3 {
  font-family: "King Red";
  text-align: center;
  font-weight: 100;
  color: $accent-color;
  font-style: italic;
}

.landing-page {
  padding: 1rem 0;

  &.container {
    display: flex;
    padding: 0.5rem;
    flex-direction: column;
  }
}

.tile-navigation {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  justify-content: center;
  padding: 1rem;
  max-width: 600px;
  margin: 0 auto;

  .nav-link {
    text-decoration: none;
  }

  .navigation-tile {
    aspect-ratio: 1 / 1;
    background: #1e1e2f;
    border: 1.5px solid #ceaa72;
    border-radius: 1rem;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #ceaa72;
    font-family: "King Red", serif;
    font-size: 1.2rem;
    transition: transform 0.2s ease, background 0.3s;

    &:hover {
      background: #2a2a3f;
      transform: scale(1.05);
    }
  }
}


.sources-link {
  padding: 1rem;
  text-align: center;

  a {
    text-decoration: underline;
  }
}

.impressum {
  margin-top: 5rem;
  padding: 1rem;
  font-size: 0.9rem;

  address {
    font-style: normal;
    line-height: 1.6;
  }
}

.egg-icon {
  width: 20px;
  height: auto;
}

.voucher {
  border: 2px dashed #ceaa72;
  padding: 1rem;
  text-align: center;
  background-color: #fff;
  font-size: 70%;
  color: #ceaa72;
}

.voucher h2 {
  margin: 0;
}

.voucher p {
  margin: 0.5rem 0 0;
}

@keyframes shake {
  0%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(5deg);
  }
  75% {
    transform: rotate(-5deg);
  }
}

.shake {
  animation: shake 0.2s;
}
</style>
