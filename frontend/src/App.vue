<template>
  <div class="container">
    <div class="text-center">
      <a href="https://vuejs.org/" target="_blank">
        <img src="./assets/alphafold.png" class="logo alphafold" alt="Alphafold logo" />
      </a>
    </div>
    <router-view />
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
