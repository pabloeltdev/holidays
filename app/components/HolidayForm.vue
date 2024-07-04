<script setup lang="ts">
import { z } from 'zod'
import type { FormSubmitEvent, Form } from '#ui/types'
import { FetchError } from 'ofetch'
import { format } from 'date-fns'
import type { Holiday } from '~/types/holiday';

const { holiday } = defineProps<{ holiday?: Holiday }>()

const min = (n: number): [number, string] => ([n, `Must have at least ${n} characters.`])
const max = (n: number): [number, string] => ([n, `Must have at max ${n} characters.`])

const year = new Date().getFullYear()
const minDate = new Date(year, 0, 1, 0, 0)
const maxDate = new Date(year, 11, 31, 23, 59)

const schema = z.object({
  title: z.string().min(...min(3)).max(...max(100)),
  description: z.string().min(...min(50)).max(...max(5000)),
  country: z.string().min(...min(4)).max(...max(30)),
  image: z.instanceof(File).optional()
    .refine((file) => (file?.size ?? 0) <= 5 * 1024 * 1024, `Max file size is 5MB.`),
  date: z.date().min(minDate).max(maxDate),
})

type Schema = z.output<typeof schema>

const state = reactive({
  title: holiday?.title,
  description: holiday?.description,
  country: holiday?.country,
  image: undefined as (File | undefined),
  date: holiday ? new Date(
    new Date().getFullYear(),
    holiday.event_month - 1,
    holiday.event_day - 1) : new Date(),
})

const router = useRouter()

const { $api } = useNuxtApp()
const image_url = ref(holiday?.image ?? '')
const form = ref<Form<Schema>>()
const fileInput = ref<{ input: HTMLInputElement }>()

function handleFileChange([file]: FileList) {
  if (image_url.value != '') URL.revokeObjectURL(image_url.value)
  image_url.value = file ? URL.createObjectURL(file) : ''
  state.image = file ?? (new File([], ''))
}

function handleClear() {
  fileInput.value!.input.value = ''
  if (image_url.value != '') URL.revokeObjectURL(image_url.value)
  image_url.value = ''
  state.image = new File([], '')
}

async function handleSubmit(event: FormSubmitEvent<Schema>) {
  // Make an update or a post
  //   edit
  // Send the data
  try {
    const { date, ...eventData } = event.data
    const data = {
      event_day: date.getDate(),
      event_month: date.getMonth() + 1,
      ...eventData
    }
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value != undefined) formData.append(key, value as string | Blob)
    });
    // Avoid upload duplication:
    // Use patch for the data
    // After use patch for image if it was modified
    if (holiday) {
      await $api(`holidays/${holiday.pk}/`, { method: 'put', body: formData })
    } else {
      await $api('holidays/', { method: 'post', body: formData })
    }
    router.push('/')
  } catch (e) {
    if (e instanceof FetchError) {
      if (e.statusCode == 400) {
        const { event_day, event_month, ...data }: Record<string, string[]> = e.data!
        const dateErrors = new Set([...(event_day ?? []), ...(event_month ?? [])])
        data['date'] = [...dateErrors.values()]
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
    <UForm ref="form" :schema="schema" :state="state" class="space-y-4" @submit="handleSubmit">
      <UFormGroup label="Title" name="title">
        <UInput v-model="state.title" autocomplete="off" />
      </UFormGroup>

      <UFormGroup label="Description" name="description">
        <UTextarea v-model="state.description" autoresize placeholder="describe the event..." autocomplete="off" />
      </UFormGroup>

      <UFormGroup label="Country" name="country">
        <UInput v-model="state.country" autocomplete="country-name" />
      </UFormGroup>

      <UFormGroup label="Image" name="image">
        <div class="flex">
          <UInput ref="fileInput" class="flex-grow" type="file" @change="handleFileChange" icon="i-heroicons-folder" />
          <UButton @click="handleClear" variant="link">Clear</UButton>
        </div>
      </UFormGroup>

      <div class="preview">
        <div v-if="image_url === ''">
          <UIcon name="i-heroicons-photo-solid" class="w-8 h-8 text-gray-200 dark:text-gray-800" />
        </div>
        <img v-else :src="image_url" alt="Holiday image">
      </div>

      <UFormGroup name="non_field_errors" />

      <div class="flex justify-between">
        <div>
          <UFormGroup label="Holiday date" name="date">
            <!-- Just to have some element to set the label for -->
            <UInput class="hidden" autocomplete="off" />
            <UPopover :popper="{ placement: 'auto-start' }">
              <UButton color="gray" variant="outline" icon="i-heroicons-calendar-days-20-solid"
                :label="format(state.date, 'd MMMM')" />
              <template #panel="{ close }">
                <DatePicker v-model="state.date" is-required @close="close" :minDate="minDate" :maxDate="maxDate" />
              </template>
            </UPopover>
          </UFormGroup>
        </div>
        <UButton class="submit-button" type="submit">
          Submit
        </UButton>
      </div>
    </UForm>
  </div>
</template>


<style scoped>
.preview {
  @apply flex items-center justify-center h-40 border rounded-lg border-gray-200 dark:border-gray-800 overflow-auto
}

.submit-button {
  @apply h-fit self-end
}
</style>
