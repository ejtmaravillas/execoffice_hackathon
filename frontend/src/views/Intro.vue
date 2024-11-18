<script setup>
  import { ref } from "vue";
  import Dashboard from "./Dashboard.vue";

  const showLogo = ref(true);
  const showText = ref(false);

  const handleAnimationEnd = () => {
    showLogo.value = false;
    showText.value = true;
  };
</script>

<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <img
      v-if="showLogo"
      class="logo-animation"
      src="@/assets/imgs/logo.jpg"
      alt="Logo"
      @animationend="handleAnimationEnd"
    />
    <div v-if="showText">
      <Dashboard />
    </div>
  </div>
</template>

<style>
@keyframes scaleAndFade {
  0% {
    transform: scale(2);
    opacity: 1; 
  }
  100% {
    transform: scale(4); 
    opacity: 0; 
  }
}

.logo-animation {
  width: 150px; 
  height: 150px; 
  animation: scaleAndFade 2s ease-in-out forwards;
}
</style>
