import axios from 'axios'

const TMDB_API_KEY = 'f2fd16b8032965fdf2108baab6171e4e' // 여기에 키 넣기
const BASE_URL = 'https://api.themoviedb.org/3'

export async function searchMovieByTitle(title) {
  const response = await axios.get(`${BASE_URL}/search/movie`, {
    params: {
      api_key: TMDB_API_KEY,
      query: title,
      include_adult: false,
      language: 'ko-KR',
    },
  })

  const results = response.data.results
  return results.length ? results[0] : null
}

export async function getMovieDetails(movieId) {
  const response = await axios.get(`https://api.themoviedb.org/3/movie/${movieId}`, {
    params: {
      api_key: TMDB_API_KEY,
      language: 'ko-KR',
      append_to_response: 'credits', // 감독, 배우 등 포함
    },
  })

  return response.data
}
