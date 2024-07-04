// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxt/ui", "nuxt-auth-utils"],
  runtimeConfig: {
    public: {
      apiURL: process.env.API_URL || 'http://localhost:8000/app/'
    },
  },
})