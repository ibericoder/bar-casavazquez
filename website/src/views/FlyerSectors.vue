<template>
  <div class="flyer-sectors">
    <div class="map-wrapper">
      <div ref="mapContainer" class="map" aria-label="Liefergebiets-Karte"></div>
    </div>
    <aside class="control-panel">
      <header>
        <h1>Flyer-Sektoren</h1>
        <p>Plane Zustellungen, markiere erledigte Bereiche und verfolge dein Team live.</p>
        <button type="button" class="reset" @click="resetServed" :disabled="allSectorsOpen">
          Markierungen zurücksetzen
        </button>
      </header>

      <div v-if="teams.length" class="team-selector">
        <label for="team-select">Team</label>
        <select id="team-select" v-model="activeTeam">
          <option v-for="team in teams" :key="team" :value="team">{{ team }}</option>
        </select>
      </div>

      <section class="tracking-card">
        <div class="tracking-header">
          <h2>Live-Tracking</h2>
          <label>
            <input v-model="autoCenter" type="checkbox" />
            Karte folgt Team
          </label>
        </div>
        <p v-if="!geolocationSupported" class="tracking-status error">
          Dein Browser unterstützt keine Geolokalisierung.
        </p>
        <template v-else>
          <p class="tracking-status" :class="{ active: trackingActive, error: trackingError }">
            {{ trackingStatusText }}
          </p>
          <div class="tracking-actions">
            <button type="button" @click="toggleTracking" :disabled="!geolocationSupported">
              {{ trackingActive ? 'Tracking stoppen' : 'Tracking starten' }}
            </button>
            <button type="button" @click="clearHistory" :disabled="positionHistory.length === 0">
              Verlauf löschen
            </button>
          </div>
          <ul v-if="positionHistory.length" class="history-stats">
            <li>Letzte Position: {{ formatLatLng(userPosition) }}</li>
            <li>Punkte im Verlauf: {{ positionHistory.length }}</li>
          </ul>
        </template>
      </section>

      <div class="sectors">
        <section v-for="sector in sectors" :key="sector.id" class="sector-card">
          <div class="card-header">
            <div class="title-group">
              <span class="badge">{{ sector.id }}</span>
              <input v-model="sector.name" class="name-input" />
            </div>
            <span class="status" :class="{ served: sector.served }">
              {{ sector.served ? 'Erledigt' : 'Offen' }}
            </span>
          </div>
          <p class="area-hint">Grenzen orientieren sich an Kreuzungen rund um die Warendorfer Straße.</p>
          <p v-if="sector.servedBy" class="team-info">Übernommen von {{ sector.servedBy }}</p>

          <div class="field">
            <label>Farbe</label>
            <input v-model="sector.color" type="color" />
          </div>

          <details class="coords" v-if="sector.coordinates.length">
            <summary>Koordinaten anzeigen</summary>
            <ul>
              <li v-for="(point, index) in sector.coordinates" :key="index">
                {{ formatLatLng(point) }}
              </li>
            </ul>
          </details>

          <div class="toggles">
            <label>
              <input v-model="sector.visible" type="checkbox" />
              Sichtbar
            </label>
            <label>
              <input :checked="sector.served" type="checkbox" @change="event => handleServedChange(sector, event)" />
              Abgedeckt
            </label>
          </div>
        </section>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import L from 'leaflet';
import type { LatLngBoundsExpression } from 'leaflet';
import 'leaflet/dist/leaflet.css';

type LatLngTuple = [number, number];

interface SectorConfig {
  id: string;
  name: string;
  color: string;
  coordinates: LatLngTuple[];
  visible: boolean;
  served: boolean;
  servedBy: string | null;
}

const mapCenter: LatLngTuple = [51.962714, 7.644085];
const storageKey = 'cv-admin-sectors-v2';
const teamStorageKey = 'cv-admin-active-team';
const historyKeyPrefix = 'cv-admin-history-';
const defaultTeams = ['Team Casa', 'Team Flyer', 'Team Nacht'];

