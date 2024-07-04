export const useAppUserSession = () => {
  const { session, ...others } = useUserSession()
  type User = {
    name: string
  }
  type CustomUserSession = {
    token?: string,
    user?: User
  }
  type AppUserSession = typeof session & globalThis.Ref<CustomUserSession>
  return { session: session as AppUserSession, ...others }
}
