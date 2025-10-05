<template>
  <nav class="navigation-bar">
    <router-link to="/home" class="nav-link" active-class="active">
      <img src="../assets/images/icons8-zuhause-64.png" alt="Home" class="nav-icon"/>
    </router-link>
    <router-link to="/vino" class="nav-link" active-class="active">
      <img src="../assets/images/icons8-bar-50.png" alt="Vino" class="nav-icon"/>
    </router-link>
    <router-link to="/drinks" class="nav-link" active-class="active">
      <img src="../assets/images/icons8-drinks-64.png" alt="Getränke" class="nav-icon"/>
    </router-link>
    <router-link to="/snacks" class="nav-link" active-class="active">
      <img src="../assets/images/icons8-snack-64.png" alt="Snacks" class="nav-icon"/>
    </router-link>
    <router-link to="/legals" class="nav-link info-link" active-class="active" aria-label="Impressum und Datenschutz">
      Info
    </router-link>
  </nav>
</template>

<script setup lang="ts">
</script>

<style scoped lang="scss">
@use "../assets/styles/main" as *;

.navigation-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;

  display: flex;
  justify-content: center;
  gap: 1rem;

  background-color: $primary-color;
  padding: 0.5rem 0;
  z-index: 1000;
  border-top: 1px solid $dark-color;

  .nav-link {
    text-decoration: none;
    color: $dark-color;
    font-size: 1rem;
    padding: 0 0.5rem;

    &.active {
      font-weight: bold;
      border-bottom: 5px solid $accent-color;
    }

    .nav-icon {
      width: 24px;
      height: 24px;
    }
  }

  .info-link {
    display: flex;
    align-items: center;
    font-family: 'King Red', serif;
    color: $accent-color;
  }

  .showroom-link {
    opacity: 0;
    animation: fadeIn 0.5s forwards;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>