import axios from "axios"

export const BASE_URL=import.meta.env.VITE_BASE_TRAIN_URL || 'http://localhost:8000'

const apiTrain=axios.create({baseURL:BASE_URL})

export default apiTrain;