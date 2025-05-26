import axios from '@/api/axios'

export async function fetchRecommendations(input, model = 'gpt-4') {
  try {
    const response = await axios.post('/api/recommend/', { input, model })
    return response.data
  } catch (error) {
    console.error('[추천 실패]', error)
    throw error
  }
}