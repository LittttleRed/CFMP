
<template>
<div>
  <h1>{{product_id}}</h1>
</div>
</template>
<script setup>
import {useRoute, useRouter} from "vue-router";

const route = useRoute()
const router = useRouter()
const product_id = route.query.product_id
</script>

<style scoped>

</style>