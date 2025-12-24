<template>
  <section
    v-if="items && items.length"
    class="featured-slider"
    aria-label="Highlights"
    @mouseenter="stopAutoScroll"
    @mouseleave="startAutoScroll"
    @touchstart.passive="stopAutoScroll"
    @touchend.passive="startAutoScroll"
  >
    <button
      class="slider-nav prev"
      type="button"
      aria-label="Vorheriges Highlight"
      @click="prevSlide"
    >
      <span aria-hidden="true">‹</span>
    </button>

    <div class="slider-viewport" ref="sliderViewport" @scroll.passive="handleManualScroll">
      <div class="slider-track" role="list" ref="sliderTrack">
        <article
          v-for="item in items"
          :key="item.id"
          class="slider-card"
          role="listitem"
        >
          <img
            class="slider-image"
            :src="item.image || fallbackImage"
            :alt="item.title"
            loading="lazy"
          />
          <div class="slider-copy">
            <h2>{{ item.title }}</h2>
            <p>{{ item.description }}</p>
          </div>
        </article>
      </div>
    </div>

    <button
      class="slider-nav next"
      type="button"
      aria-label="Nächstes Highlight"
      @click="nextSlide"
    >
      <span aria-hidden="true">›</span>
    </button>
  </section>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue";

interface SliderItem {
  id: string;
  title: string;
  description: string;
  image?: string;
}

const props = defineProps<{ items: SliderItem[] }>();
const fallbackImage =
  'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><circle cx="60" cy="60" r="58" fill="%23ceaa72"/><text x="60" y="78" text-anchor="middle" font-size="72" fill="white" font-family="Arial, sans-serif">i</text></svg>';
const sliderViewport = ref<HTMLDivElement | null>(null);
const sliderTrack = ref<HTMLDivElement | null>(null);
const currentIndex = ref(0);
const AUTO_INTERVAL = 6000;
let autoScrollHandle: number | undefined;
let scrollDebounceHandle: number | undefined;

const scrollToIndex = (index: number) => {
  const viewport = sliderViewport.value;
  const track = sliderTrack.value;
  if (!viewport || !track) return;
  const target = track.children[index] as HTMLElement | undefined;
  if (!target) return;
  viewport.scrollTo({ left: target.offsetLeft, behavior: "smooth" });
};

const nextSlide = () => {
  if (!props.items?.length) return;
  currentIndex.value = (currentIndex.value + 1) % props.items.length;
  scrollToIndex(currentIndex.value);
};

const prevSlide = () => {
  if (!props.items?.length) return;
  currentIndex.value = (currentIndex.value - 1 + props.items.length) % props.items.length;
  scrollToIndex(currentIndex.value);
};

const stopAutoScroll = () => {
  if (autoScrollHandle) {
    clearInterval(autoScrollHandle);
    autoScrollHandle = undefined;
  }
};

const startAutoScroll = () => {
  stopAutoScroll();
  if (props.items?.length > 1) {
    autoScrollHandle = window.setInterval(nextSlide, AUTO_INTERVAL);
  }
};

const handleManualScroll = () => {
  const viewport = sliderViewport.value;
  const track = sliderTrack.value;
  if (!viewport || !track || !props.items?.length) return;
  stopAutoScroll();
  if (scrollDebounceHandle) {
    clearTimeout(scrollDebounceHandle);
  }
  scrollDebounceHandle = window.setTimeout(() => {
    const children = Array.from(track.children) as HTMLElement[];
    let closestIndex = 0;
    let smallestDelta = Number.POSITIVE_INFINITY;
    children.forEach((child, index) => {
      const delta = Math.abs(child.offsetLeft - viewport.scrollLeft);
      if (delta < smallestDelta) {
        smallestDelta = delta;
        closestIndex = index;
      }
    });
    currentIndex.value = closestIndex;
    scrollDebounceHandle = undefined;
    startAutoScroll();
  }, 140);
};

const handleVisibilityChange = () => {
  if (document.hidden) {
    stopAutoScroll();
  } else {
    startAutoScroll();
  }
};

onMounted(() => {
  startAutoScroll();
  document.addEventListener("visibilitychange", handleVisibilityChange);
});

onBeforeUnmount(() => {
  stopAutoScroll();
  if (scrollDebounceHandle) {
    clearTimeout(scrollDebounceHandle);
  }
  document.removeEventListener("visibilitychange", handleVisibilityChange);
});

watch(
  () => props.items?.length,
  () => {
    currentIndex.value = 0;
    scrollToIndex(0);
    startAutoScroll();
  }
);
</script>

<style scoped lang="scss">
@use "../assets/styles/main" as *;

.featured-slider {
  margin: 0 auto 1.25rem;
  max-width: 960px;
  position: relative;
}

.slider-viewport {
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.slider-viewport::-webkit-scrollbar {
  display: none;
}

.slider-track {
  display: flex;
  gap: 0.85rem;
  scroll-behavior: smooth;
  padding-bottom: 0.25rem;
}

.slider-card {
  background: rgba(22, 14, 46, 0.85);
  border: 1px solid rgba(206, 170, 114, 0.5);
  border-radius: 16px;
  padding: 0.65rem 0.75rem;
  min-width: 280px;
  max-width: 340px;
  display: flex;
  gap: 0.65rem;
  align-items: center;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18);
  scroll-snap-align: start;
}

.slider-image {
  width: 68px;
  height: 68px;
  border-radius: 12px;
  object-fit: contain;
  background: rgba(255, 255, 255, 0.05);
  flex-shrink: 0;
}

.slider-copy {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.slider-copy h2 {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.2;
  color: $accent-color;
}

.slider-copy p {
  margin: 0;
  font-size: 0.78rem;
  line-height: 1.3;
}

.slider-nav {
  background: rgba(206, 170, 114, 0.15);
  border: 1px solid rgba(206, 170, 114, 0.45);
  color: $accent-color;
  border-radius: 999px;
  width: 42px;
  height: 42px;
  font-size: 1.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s ease;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}

.slider-nav:hover,
.slider-nav:focus-visible {
  background: rgba(206, 170, 114, 0.35);
}

.slider-nav span {
  line-height: 1;
}

.slider-nav.prev {
  left: 0;
}

.slider-nav.next {
  right: 0;
}

@media (max-width: 720px) {
  .featured-slider {
    padding: 0;
  }

  .slider-card {
    min-width: 80vw;
    max-width: 260px;
  }

  .slider-nav {
    width: 38px;
    height: 38px;
  }
}
</style>
