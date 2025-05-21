export function setWithExpiry(key, value, ttlMs) {
  const now = Date.now()
  const item = {
    value,
    expiry: now + ttlMs
  }
  localStorage.setItem(key, JSON.stringify(item))
}

export function getWithExpiry(key) {
  const itemStr = localStorage.getItem(key)
  if (!itemStr) return null

  const item = JSON.parse(itemStr)
  if (Date.now() > item.expiry) {
    localStorage.removeItem(key)
    return null
  }
  return item.value
}