const mapContainer = ref<HTMLDivElement | null>(null);
const mapInstance = ref<L.Map | null>(null);
const sectorLayerGroup = ref<L.LayerGroup | null>(null);
const trackingLayerGroup = ref<L.LayerGroup | null>(null);

const sectors = ref<SectorConfig[]>(loadSectors());
const teams = ref<string[]>([...defaultTeams]);
const activeTeam = ref<string>(loadActiveTeam());
const positionHistory = ref<LatLngTuple[]>(loadHistory(activeTeam.value));
const userPosition = ref<LatLngTuple | null>(
  positionHistory.value.length ? positionHistory.value[positionHistory.value.length - 1] : null
);

const geolocationSupported = typeof window !== 'undefined' && 'geolocation' in navigator;
const trackingActive = ref(false);
const trackingError = ref<string | null>(null);
const autoCenter = ref(true);
const watchId = ref<number | null>(null);

const trackingStatusText = computed(() => {
  if (!geolocationSupported) {
    return 'Geolokalisierung nicht verfügbar';
  }
  if (trackingError.value) {
    return `Fehler: ${trackingError.value}`;
  }
  return trackingActive.value ? 'Tracking aktiv' : 'Tracking inaktiv';
});

const allSectorsOpen = computed(() => sectors.value.every(sector => !sector.served));

onMounted(() => {
  if (!mapContainer.value) {
    return;
  }
  const map = L.map(mapContainer.value, {
    center: mapCenter,
    zoom: 16,
    maxZoom: 19,
  });
  mapInstance.value = map;

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap-Mitwirkende',
  }).addTo(map);

  sectorLayerGroup.value = L.layerGroup().addTo(map);
  trackingLayerGroup.value = L.layerGroup().addTo(map);

  renderSectors(true);
  updateTrackingLayers(true);
});

onBeforeUnmount(() => {
  stopTracking();
  if (mapInstance.value) {
    mapInstance.value.remove();
  }
});

watch(
  sectors,
  newValue => {
    const normalized = newValue.map(sector => ({
      ...sector,
      servedBy: sector.served ? sector.servedBy ?? activeTeam.value ?? null : null,
    }));
    const mutated = normalized.some((sector, index) => sector.servedBy !== newValue[index].servedBy);
    if (mutated) {
      sectors.value = normalized;
      return;
    }
    persistSectors(normalized);
    renderSectors();
  },
  { deep: true }
);

watch(activeTeam, value => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(teamStorageKey, value);
  }
  positionHistory.value = loadHistory(value);
  userPosition.value = positionHistory.value.length
    ? positionHistory.value[positionHistory.value.length - 1]
    : null;
  updateTrackingLayers(true);
});

watch(positionHistory, () => {
  persistHistory();
  updateTrackingLayers();
});

watch(userPosition, () => {
  updateTrackingLayers();
});

function renderSectors(fit = false) {
  const group = sectorLayerGroup.value;
  const map = mapInstance.value;
  if (!group || !map) {
    return;
  }
  group.clearLayers();

  const fitPoints: LatLngTuple[] = [];

  sectors.value.forEach(sector => {
    if (!sector.visible || sector.coordinates.length < 3) {
      return;
    }
    const fillColor = sector.served ? mixWithWhite(sector.color, 0.65) : sector.color;
    const fillOpacity = sector.served ? 0.18 : 0.45;
    const polygon = L.polygon(sector.coordinates, {
      color: sector.color,
      weight: 2,
      fillColor,
      fillOpacity,
      dashArray: sector.served ? '6 6' : undefined,
    });

    const labelText = `<span>${sector.name}</span>${sector.servedBy ? `<small>${sector.servedBy}</small>` : ''}`;
    const label = L.marker(polygon.getBounds().getCenter(), {
      icon: L.divIcon({
        className: 'sector-label',
        html: labelText,
      }),
      interactive: false,
    });

    group.addLayer(polygon);
    group.addLayer(label);

    if (fit) {
      fitPoints.push(...sector.coordinates);
    }
  });

  if (fit && fitPoints.length) {
    map.fitBounds(fitPoints as LatLngBoundsExpression, { padding: [20, 20] });
  }
}

