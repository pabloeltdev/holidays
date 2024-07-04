<script lang="ts" setup>
import type { Holiday } from '~/types/holiday';

const { holiday } = defineProps<{ holiday: Holiday }>()
const router = useRouter()

function goToInfo() {
  router.push(`holidays/${holiday.pk}/info/`)
}
</script>

<template>
  <div class="root-container">
    <UCard class="h-full">
      <template #header>
        <div class="image-container">
          <img v-if="holiday.image" class="image" :src="holiday.image" alt="" />
          <div v-else class="image placeholder" />
        </div>
        <div class="text-nowrap overflow-hidden text-ellipsis">
          <span class="country">{{ holiday.country }}: </span>
          <span class="title">{{ holiday.title }}</span>
        </div>
        <div class="date">
          <span>{{ holiday.event_long_month }}</span>
          <span>&nbsp;</span>
          <span>{{ holiday.event_day }}</span>
        </div>
      </template>
      <template #footer>
        <UButton @click="goToInfo" variant="ghost">See details</UButton>
      </template>
    </UCard>
  </div>
</template>

<style scoped>
.root-container {
  @apply px-5 py-5 h-full
}

.image-container {
  @apply flex flex-col
}

.image {
  @apply aspect-[16/9] rounded-lg
}

.image.placeholder {
  @apply bg-gray-200 dark:bg-gray-800
}

.country {
  @apply text-gray-800 dark:text-gray-100
}

.title {
  @apply text-gray-700 dark:text-gray-200
}

.date {
  @apply flex justify-end text-gray-500
}
</style>
