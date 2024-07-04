<script setup lang="ts">
const { isOpen, errorMessage } = useErrorModal()
</script>

<template>
  <UModal v-model="isOpen" v-bind="$attrs">
    <UCard :ui="{ ring: '', divide: 'divide-y divide-gray-100 dark:divide-gray-800' }">
      <template #header>
        An Error has occurred
      </template>

      {{ errorMessage }}

      <template #footer>
        <UButton @click="isOpen = false">Ok</UButton>
      </template>
    </UCard>
  </UModal>
</template>
