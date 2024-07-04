<script setup lang="ts">
import type { Holiday } from '~/types/holiday';

const route = useRoute()
const { data: holiday } = await useAPI<Holiday>(`/holidays/${route.params.id}/`)

</script>

<template>
  <div>
    <UContainer class="mx-2 sm:mx-16 md:mx-32 lg:mx-48 my-4">
      <HolidayForm :holiday="holiday!" />
    </UContainer>
  </div>
</template>

<style scoped></style>