function updateTrackingLayers(fit = false) {
  const trackingGroup = trackingLayerGroup.value;
  const map = mapInstance.value;
  if (!trackingGroup || !map) {
    return;
  }
  trackingGroup.clearLayers();

  let historyBounds: L.LatLngBounds | null = null;

  if (positionHistory.value.length > 1) {
    const polyline = L.polyline(positionHistory.value, {
      color: '#f06595',
      weight: 4,
      opacity: 0.8,
    });
    trackingGroup.addLayer(polyline);
    historyBounds = polyline.getBounds();
  }

  if (userPosition.value) {
    const marker = L.circleMarker(userPosition.value, {
      radius: 8,
      color: '#ff6b6b',
      weight: 2,
      fillColor: '#ffffff',
      fillOpacity: 0.9,
    });
    trackingGroup.addLayer(marker);

    if (autoCenter.value) {
      map.setView(userPosition.value, Math.max(map.getZoom(), 17));
    }
  }

  if (fit) {
    if (historyBounds) {
      map.fitBounds(historyBounds.pad(0.2));
    } else if (userPosition.value) {
      map.setView(userPosition.value, 17);
    }
  }
}

function loadSectors(): SectorConfig[] {
  if (typeof window === 'undefined') {
    return createDefaultSectors();
  }
  const stored = localStorage.getItem(storageKey);
  if (!stored) {
    return createDefaultSectors();
  }
  try {
    const parsed = JSON.parse(stored) as SectorConfig[];
    if (Array.isArray(parsed) && parsed.every(isValidSector)) {
      return parsed;
    }
    return createDefaultSectors();
  } catch {
    return createDefaultSectors();
  }
}

function persistSectors(value: SectorConfig[]) {
  if (typeof window === 'undefined') {
    return;
  }
  localStorage.setItem(storageKey, JSON.stringify(value));
}

function loadActiveTeam() {
  if (typeof window === 'undefined') {
    return defaultTeams[0];
  }
  return localStorage.getItem(teamStorageKey) || defaultTeams[0];
}

function loadHistory(team: string): LatLngTuple[] {
  if (typeof window === 'undefined') {
    return [];
  }
  const stored = localStorage.getItem(`${historyKeyPrefix}${team}`);
  if (!stored) {
    return [];
  }
  try {
    const parsed = JSON.parse(stored) as LatLngTuple[];
    if (Array.isArray(parsed)) {
      return parsed.filter(isLatLngTuple);
    }
    return [];
  } catch {
    return [];
  }
}

function persistHistory() {
  if (typeof window === 'undefined') {
    return;
  }
  const key = `${historyKeyPrefix}${activeTeam.value}`;
  localStorage.setItem(key, JSON.stringify(positionHistory.value));
}

function createDefaultSectors(): SectorConfig[] {
  return [
    {
      id: 'N',
      name: 'Nord-Sektor',
      color: '#FF6B6B',
      coordinates: [
        [51.9652, 7.6402],
        [51.9668, 7.6387],
        [51.9689, 7.6395],
        [51.9709, 7.642],
        [51.9722, 7.6468],
        [51.9716, 7.6524],
        [51.9695, 7.6558],
        [51.9674, 7.6564],
        [51.9657, 7.6518],
        [51.965, 7.6461],
        [51.965, 7.6428],
      ],
      visible: true,
      served: false,
      servedBy: null,
    },
    {
      id: 'E',
      name: 'Ost-Sektor',
      color: '#339AF0',
      coordinates: [
        [51.965, 7.6461],
        [51.9657, 7.6518],
        [51.9674, 7.6564],
        [51.9669, 7.6605],
        [51.966, 7.6624],
        [51.965, 7.6635],
        [51.964, 7.6639],
        [51.963, 7.663],
        [51.962, 7.661],
        [51.9612, 7.6584],
        [51.9608, 7.6542],
        [51.9616, 7.6493],
        [51.9627, 7.6466],
        [51.9636, 7.6452],
      ],
      visible: true,
      served: false,
      servedBy: null,
    },
    {
      id: 'S',
      name: 'Süd-Sektor',
      color: '#FF922B',
      coordinates: [
        [51.9636, 7.6452],
        [51.9627, 7.6466],
        [51.9616, 7.6493],
        [51.9608, 7.6542],
  [51.9596, 7.6556],
  [51.9586, 7.6562],
  [51.9576, 7.6565],
  [51.9567, 7.6558],
  [51.9558, 7.6539],
  [51.9554, 7.6515],
  [51.9556, 7.649],
        [51.9548, 7.6462],
        [51.9572, 7.6446],
        [51.9584, 7.6409],
        [51.9605, 7.6399],
        [51.962, 7.6422],
      ],
      visible: true,
      served: false,
      servedBy: null,
    },
  ];
}

