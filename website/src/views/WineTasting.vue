<template>
  <section class="tasting-page">
    <header class="tasting-header">
      <h1 class="tasting-title">Willkommen zur Herbst Degustation im Casa Vazquez!</h1>
      <p class="tasting-sub">Sechs Weine, sechs Geschichten – scroll dich durch unsere Auswahl.</p>
      <p class="tasting-sub">Die Weine sind jeweils Flaschenweise für <b>44,50€</b> erhältlich.</p>
    </header>

    <div class="tasting-map" ref="mapEl" role="img" aria-label="Karte der Weinregionen"></div>
    <div class="tasting-map-legend">
      <div class="legend-title">Kartenlegende</div>
      <ul>
        <li v-for="(p, i) in mapPoints" :key="p.name">
          <button class="legend-item" @click="flyToIndex(i)">
            <span class="legend-pin">{{ i + 1 }}</span>
            <span class="legend-text">
              <strong>{{ p.name }}</strong>
              <small>{{ p.loc }}</small>
            </span>
          </button>
        </li>
      </ul>
    </div>

    <div class="tasting-sections">
      <section v-for="(w, i) in wines" :key="i" class="tasting-section">
        <div class="tasting-content">
          <div class="tasting-text">
            <h2 class="wine-name">{{ w.name }}</h2>
            <p class="wine-story">{{ w.story }}</p>
            <p v-if="w.note" class="wine-note">{{ w.note }}</p>
          </div>
          <div class="tasting-image">
            <img :src="w.image" :alt="w.name" loading="lazy" referrerpolicy="no-referrer" @error="hideOnError($event)" />
          </div>
        </div>
      </section>
    </div>
  </section>
  
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import markerIcon2xUrl from 'leaflet/dist/images/marker-icon-2x.png?url';
import markerIconUrl from 'leaflet/dist/images/marker-icon.png?url';
import markerShadowUrl from 'leaflet/dist/images/marker-shadow.png?url';

type TastingWine = { name: string; story: string; image: string; note?: string };

function hideOnError(e: Event) {
  const el = e.target as HTMLImageElement;
  if (el) el.style.display = 'none';
}

// Resolve local images (added under src/assets/images/tinified (6)) via Vite
const imgVette = new URL('../assets/images/tinified (6)/vette.jpg', import.meta.url).href;
const imgJosePariente = new URL('../assets/images/tinified (6)/josepariente.jpg', import.meta.url).href;
const imgElenaWalch = new URL('../assets/images/tinified (6)/elenawalch.jpg', import.meta.url).href;
const imgTerlan = new URL('../assets/images/tinified (6)/terlan.jpg', import.meta.url).href;
const imgPompaelo = new URL('../assets/images/tinified (6)/pompaelo.jpg', import.meta.url).href;
const imgNounat = new URL('../assets/images/tinified (6)/nounat.jpg', import.meta.url).href;

const wines: TastingWine[] = [
  {
    name: 'Pompaelo Blanc de Noir',
    story:
      'Weiß gekeltert aus roten Garnacha-Trauben: hell, saftig und fruchtbetont, mit Anklängen an rote Beeren, Pfirsich und feine Würze. Ein ungewöhnlicher, animierender Wein mit viel Charme – perfekt als Aperitif oder zu leichten Tapas.',
    image: imgPompaelo,
    note: 'Erhältlich bei K&D WineStories Münster.',
  },
  {
    name: 'Vette San Leonardo 2024',
    story:
      'Ein Sauvignon Blanc aus den kühlen Höhenlagen des Trentino. Klare Alpenfrische, Noten von Zitrus, Stachelbeere und Bergkräutern, unterlegt von einer lebendigen, geradlinigen Säure. Der Ausbau im Edelstahltank bewahrt die kristallklare Frucht und eine salzige Mineralität – präzise, kühl und sehr trinkanimierend.',
    image: imgVette,
  },
  {
    name: 'José Pariente 2024 Sauvignon Blanc',
    story:
      'Aus Rueda: duftige Aromen von Limette, Grapefruit und Stachelbeere, dazu feine Kräuter- und Heunoten. Am Gaumen saftig und frisch, mit ziselierter Säure und klarer Frucht. Ein moderner, spannkräftiger Sauvignon, der trotzdem niemals laut wirkt.',
    image: imgJosePariente,
  },
  {
    name: 'Elena Walch Pinot Bianco 2024',
    story:
      'Südtirol in Reinkultur: kühle Eleganz, weiße Blüten, grüner Apfel und ein Hauch Zitruszeste. Straff und schnörkellos mit feiner Mineralität und klarer Linie – ein Pinot Bianco, der Leichtigkeit und Tiefe verbindet.',
    image: imgElenaWalch,
  },
  {
    name: 'Terlan Chardonnay 2024 Alto Adige DOC',
    story:
      'Der Klassiker der Kellerei Terlan: zarte Aromen von Apfel, Birne und etwas Zitrus, cremig untermalt von feiner Textur und einer präzisen Säureader. Die typische Terlaner Mineralität sorgt für Länge und glasklare Kontur.',
    image: imgTerlan,
  },

  {
    name: 'Nounat 2024 – Binigrau Mallorca',
    story:
      'Mallorca-Highlight: eine elegante Cuvée, häufig aus Prensal Blanc und Chardonnay. Reife gelbe Frucht, zarte Kräuter der Insel und eine cremige Textur treffen auf salzige Frische. Sonnig, vielschichtig und dennoch erstaunlich balanciert – mediterraner Charakter mit Tiefgang.',
    image: imgNounat,
  },
];

