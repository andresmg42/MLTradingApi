import axios from "axios"

export const BASE_URL=import.meta.env.VITE_BASE_INFERENCE_URL || 'http://localhost:8001'

const apiInfernce=axios.create({baseURL:BASE_URL})

export default apiInfernce;