function isValidSector(value: Partial<SectorConfig>): value is SectorConfig {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof value.id === 'string' &&
    typeof value.name === 'string' &&
    typeof value.color === 'string' &&
    Array.isArray(value.coordinates) &&
    value.coordinates.every(isLatLngTuple) &&
    typeof value.visible === 'boolean' &&
    typeof value.served === 'boolean'
  );
}

function isLatLngTuple(value: unknown): value is LatLngTuple {
  return (
    Array.isArray(value) &&
    value.length === 2 &&
    typeof value[0] === 'number' &&
    typeof value[1] === 'number'
  );
}

function resetServed() {
  if (allSectorsOpen.value) {
    return;
  }
  sectors.value = sectors.value.map(sector => ({
    ...sector,
    served: false,
    servedBy: null,
  }));
}

function toggleTracking() {
  if (trackingActive.value) {
    stopTracking();
  } else {
    startTracking();
  }
}

function startTracking() {
  if (!geolocationSupported || watchId.value !== null) {
    return;
  }
  trackingError.value = null;
  watchId.value = navigator.geolocation.watchPosition(
    handlePositionUpdate,
    handleTrackingError,
    { enableHighAccuracy: true, maximumAge: 5000, timeout: 15000 }
  );
  trackingActive.value = true;
}

function stopTracking() {
  if (watchId.value !== null && typeof navigator !== 'undefined') {
    navigator.geolocation.clearWatch(watchId.value);
    watchId.value = null;
  }
  trackingActive.value = false;
}

function handlePositionUpdate(position: GeolocationPosition) {
  const point: LatLngTuple = [position.coords.latitude, position.coords.longitude];
  const last = positionHistory.value.length
    ? positionHistory.value[positionHistory.value.length - 1]
    : null;

  userPosition.value = point;

  if (!last || distanceMeters(last, point) >= 5) {
    positionHistory.value = [...positionHistory.value, point];
  }

  if (autoCenter.value && mapInstance.value) {
    mapInstance.value.setView(point, Math.max(mapInstance.value.getZoom(), 17));
  }
}

function handleTrackingError(error: GeolocationPositionError) {
  trackingError.value = error.message;
  stopTracking();
}

function clearHistory() {
  positionHistory.value = [];
  userPosition.value = null;
}

