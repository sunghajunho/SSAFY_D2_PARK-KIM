import axios from '@/api/axios'

export async function fetchRecommendations(input) {
  try {
    const response = await axios.post('/api/recommend/', { input })
    return response.data.results
  } catch (error) {
    console.error('[추천 실패]', error)
    throw error
  }
}