type MapPoint = { name: string; loc: string; lat: number; lng: number };
const mapPoints: MapPoint[] = [
  { name: 'Pompaelo Blanc de Noir', loc: 'Navarra, Spanien', lat: 42.812, lng: -1.646 },
  { name: 'José Pariente 2024 Sauvignon Blanc', loc: 'Rueda, Spanien', lat: 41.412, lng: -4.959 },
  { name: 'Nounat 2024 – Binigrau', loc: 'Mallorca, Spanien', lat: 39.569, lng: 2.650 },
  { name: 'Vette San Leonardo 2024', loc: 'Trentino, Italien', lat: 45.757, lng: 10.962 },
  { name: 'Elena Walch Pinot Bianco 2024', loc: 'Südtirol, Italien', lat: 46.342, lng: 11.238 },
  { name: 'Terlan Chardonnay 2024 Alto Adige DOC', loc: 'Südtirol (Alto Adige), Italien', lat: 46.517, lng: 11.248 },
];

const mapEl = ref<HTMLDivElement | null>(null);
let map: L.Map | null = null;
let markers: L.Marker[] = [];

onMounted(() => {
  if (!mapEl.value) return;
  const DefaultIcon = L.icon({
    iconRetinaUrl: markerIcon2xUrl,
    iconUrl: markerIconUrl,
    shadowUrl: markerShadowUrl,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    tooltipAnchor: [16, -28],
    shadowSize: [41, 41],
  });
  (L.Marker.prototype as any).options.icon = DefaultIcon;
  map = L.map(mapEl.value, { zoomControl: true });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap-Mitwirkende',
    maxZoom: 18,
  }).addTo(map);
  markers = mapPoints.map((p, i) => {
    const icon = L.divIcon({
      html: `<div class="map-pin">${i + 1}</div>`,
      className: 'map-pin-wrap',
      iconSize: [28, 28],
      iconAnchor: [14, 28]
    });
    return L.marker([p.lat, p.lng], { icon }).bindPopup(`<b>${p.name}</b><br>${p.loc}`);
  });
  const group = L.featureGroup(markers).addTo(map);
  map.fitBounds(group.getBounds().pad(0.3));
});

onBeforeUnmount(() => {
  if (map) {
    map.remove();
    map = null;
  }
});

function flyToIndex(i: number) {
  if (!map || !markers[i]) return;
  map.setView(markers[i].getLatLng(), 8, { animate: true });
  markers[i].openPopup();
}
</script>

<style lang="scss" scoped>
@use "../assets/styles/main" as *;

.tasting-page {
  background-color: $background-color;
  color: $text-color;
  font-family: $font-family;
  max-width: 100%;
}

.tasting-header {
  text-align: center;
  padding: 2rem 1rem 2rem;
}

.tasting-map {
  height: 33vh;
  margin: 0 1rem 2rem;
  border: 2px solid $accent-color;
  border-radius: 10px;
  overflow: hidden;
}

.tasting-map-legend {
  margin: 0 1rem 2rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: .5rem .75rem;
}

.tasting-map-legend .legend-title {
  color: $accent-color;
  font-weight: bold;
  margin-bottom: .25rem;
}

.tasting-map-legend ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: .25rem .5rem;
}

@media (min-width: 720px) {
  .tasting-map-legend ul {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.legend-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: .5rem;
  background: transparent;
  color: inherit;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: .35rem .5rem;
  text-align: left;
}

.legend-item:hover {
  border-color: $accent-color;
}

.legend-pin {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: $accent-color;
  color: #111;
  font-weight: 700;
  font-size: 12px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.25);
}

.legend-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.legend-text small {
  opacity: .75;
}

:deep(.map-pin-wrap) {
  background: transparent;
  border: none;
}

:deep(.map-pin) {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: $accent-color;
  color: #111;
  font-weight: 700;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.35);
  border: 2px solid #fff;
}

.tasting-title {
  color: $accent-color;
  font-family: 'King Red';
  font-size: 2rem;
  font-weight: normal;
}

.tasting-sub {
  opacity: .9;
}

.tasting-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 0 1rem 4rem;
}

.tasting-section {
  border: 2px solid $accent-color;
  border-radius: 10px;
  min-height: calc(100vh - 9rem);
  display: grid;
  grid-template-columns: 1fr;
  overflow: hidden;
}

@media (min-width: 720px) {
  .tasting-section {
    grid-template-columns: 1fr 1fr;
    min-height: 80vh;
  }
}

.tasting-content {
  display: contents;
}

.tasting-text {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: .75rem;
}

.wine-name {
  color: $accent-color;
  font-family: 'King Red';
  font-size: 1.5rem;
  margin: 0;
}

.wine-story {
  line-height: 1.6;
}

.wine-note {
  font-style: italic;
  color: $accent-color;
}

.tasting-image {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.03);
}

.tasting-image img {
  max-height: 70vh;
  max-width: 90%;
  object-fit: contain;
}
</style>