function distanceMeters([lat1, lng1]: LatLngTuple, [lat2, lng2]: LatLngTuple) {
  const R = 6371000;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) * Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLng / 2) * Math.sin(dLng / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function mixWithWhite(hex: string, intensity: number) {
  const normalized = normalizeHex(hex);
  const r = parseInt(normalized.slice(0, 2), 16);
  const g = parseInt(normalized.slice(2, 4), 16);
  const b = parseInt(normalized.slice(4, 6), 16);
  const mix = (channel: number) => Math.round(channel + (255 - channel) * intensity);
  return `#${toHex(mix(r))}${toHex(mix(g))}${toHex(mix(b))}`;
}

function normalizeHex(value: string) {
  const trimmed = value.trim().replace('#', '');
  if (trimmed.length === 3) {
    return trimmed
      .split('')
      .map(char => char + char)
      .join('');
  }
  return trimmed.padEnd(6, '0').slice(0, 6);
}

function toHex(value: number) {
  return value.toString(16).padStart(2, '0');
}

function handleServedChange(sector: SectorConfig, event: Event) {
  const target = event.target as HTMLInputElement;
  const checked = Boolean(target?.checked);
  sector.served = checked;
  sector.servedBy = checked ? (activeTeam.value || null) : null;
  sectors.value = [...sectors.value];
}

function formatLatLng(point: LatLngTuple | null) {
  if (!point) {
    return '—';
  }
  return `${point[0].toFixed(5)}, ${point[1].toFixed(5)}`;
}
</script>

<style scoped lang="scss">
@use "../assets/styles/main" as *;

.flyer-sectors {
  display: flex;
  flex-direction: row;
  height: 100vh;
  background-color: #1f1b2f;
  color: #f8f4f1;
}

.map-wrapper {
  flex: 1;
  min-width: 0;
  position: relative;
}

.map {
  position: absolute;
  inset: 0;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.control-panel {
  width: 360px;
  max-width: 100%;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: rgba(9, 6, 20, 0.88);
  overflow-y: auto;
}

header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

h1 {
  margin: 0;
  font-size: 1.5rem;
}

p {
  margin: 0;
  font-size: 0.9rem;
  color: rgba(248, 244, 241, 0.7);
}

.reset {
  align-self: flex-start;
  background: linear-gradient(120deg, #ff6b6b, #f06595);
  color: white;
  border: none;
  border-radius: 999px;
  padding: 0.35rem 1rem;
  font-size: 0.85rem;
  cursor: pointer;
}

.reset:hover {
  filter: brightness(1.05);
}

.reset:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.team-selector {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.9rem;
}

.team-selector select {
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: 0.75rem;
  padding: 0.45rem 0.6rem;
  color: inherit;
}

.tracking-card {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 1rem;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25);
}

.tracking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.tracking-header h2 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #f8f4f1;
}

.tracking-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tracking-actions button {
  flex: 1 1 140px;
  border-radius: 999px;
  border: none;
  padding: 0.45rem 0.75rem;
  background: rgba(255, 255, 255, 0.08);
  color: inherit;
  cursor: pointer;
}

.tracking-actions button:hover {
  filter: brightness(1.1);
}

.tracking-status {
  font-size: 0.85rem;
  color: rgba(248, 244, 241, 0.7);
}

.tracking-status.active {
  color: #8df7a9;
}

.tracking-status.error {
  color: #ff8787;
}

.history-stats {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 0.8rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.sectors {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sector-card {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 1rem;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.title-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  font-weight: 600;
}

.name-input {
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: 0.75rem;
  padding: 0.35rem 0.75rem;
  color: inherit;
  min-width: 8rem;
}

.status {
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  background: rgba(255, 213, 0, 0.1);
  font-size: 0.8rem;
}

.status.served {
  background: rgba(81, 207, 102, 0.15);
  color: #8df7a9;
}

.team-info {
  font-size: 0.8rem;
  color: rgba(141, 247, 169, 0.9);
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.85rem;
}

.field input[type='color'],
.field input[type='text'] {
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: 0.75rem;
  padding: 0.4rem 0.6rem;
  color: inherit;
}

.area-hint {
  font-size: 0.75rem;
  color: rgba(248, 244, 241, 0.5);
}

.coords ul {
  list-style: none;
  margin: 0;
  padding: 0.35rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.75rem;
}

.coords li {
  font-family: 'Fira Code', 'Courier New', monospace;
  color: rgba(248, 244, 241, 0.65);
}

.toggles {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  align-items: center;
}

.toggles label {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.sector-label {
  color: #1f1b2f;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 0.75rem;
  padding: 0.15rem 0.5rem;
  font-weight: 600;
  text-align: center;
  display: inline-flex;
  flex-direction: column;
  gap: 0.1rem;
  font-size: 0.75rem;
}

.sector-label span {
  font-size: 0.85rem;
}

.sector-label small {
  font-size: 0.65rem;
  color: #555260;
}

@media (max-width: 960px) {
  .flyer-sectors {
    flex-direction: column;
  }

  .map {
    position: relative;
    height: 50vh;
    border-right: none;
  }

  .control-panel {
    width: 100%;
    height: auto;
  }
}
</style>
