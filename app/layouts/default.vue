<script setup lang="ts">
const { loggedIn, clear } = useAppUserSession()

function handleLogout() {
  clear()
}
</script>

<template>
  <div>
    <header>
      <ColorScheme>
        <USelect v-model="$colorMode.preference" color="white" :options="['system', 'light', 'dark']" />
      </ColorScheme>
      <div class="button-login">
        <UButton v-if="loggedIn" @click="handleLogout" color="gray" variant="outline">Logout</UButton>
        <UButton v-else to="/login/" color="gray" variant="outline">Admin</UButton>
      </div>
    </header>
    <main>
      <slot />
    </main>
  </div>
</template>

<style scoped>
header {
  @apply flex justify-end p-5 gap-4
}

main {
  @apply px-20
}

.button-login {
  @apply w-16
}
</style>
