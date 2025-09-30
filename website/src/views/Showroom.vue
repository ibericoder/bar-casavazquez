<template>
  <div class="showroom">
    <h2 class="title">Was gibt es hier?</h2>
    <div class="slideshow">
      <div
          v-for="(slide, index) in slides"
          :key="index"
          v-show="index === currentIndex"
          class="slide"
      >
        <img
            :src="slide"
            :alt="`Bild ${index + 1}`"
            class="slide-image"
            loading="lazy"
        />
      </div>

      <button class="nav-button prev" @click="prevSlide">‹</button>
      <button class="nav-button next" @click="nextSlide">›</button>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, ref, onMounted, onUnmounted} from 'vue';

export default defineComponent({
  name: 'Showroom',
  setup() {
    const slideNames = [
      '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg',
      '6.jpg', '7.jpg', '9.jpg', '10.webp',
      '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.jpg', '16.jpg'
    ];
    const base = import.meta.env.BASE_URL;
    const slides = slideNames.map(name => `${base}${name}`);
    const sliderDuration = 4000;
    const currentIndex = ref(0);
    let intervalId: number;

    const startSlideshow = () => {
      intervalId = window.setInterval(() => {
        nextSlide();
      }, sliderDuration);
    };

    const stopSlideshow = () => {
      window.clearInterval(intervalId);
    };

    const resetSlideshow = () => {
      stopSlideshow();
      startSlideshow();
    };

    const nextSlide = () => {
      currentIndex.value = (currentIndex.value + 1) % slides.length;
      resetSlideshow();
    };

    const prevSlide = () => {
      currentIndex.value = (currentIndex.value - 1 + slides.length) % slides.length;
      resetSlideshow();
    };

    onMounted(startSlideshow);
    onUnmounted(() => stopSlideshow());

    return {
      slides,
      currentIndex,
      nextSlide,
      prevSlide,
    };
  },
});
</script>

<style scoped>
.showroom {
  text-align: center;
}

.title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.slideshow {
  position: relative;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  height: 80vh;
  overflow: hidden;
}

.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.slide-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.nav-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(30, 30, 30, 0.6);
  border: none;
  color: #fff;
  font-size: 2.5rem;
  padding: 0.3rem 1rem;
  cursor: pointer;
  z-index: 10;
  border-radius: 0.5rem;
  transition: background 0.2s ease;
}

.nav-button:hover {
  background: rgba(30, 30, 30, 0.8);
}

.prev {
  left: 0;
}

.next {
  right: 0;
}
</style>
