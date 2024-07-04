export const useErrorModal = () => {
  const isOpen = useState('errorModalIsOpen', () => false)
  const errorMessage = useState('errorModalMessage', () => '')
  return { isOpen, errorMessage }
}
