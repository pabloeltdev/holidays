export default defineNuxtPlugin((nuxtApp) => {
  const { session } = useAppUserSession()
  const config = useRuntimeConfig()

  const { isOpen, errorMessage } = useErrorModal()

  const api = $fetch.create({
    baseURL: config.public.apiURL,
    onRequest({ options }) {
      if (session.value?.token) {
        const headers = options.headers ||= {}
        if (Array.isArray(headers)) {
          headers.push(['Authorization', `Token ${session.value?.token}`])
        } else if (headers instanceof Headers) {
          headers.set('Authorization', `Token ${session.value?.token}`)
        } else {
          headers.Authorization = `Token ${session.value?.token}`
        }
      }
    },
    async onResponseError({ response }) {
      if (response.status === 403) {
        await nuxtApp.runWithContext(() => navigateTo('/login'))
      }
      const { status, statusText } = response
      if (status === 400 || isOpen.value) return
      let message = 'Could not do this action. '
      let data = null
      if (response._data) data = response._data
      else data = await response.json()
      if (statusText) {
        message += statusText + '. '
      } else {
        message += 'Unexpected error. '
      }
      if (Object.hasOwn(data, 'detail')) {
        message += data['detail']
      }
      errorMessage.value = message
      isOpen.value = true
    },
    async onRequestError() {
      if (nuxtApp.payload.path != '/') {
        await nuxtApp.runWithContext(() => navigateTo('/'))
      }
      errorMessage.value = 'System is offline.'
      isOpen.value = true
    }
  })
  return {
    provide: {
      api
    }
  }
})
