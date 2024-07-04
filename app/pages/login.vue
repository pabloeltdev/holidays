<script setup lang="ts">
import { z } from 'zod'
import type { Form, FormSubmitEvent } from '#ui/types'
import { FetchError } from 'ofetch'

const schema = z.object({
  username: z.string(),
  password: z.string()
})

type Schema = z.output<typeof schema>

const state = reactive({
  username: undefined,
  password: undefined
})

const router = useRouter()
const { $api } = useNuxtApp()
const { session } = useAppUserSession()

const form = ref<Form<Schema>>()

async function onSubmit(event: FormSubmitEvent<Schema>) {
  try {
    const data: { token: string } = await $api(
      'auth/', {
      method: 'post',
      body: { ...event.data }
    })
    session.value.user = { name: event.data.username }
    session.value.token = data.token
    // redirect
    router.push('/')
  } catch (e) {
    if (e instanceof FetchError) {
      if (e.statusCode == 400) {
        const data: Record<string, string[]> = e.data!
        form.value!.setErrors(
          Object.keys(data).map((key) => {
            return {
              message: data[key].join(' '),
              path: key
            }
          })
        )
      }

    }
    console.error(e)
  }
}
</script>

<template>
  <div>
    <ErrorModal />
    <UContainer class="flex mt-10 justify-center">
      <UCard class="w-1/2">
        <UForm ref="form" :schema="schema" :state="state" class="space-y-4" @submit="onSubmit">
          <UFormGroup label="Username" name="username">
            <UInput v-model="state.username" autocomplete="username" />
          </UFormGroup>

          <UFormGroup label="Password" name="password">
            <UInput v-model="state.password" type="password" autocomplete="current-password" />
          </UFormGroup>

          <UFormGroup name="non_field_errors" />

          <UButton type="submit">
            Login
          </UButton>
        </UForm>
      </UCard>
    </UContainer>
  </div>
</template>
