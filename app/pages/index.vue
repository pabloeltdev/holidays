<script setup lang="ts">
import type { Holiday } from '~/types/holiday';
const { data: holidays } = await useAPI<Holiday[]>('/holidays/')
const { loggedIn } = useAppUserSession()
</script>

<template>
  <div>
    <ErrorModal />
    <div class="mt-5">
      <UButton v-if="loggedIn" to="/holidays/create/" class="ml-5" variant="soft">Create holiday</UButton>
      <span v-else-if="holidays?.length == 0">No holidays created. Login as admin and create one.</span>
      <div class="holidays-container">
        <HolidayItem class="holiday-item" v-for="holiday in holidays" :holiday="holiday" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  @apply flex justify-between mx-5
}

.holidays-container {
  @apply flex flex-wrap
}

.holiday-item {
  @apply w-full md:w-1/2 lg:w-1/3
}
</style>
