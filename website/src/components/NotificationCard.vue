<template>
  <div class="notification-card">
    <div class="flex-container">
      <img :src="imageSrc" alt="title" class="notification-image" :class="{ rounded: roundedImage }" />
      <div class="notification-content">
        <div class="notification-header">
          <h3 class="notification-title">{{ title }}</h3>
          <span v-if="false" class="notification-age">{{ timeAgo }}</span>
        </div>
        <p class="notification-text">{{ text }}</p>
      </div>
    </div>
    <a v-if="linkTo" :href="linkTo">{{linkText ? linkText : linkTo}} >></a>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useTimeAgo } from '@vueuse/core';
import defaultImage from '../assets/images/icons8-neu-64.png';
import type { UseTimeAgoMessages } from '@vueuse/core';

const props = defineProps({
  title: { type: String, required: true },
  text: { type: String, required: true },
  linkText: { type: String },
  linkTo: { type: String },
  image: { type: String, default: null },
  createdAt: { type: [String, Date], required: true },
  roundedImage: { type: Boolean, default: false },
});

const imageSrc = computed(() => {
  return props.image ? new URL(`/src/assets/images/${props.image}`, import.meta.url).href : defaultImage;
});

const messages: UseTimeAgoMessages = {
  justNow: 'gerade eben',
  past: (n: string) => n,
  future: (n: string) => `in ${n}`,
  month: (n) => `${n} Monat${n > 1 ? 'e' : ''}`,
  year: (n) => `${n} Jahr${n > 1 ? 'e' : ''}`,
  day: (n) => `${n} Tag${n > 1 ? 'e' : ''}`,
  week: (n) => `${n} Woche${n > 1 ? 'n' : ''}`,
  hour: (n) => `${n} Stunde${n > 1 ? 'n' : ''}`,
  minute: (n) => `${n} Minute${n > 1 ? 'n' : ''}`,
  second: (n) => `${n} Sekunde${n > 1 ? 'n' : ''}`,
  invalid: '',
};

const timeAgo = useTimeAgo(new Date(props.createdAt), {
  messages,
  showSecond: false,
});
</script>

<style scoped lang="scss">
@import "../assets/styles/main.scss";

.notification-card {
  transition: box-shadow 0.2s ease-in-out;
  border: 1px solid lightgrey;

  .flex-container {
    display: flex;
    align-items: center;

    img {display: none}
  }

  a {
    display: block;
    text-align: right;
    padding-right: 8px;
    font-size: .75rem;
    color: #0095f6;
  }

  background-color: #fff8f0;
  border-radius: 1rem;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  padding: 1rem;
  margin-bottom: 1rem;
  border-left: 4px solid #ceaa724d;
}
.notification-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.notification-image {
  width: 48px;
  height: 48px;
  object-fit: cover;
  margin-right: 12px;
  &.rounded {
    border-radius: 50%;
  }
}
.notification-content {
  flex: 1;
}
.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.notification-title {
  color: $accent-color;
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}
.notification-age {
  font-size: .65rem;
  color: #888;
}
.notification-text {
  margin-top: 4px;
  font-size: .8rem;
  color: #555;
}
</style>
