<script setup lang="ts">
import type { Holiday } from '~/types/holiday';

const route = useRoute()
const router = useRouter()

const { data: holiday } = await useAPI<Holiday>(`/holidays/${route.params.id}/`)

function handleEdit() {
  router.push(`/holidays/${route.params.id}/edit/`)
}

</script>

<template>
  <div>
    <ErrorModal />
    <div class="root-container">
      <UContainer class="content-container">
        <div v-if="holiday?.image" class="image-container">
          <img class="image" :src="holiday.image" alt="">
        </div>
        <div class="info">
          <div class="title">
            <UButton @click="handleEdit" icon="i-heroicons-pencil-square-solid" color="gray" variant="ghost" />
            <span>{{ holiday?.title }} ({{ holiday?.country }})</span>
          </div>
          <p class="description">{{ holiday?.description }}</p>
          <span class="date"></span>
        </div>
      </UContainer>
    </div>
  </div>
</template>

<style scoped>
.root-container {
  @apply py-10
}

.info {
  @apply overflow-clip
}

.title {
  @apply text-lg flex items-center
}

.description {
  @apply mt-4 break-words dark:text-gray-200 text-gray-800
}

.image-container {
  @apply flex justify-center aspect-[16/9]
}

.image {
  @apply pb-4 rounded-lg
}
</style>
