

<script setup lang="ts">

import { ParticlesComponent } from 'particles.vue3';
import { loadSlim } from 'tsparticles-slim'
import { particles_config } from '../components/background/particles-config'
const particlesInit = async engine => {
    //await loadFull(engine);
    await loadSlim(engine);
};
const particlesLoaded = async container => {
    console.log(container);
};
</script>

<style scoped lang="less">

</style>
<template>
  <ParticlesComponent
    id="tsparticles"
    :particlesInit="particlesInit"
    :particlesLoaded="particlesLoaded"
    :options="particles_config"
  />
</template>
